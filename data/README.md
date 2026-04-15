# Changelog for Latest Push (4/13)
- Expanded dataset size to 8 reference files per bird
- Added "background noise" class using audio clipped from reference samples
- Retrained model and adjusted several parameters. When testing, please test classifier FIRST, as running the nn_trainer will overwrite model data and may cause incorrect matches
- Changed a few directory names for clarity when integrating into the app
- Moved unused files into "unused" directory
- Changed bird list to birds the model had a better time differentiating
- Added code change recommendations below. I do not want to cause a merge conflict, so I am putting them here to be pasted in after Bri's request is merged

# Code Change Recommendations

### Compare this to app.py and ensure it does not conflict with Bri's changes

```
from flask import Flask, render_template, request, redirect, url_for
import os

from dataset_builder import generate_spec_numpy

from spectrogram_generator import generate_mel_spectrogram, plot_spectrogram

import classifier

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

    # more elaborate analyze steps to agree with model and filesave structure
    # Calls new classifier model instead of similarity_ranker
    results = classifier.identify_bird(filepath)
    bird_name = results[0]["bird"]
    
    spec_array = generate_mel_spectrogram(filepath)
    spec_filename = f"{bird_name}_spectrogram.png"
    spec_save_path = os.path.join(app.config['UPLOAD_FOLDER'], spec_filename)
    plot_spectrogram(spec_array, save_path=spec_save_path, bird_name=bird_name)

    return render_template(
        'results.html',
        # *** needs plot_spectogram to save file to static/uploads/ <- COMPLETE
        spectrogram_image=f"uploads/{bird_name}_spectrogram.png",
        results = results
    )

# 4) Bird Details Page
@app.route('/bird/<bird_name>')
def bird_details(bird_name):
    # TODO: Replace with SQL lookup ***
    bird_data = {
        "name": bird_name,
        "description": "Placeholder description.",
        "image": f"birds/{bird_name}.png",
        "audio": f"birds/{bird_name}.mp3",
        "reference_spec": f"birds/{bird_name}_spectrogram.png"
    }

    return render_template('bird_details.html', bird=bird_data)
    
# 5) About Page
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

```

### Small change to Bri's spectrogram_generator to agree with above code

Add a variable to call, so signature is this 

def plot_spectrogram(S_db, save_path="spectrogram.png", bird_name="Unknown Bird"):

under the comment "Save as a PNG for the UI to display later" change to this

    plt.savefig(save_path)
    plt.close()



---

# Guide to the New Folders and Files (3/27)
---
### This commit has quite a lot of new stuff in it. Key new features include:
- birdTrapper shell script showcased in our Week 8 Sprint. Use this to gather more samples from xeno-canto.org
- trapped_birds_nest directory, which is the default destination for scraped audio files
- Additional source files added to reference and test to practice and train on
- NeuralNetwork, model, and spectrograms directories, all used in the new offline pipeline

As we discussed in Sprint 8, the new pipline is split into two separate streams: offline and online 

offline: dataset_builder(used on reference files) -> nn_trainer(to generate traing arrays) -> populate model dir \
online: user input(via UI) -> classifier (one-time generation of input spec saved to memory only) -> compare against trained data -> output confidence level and SQL query for highest match bird data

---
### birdTrapper.sh
- Run this shellscript with the format $ bash birdTrapper.sh https://xeno-canto.org/[page_code]
- It will scrape and dump the .mp3 file from the specified page to the nest directory
- It will name the .mp3 dump with the format Bird_Name-Species_name(entrycode).mp3 to retain cited source info and bird details. This info can be used in SQL queries

### spectrograms directory
- This directory has been populated with numpy arrays that have been generated via the new combination program dataset_builder, which bundles functions from Bri and Peyton's scripts
- the .npy binaries can now be sourced as reference files for the new classifier program

### model directory
- destination of the trained model (bird_nn.npy) and the bird labels (labels.npy) for use in the classifier program and future training

### NeuralNetwork
- The big one! Following a tutorial found at https://pyimagesearch.com/2021/05/06/backpropagation-from-scratch-with-python/, I built a standard backpropagation model to be used in the offline pipeline
- nn_original_comments.py is the untouched version from the tutorial, with modified comments from me so that it is easier to follow the math
- nn.py is used in the offline pipeline. It has an added @classmethod so it can load saved training data for future training, and comments have been removed for easier adaptation
- dataset_builder.py is a combination of Bri's generate_mel_spectrogram function and Peyton's normalize function, so that spectrogram arrays can be generated, normalized, and saved offline. It includes a loop function for one-and-done
- nn_trainer.py is the entry point of the offline pipline. Use this to call the .fit() function from the NeuralNetwork class to generate two trained binaries, saved in the model directory
- classifier.py is a prototype to replace similarity_ranker as the main program for UI output. Structure is nearly identical to similarity_ranker, with the main differences being:
  - it loads the trained model for a one-to-many confidence comparison, rather than a one-time correlation score
  - identify_bird() calls nn.predict() rather than scipy.correlate()
  - it also flattens and crops the spectrogram in one function, padding misaligned inputs with zeros, rather than cropping shape. This ideally avoids data loss (this should probably be hoisted into the dataset_builder)
  - return printout provides confidence scores rather than ranked scores. Results from first train are inaccurate.
- ranker_rewrite was my first attempt at optimizing similarity_ranker by relying on pre-generated spectogram arrays. Included here for process preservation, and is not used

---
# Next Steps
- As it stands, the basic neural network implementation is not efficient for one-to-many comparisons.
- The original implementation uses a linear regression model, but we have multiple possibilities. This math needs to be refactored
- Sigmoid activation can get easily overwhelmed with several cases. Again, linear regression is not a good fit (pun intended)
- The error rate is MSE (mean squared error), so it has the same problem as sigmoid. Convolutional logic needs to be looked into.
- On the first train, error rate plateaued at about 0.7, which indicates poor optimization and ill-fitting math.



Note: you may need to move these files into the top of the directory in order to experiment with them. I am still not very good with PATH finding variables, and trying the sys function that Peyton wrote has not worked for me.