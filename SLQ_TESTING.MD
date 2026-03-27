# Project Milestone 5: SQL Design

**Project:** Cawler ID

**Purpose:** Database schema and testing specification for Cawler ID.

## Overview

This document defines the PostgreSQL database schema and data access methods for the Cawler ID application. It bridges the gap between the FastAPI backend and the stored bird metadata required for identification.

This document answers:

* What tables exist (Users, Bird Species, and Identification History)?
* How are audio files and spectrograms related to bird records?
* How do we verify that the data access routines work correctly?

## 1\) Table: users

**Table Description**
Stores account information and preferences for users.

**Fields**

|Field Name|Description|Constraints|
|-|-|-|
|id|Unique user identifier|Primary Key|
|username|Unique display name|Unique, NOT NULL|
|email|Contact and login email|Unique, NOT NULL|
|password\_hash|Securely hashed password|NOT NULL|
|created\_at|Account creation date|NOT NULL, Default NOW()|

**Table Tests**

|Use Case Name|Description|Test Steps|Expected Result|Status|
|-|-|-|-|-|
|Create new user|Verify a user record can be persisted.|1. Insert valid user row.<br>2. Query by email.|User row exists and matches input.|Pass|

## 2\) Table: bird\_species

**Table Description**
The "Field Guide" table contains reference data for each bird the model can identify.

**Fields**

|Field Name|Description|Constraints|
|-|-|-|
|id|Unique species ID|Primary Key|
|common\_name|Name used in UI (e.g., "American Robin")|NOT NULL|
|scientific\_name|Formal Latin name|Unique|
|description|Brief species bio|NOT NULL|
|ref\_audio\_path|Path to reference .mp3 in /data|NOT NULL|
|ref\_spec\_path|Path to reference spectrogram .png|NOT NULL|
|ref\_image|Path to reference image|NOT NULL|

**Table Tests**

|Use Case Name|Description|Test Steps|Expected Result|Status|
|-|-|-|-|-|
|Fetch Bird Details|Ensure species metadata is retrievable by name.|1. Query table for common\_name = 'American Robin'.|Returns correct scientific name and file paths.|Pass|

## 3\) Table: identification\_history

**Table Description**
Logs every identification attempt made by users to populate the "History" page.

**Fields**

|Field Name|Description|Constraints|
|-|-|-|
|id|Unique log ID|Primary Key|
|user\_id|User who performed the upload|Foreign Key → users.id|
|species\_id|The top-ranked bird identified|Foreign Key → bird\_species.id|
|confidence\_score|The similarity score from the model|Float, NOT NULL|
|upload\_path|Path to the user's uploaded audio file|NOT NULL|
|created\_at|Timestamp of analysis|NOT NULL|

**Table Tests**

|Use Case Name|Description|Test Steps|Expected Result|Status|
|-|-|-|-|-|
|Log Analysis Result|Verify an identification result can be linked to a user.|1. Insert result with valid user\_id and species\_id.|Record appears in user's history query.|Pass|

## Data Access Methods

**Access Method: get\_bird\_by\_name**

* **Description:** Fetches full species profile for the "Bird Details" page.
* **Parameters:** common\_name (string)
* **Return Values:** Bird Record Object or 404 Error.

**Access Method: get\_user\_history**

* **Description:** Retrieves all past identifications for a logged-in user.
* **Parameters:** user\_id (int)
* **Return Values:** List of history objects (Bird Name, Date, Score).

## Page-to-Database Mapping

|Page|Tables Accessed|
|-|-|
|Landing|None (Static Content)|
|About|None (Static Content)|
|Upload|None (Static Content)|
|Results|bird\_species (for match data), identification\_history (to save log)|
|Bird Details|bird\_species|
|User Library|identification\_history, bird\_species|



