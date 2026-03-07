from flask import Flask, render_template, request, redirect, url_for
import os

from spectrogram.spectrogram_generator import generate_mel_spectrogram, plot_spectrogram
from ranker.ranker import compare_to_references, generate_mock_spectrogram

app = Flask(__name__)
# Configure uploads folder:
app.config['UPLOAD_FOLDER'] = 'static/uploads'

@app.route('/')
def index():
    return render_template('index.html')

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

    # Run ranker from Peyton's function
    results = compare_to_references(spec, reference_specs)

    return render_template(
        'results.html',
        spectrogram_image=f"uploads/{bird_name}_spectrogram.png",
        results=results

if __name__ == '__main__':
    app.run(debug=True)