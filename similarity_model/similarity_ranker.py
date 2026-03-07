"""
Bird Call Similarity Ranker
Sprint 2: Peyton Cunningham

Pipeline:
    [Dataset (Jake)] > [Spectrograms (Brie)] > [THIS MODULE] > [UI (Stephen)]
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # adds project root to path so all modules are found

import numpy as np
from scipy.signal import correlate
from spectrogram.spectrogram_generator import generate_mel_spectrogram           # Brie's function


# PATHS

REFERENCE_DIR = "data/reference"    # one subfolder per bird, each with 3 reference recordings
TEST_DIR      = "data/test"         # one subfolder per bird, each with 1 test recording


# LOAD FILES

def get_reference_files():
    """Scan data/reference/ and return all audio files grouped by bird."""
    files = {}
    for bird in sorted(os.listdir(REFERENCE_DIR)):                              # loop through each bird folder
        path = os.path.join(REFERENCE_DIR, bird)
        if not os.path.isdir(path):                                             # skip loose files
            continue
        audio = [os.path.join(path, f) for f in sorted(os.listdir(path))
                 if f.endswith(".mp3") or f.endswith(".wav")]                   # only grab audio files
        if audio:
            files[bird] = audio
    return files


def get_test_files():
    """Scan data/test/ and return one test file per bird."""
    files = {}
    for bird in sorted(os.listdir(TEST_DIR)):                                   # loop through each bird folder
        path = os.path.join(TEST_DIR, bird)
        if not os.path.isdir(path):                                             # skip loose files
            continue
        audio = [os.path.join(path, f) for f in sorted(os.listdir(path))
                 if f.endswith(".mp3") or f.endswith(".wav")]
        if audio:
            files[bird] = audio[0]                                              # only one test file per bird
    return files


# COMPARISON

def normalize(spec):
    """Scale spectrogram values to 0 to 1 so volume does not affect the score."""
    min_val, max_val = spec.min(), spec.max()
    if max_val == min_val:
        return np.zeros_like(spec, dtype = float)                               # flat recording, return zeros
    return (spec - min_val) / (max_val - min_val)


def crop_to_match(a, b):
    """Crop both spectrograms to the same shape before comparing."""
    rows = min(a.shape[0], b.shape[0])
    cols = min(a.shape[1], b.shape[1])
    return a[:rows, :cols], b[:rows, :cols]


def score(input_spec, reference_spec):
    """Return a similarity score between two spectrograms using cross correlation."""
    a, b = normalize(input_spec), normalize(reference_spec)
    a, b = crop_to_match(a, b)
    correlation = correlate(a.flatten(), b.flatten(), mode = "valid")           # slide signals over each other and measure overlap
    return float(np.max(correlation))                                           # peak overlap is the similarity score


def rank_birds(input_spec, reference_files):
    """Score input against all reference birds and return ranked results."""
    scores = {}
    for bird, ref_paths in reference_files.items():
        bird_scores = [score(input_spec, generate_mel_spectrogram(p)) for p in ref_paths]  # score against all 3 references
        scores[bird] = sum(bird_scores) / len(bird_scores)                      # average the 3 scores for this bird

    ranked = sorted(scores.items(), key = lambda x: x[1], reverse = True)      # sort highest score first
    return [{"rank": i + 1, "bird": bird, "score": round(s, 4)} for i, (bird, s) in enumerate(ranked)]


def compare_to_references(input_spectrogram, reference_files):
    """Main entry point for Stephen's UI."""
    if not isinstance(input_spectrogram, np.ndarray):
        raise TypeError("input_spectrogram must be a numpy array")
    if input_spectrogram.ndim != 2:
        raise ValueError(f"Expected 2D array, got shape {input_spectrogram.shape}")
    if len(reference_files) == 0:
        raise ValueError("reference_files is empty")
    return rank_birds(input_spectrogram, reference_files)


# RUN

if __name__ == "__main__":
    reference_files = get_reference_files()                                     # load all reference birds from data/reference/
    test_files      = get_test_files()                                          # load all test birds from data/test/

    print(f"\n[PIPELINE] Testing {len(test_files)} birds against {len(reference_files)} references\n")

    for test_bird, test_path in test_files.items():                             # loop through every test bird
        test_spec = generate_mel_spectrogram(test_path)                         # convert test audio to spectrogram
        results   = compare_to_references(test_spec, reference_files)           # rank against all references
        top_match = results[0]["bird"]
        correct   = "CORRECT" if top_match == test_bird else "WRONG"

        print(f"  Tested: {test_bird:<30} Top match: {top_match:<30} [{correct}]")
        for entry in results:
            print(f"    #{entry['rank']}  {entry['bird']:<30} score: {entry['score']}")
        print()