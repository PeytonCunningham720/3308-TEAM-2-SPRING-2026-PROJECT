from flask import Flask, render_template, request, redirect, url_for, abort
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from database.db import get_bird_by_name

from spectrogram.spectrogram_generator import plot_spectrogram, generate_mel_spectrogram
from ranker.ranker import compare_to_references, generate_mock_spectrogram, reference_specs

app = Flask(__name__)
# Configure uploads folder:
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 1) Landing Page
@app.route('/')
def landing():
    return render_template('landing.html')

# 2) Upload Page
@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# 3) Analyze 
@app.route('/analyze', methods=['POST'])
def analyze():
    
    # When user submits the form, Flask creates dictionary called request.files
    # Each <input type="file" name="..."> becomes a key in request.files
    if 'audio_file' not in request.files:
        return "No file uploaded", 400
        
    file = request.files['audio_file']
    if file.filename == '':
        return "No selected file", 400

    # Save uploaded file
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # ("static/uploads", "raven_call.mp3") -> "static/uploads/raven_call.mp3"
    file.save(filepath)

    # Generate spectrogram from uploaded audio
    spec = generate_mel_spectrogram(filepath)

    # Save spectrogram image
    bird_name = "uploaded_call"
    plot_spectrogram(spec, bird_name)

    # TODO: Pass reference_specs ***
    # Added: from ranker.ranker import reference_specs
    results = compare_to_references(spec, reference_specs)

    return render_template(
        'results.html',
        # *** needs plot_spectogram to save file to static/uploads/
        spectrogram_image=f"uploads/{bird_name}_spectrogram.png",
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

if __name__ == '__main__':
    app.run(debug=True)