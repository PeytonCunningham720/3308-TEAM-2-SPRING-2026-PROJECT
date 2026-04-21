# CawlerID Final Report

## Milestone 8: Final Report Submission

## Project Title
CawlerID - Bird Call Identification Web App

## Team Members
- Peyton Cunningham 
- Stephen Enriquez 
- Bri Martinez 
- Jake Mooradian

## Link to Project Repository
https://github.com/PeytonCunningham720/3308-TEAM-2-SPRING-2026-PROJECT

## Link to Project Presentation Slide Deck
https://docs.google.com/presentation/d/1L3VJ6vxHH7hPkUhAACE0VtsKBoXwroGh/edit?usp=sharing&ouid=112170567208295558420&rtpof=true&sd=true

(also included in project repository)

## Repository Readiness

All team members have verified that their latest work is pushed to the remote repository.

The repository contains the following required files and assets:

- README.md
- WEEKLY_STATUS.md
- PAGE_TESTING.md
- SQL_TESTING.md
- FINAL_REPORT.md
- Project presentation slides (linked above)
- Video of demo
- Source code (frontend and backend)
- Requirements text file

## Final Status Report

### What We Completed

- Working MVP including:
- **Presentation:** slides and a customer-facing demo video
- **Bird call identification pipeline:** Users can upload an audio recording (.wav / .mp3) and receive a ranked list of matching bird species, powered by a trained neural network classifier built on mel-spectrogram features extracted with Librosa.
- **Neural network model:** Trained a convolutional/dense classifier on spectrograms derived from Xeno-canto and Kaggle bird-call datasets; integrated into the Flask backend via `classifier.py`.
- **Spectrogram generation:** Visual mel-spectrogram is generated for each uploaded audio file and displayed on the results page.
- **PostgreSQL database:** Full schema and data access layer (`database/db.py`) supporting bird species records, user accounts, and identification history.
- **User authentication:** Registration, login, logout, and session management using Werkzeug password hashing (pbkdf2:sha256).
- **Identification history:** Logged per-user, accessible from the user library page.
- **Bird detail pages:** Individual pages for each identified species with description, image, and taxonomy info; seeded from a local dataset.
- **React-inspired Flask frontend:** Multi-page UI (landing, upload, results, bird detail, user library, about, login/register) with custom CSS styling.
- **Background noise filtering:** Results explicitly exclude `background_noise` classifications.

### What We Were in the Middle of Implementing
- Expanding the bird species database beyond the current seed set (additional North American backyard bird species).
- Improving model accuracy and confidence scoring — exploring data augmentation to address class imbalance in the training set.
- Refining the results page UX (e.g., confidence percentage display, ranked result cards).
- Public deployment with a large enough memory allocation for a single-load neural network

### What We Planned for the Future
- **User accounts enhancements:** Profile pages, ability to save favorite species, and sharing identifications.
- **Mobile-responsive design:** Optimize the UI for phone-based audio uploads (field use).
- **Real-time audio recording:** Allow users to record directly in the browser rather than uploading a file.
- **Expanded species coverage:** Scale the model to cover a broader range of North American birds beyond the backyard MVP set.
- **Map integration:** Show geographic range of identified species on an interactive map.
- **API endpoint:** Expose identification as a REST API for potential third-party integrations.

### Known Problems and Limitations
- Some bird classes have stronger network output (confidence scores)
- Adding bird classes requires neural network retraining and expansion of the database
- Public deployment requires dynamic access to project directory and enough memory to call NN
- The model's accuracy degrades on low-quality or heavily compressed audio files; no pre-upload audio quality warning is shown.
- Password reset / forgot-password flow is not implemented — users who forget their password cannot recover their account.
- The `static/uploads/` directory accumulates files indefinitely; no cleanup policy is in place.
- Some species with very few training samples have noticeably lower identification accuracy.
- The app runs in Flask's built-in development server; a production WSGI deployment (e.g., Gunicorn + Nginx) was not configured.
- No HTTPS enforcement on the hosted instance.

## System Overview

CawlerID uses an offline/online architecture:

OFFLINE:
- Build training dataset
- Train neural network on data
- Test neural network output

ONLINE:
- Frontend: Flask
- Backend: Python
- Database: PostgreSQL

The system was designed to support incremental development, clear separation of concerns, and straightforward testing.

## Pages That Access Database Information

- Login: users
- Register: users
- Analyze (Upload/Results): bird_species, identification_history
- Bird Details Page: bird_species
- User Library: identification_history, bird_species, users

## Page Data Access Tests (High-Level)

### Use case name
User Library loads correct identification history for the logged-in user

### Description
Verify the User Library page displays only past identifications belonging to the currently logged-in user, joined with correct bird species data.

### Pre-conditions
- User account exists in the users table
- User is logged in (valid session)
- User has at least one entry in identification_history

### Test steps
1. Login as a specific user
2. Navigate to /library
3. Observe the identification history list

### Expected result
- Only identifications where identification_history.user_id matches the logged-in user are shown
- Each entry displays the correct common_name, scientific_name, confidence_score, and created_at via the JOIN on bird_species

### Actual result
- Library page shows the correct history entries for the logged-in user, ordered most-recent first

### Status
Pass

### Notes
A second user account with separate history was used to confirm isolation; no cross-user data leakage observed.

### Post-conditions
No data is modified (read-only query).

## Reflection

Over the course of this project we successfully built and integrated all three tiers of a full-stack application: a machine learning audio pipeline, a PostgreSQL-backed Flask server, and a multi-page HTML/CSS frontend. The biggest technical challenge was connecting the ML model output (class labels from the neural network) to real bird records in the database, which required careful normalization of species name strings between the training labels and the bird_species table.

If we were to continue development, the highest-priority improvements would be expanding the species the model can identify, adding a forgot-password flow, and deploying behind a production WSGI server with HTTPS. We also learned that training data quality matters more than model architecture, early accuracy problems were almost entirely due to class imbalance in the dataset, not the network design.
Working in Scrum sprints helped keep the project moving even when individual tasks were blocked, because we could pivot within a sprint rather than waiting for a formal replanning cycle.

Key takeaways:
- Scope control matters. The limited dataset and offline pretraining kept the project shippable.
- Frequent integration reduces surprises later.
- Clear task ownership and weekly check-ins kept progress steady.
- Deployment of a working similarity ranker pipeline early paid off during final integration.

