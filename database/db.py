"""
database/db.py
--------------
Database connection and data-access helpers for Cawler ID.

Expected environment variables:
    DB_HOST      (default: localhost)
    DB_PORT      (default: 5432)
    DB_NAME      (default: cawlerid)
    DB_USER      (default: postgres)
    DB_PASSWORD  (required)
"""

import os
import psycopg2
import psycopg2.extras


def get_connection():
    """Open and return a psycopg2 connection using environment variables."""
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=int(os.environ.get("DB_PORT", 5432)),
        dbname=os.environ.get("DB_NAME", "cawlerid"),
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
    )


# ---------------------------------------------------------------------------
# Data Access Methods
# ---------------------------------------------------------------------------

def get_bird_by_name(common_name: str) -> dict | None:
    """
    Fetch a full species profile by common name.

    Parameters
    ----------
    common_name : str
        The human-readable bird name shown in the UI (e.g. "American Robin").

    Returns
    -------
    dict with keys: id, common_name, scientific_name, description,
                    ref_audio_path, ref_spec_path, ref_image
    None if no matching species is found.
    """
    sql = """
        SELECT id, common_name, scientific_name, description,
               ref_audio_path, ref_spec_path, ref_image
        FROM   bird_species
        WHERE  common_name = %s
        LIMIT  1;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (common_name,))
            row = cur.fetchone()
            return dict(row) if row else None


def get_user_history(user_id: int) -> list[dict]:
    """
    Retrieve all past identifications for a logged-in user.

    Parameters
    ----------
    user_id : int
        Primary key of the user in the users table.

    Returns
    -------
    List of dicts with keys: id, common_name, scientific_name,
                              confidence_score, upload_path, created_at
    Ordered most-recent first.
    """
    sql = """
        SELECT ih.id,
               bs.common_name,
               bs.scientific_name,
               ih.confidence_score,
               ih.upload_path,
               ih.created_at
        FROM   identification_history ih
        JOIN   bird_species           bs ON bs.id = ih.species_id
        WHERE  ih.user_id = %s
        ORDER  BY ih.created_at DESC;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (user_id,))
            return [dict(row) for row in cur.fetchall()]


def log_identification(user_id: int, species_id: int,
                       confidence_score: float, upload_path: str) -> int:
    """
    Persist a new identification result to identification_history.

    Returns the new row's id.
    """
    sql = """
        INSERT INTO identification_history
            (user_id, species_id, confidence_score, upload_path)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (user_id, species_id, confidence_score, upload_path))
            new_id = cur.fetchone()[0]
        conn.commit()
    return new_id


# ---------------------------------------------------------------------------
# User Management
# ---------------------------------------------------------------------------

def get_user_by_email(email: str) -> dict | None:
    """
    Fetch a user record by email address.

    Parameters
    ----------
    email : str
        The user's email.

    Returns
    -------
    dict with keys: id, username, email, password_hash, created_at
    None if no matching user is found.
    """
    sql = """
        SELECT id, username, email, password_hash, created_at
        FROM   users
        WHERE  email = %s
        LIMIT  1;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (email,))
            row = cur.fetchone()
            return dict(row) if row else None


def create_user(username: str, email: str, password_hash: str) -> dict:
    """
    Create a new user account.

    Parameters
    ----------
    username : str
        Unique display name.
    email : str
        Unique email address.
    password_hash : str
        Pre-hashed password (hash using werkzeug.security before calling).

    Returns
    -------
    dict with keys: id, username, email, created_at

    Raises
    ------
    psycopg2.IntegrityError if username or email already exists.
    """
    sql = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
        RETURNING id, username, email, created_at;
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, (username, email, password_hash))
            row = cur.fetchone()
        conn.commit()
    return dict(row) if row else {}
