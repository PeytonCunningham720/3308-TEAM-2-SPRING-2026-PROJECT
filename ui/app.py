from flask import Flask, render_template, request, redirect, url_for, abort, session
import os
import sys
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db import get_bird_by_name, get_user_by_email, create_user, get_user_history, log_identification

from spectrogram.spectrogram_generator import plot_spectrogram, generate_mel_spectrogram
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(__file__), '..', 'data', 'NeuralNetwork'))
from classifier import identify_bird

app = Flask(__name__)
# Configure uploads folder:
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Session config
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_HTTPONLY'] = True


def login_required(f):
    """Decorator: redirect to login if user not in session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# 0) Authentication Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not email or not password:
            return render_template('login.html', error='Email and password required.')

        user = get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('landing'))
        else:
            return render_template('login.html', error='Invalid email or password.')

    return render_template('login.html', error=None)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        if not username or not email or not password:
            return render_template('register.html', error='All fields required.')

        try:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            user = create_user(username, email, password_hash)
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('landing'))
        except Exception:
            error = 'Email or username already exists.'
            return render_template('register.html', error=error)

    return render_template('register.html', error=None)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('landing'))


@app.route('/')
def landing():
    return render_template('landing.html')

# 2) Upload Page
@app.route('/upload')
@login_required
def upload_page():
    return render_template('upload.html')

# 3) Analyze
@app.route('/analyze', methods=['POST'])
@login_required
def analyze():

    # When user submits the form, Flask creates dictionary called request.files
    # Each <input type="file" name="..."> becomes a key in request.files
    if 'audio_file' not in request.files:
        return "No file uploaded", 400

    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded file
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # ("static/uploads", "raven_call.mp3") -> "static/uploads/raven_call.mp3"
    file.save(filepath)

    # Generate spectrogram image for display
    spec = generate_mel_spectrogram(filepath)
    plot_spectrogram(spec, "uploaded_call")

    # Identify bird using trained neural network
    results = identify_bird(filepath)
    results = [r for r in results if r["bird"] != "background_noise"]

    # Log the top identification result to user history
    if results:
        top_result = results[0]
        top_bird_name = top_result.get('bird', '')
        top_score = top_result.get('score', 0.0)

        bird_info = get_bird_by_name(top_bird_name)
        if bird_info:
            log_identification(
                user_id=session.get('user_id'),
                species_id=bird_info['id'],
                confidence_score=float(top_score),
                upload_path=filepath
            )

    return render_template(
        'results.html',
        # *** needs plot_spectogram to save file to static/uploads/
        spectrogram_image="uploads/uploaded_call_spectrogram.png",
        results=results
    )

# 4) Bird Details Page
@app.route('/bird/<bird_name>')
def bird_details(bird_name):
    bird_data = get_bird_by_name(bird_name)
    if bird_data is None:
        abort(404)
    return render_template('bird_details.html', bird=bird_data)
    
# 5) About Page
@app.route('/about')
def about():
    return render_template('about.html')

# 6) User Library (History)
@app.route('/library')
@login_required
def user_library():
    user_id = session.get('user_id')
    history = get_user_history(user_id)
    return render_template('user_library.html', history=history)

if __name__ == '__main__':
    app.run(debug=True)