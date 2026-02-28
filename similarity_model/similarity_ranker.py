"""
Bird Call Similarity Ranker
Sprint 1: Peyton Cunningham

Pipeline:
    [Dataset (Jake)] > [Spectrograms (Brie)] > [THIS MODULE] > [UI (Stephen)]

What this does:
    Takes an input spectrogram and compares it against 5 reference spectrograms.
    Returns a ranked list of birds ordered from most to least similar.

Dependencies:
    numpy
    scipy
"""

import numpy as np
from scipy.signal import correlate

# CORE FUNCTIONS

def normalize_spectrogram(spec):
    """Scale all values in a spectrogram to between 0 and 1."""

    min_val = spec.min()                                    # lowest value in array
    max_val = spec.max()                                    # highest value in array

    if max_val == min_val:                                  # flat or silent recording
        return np.zeros_like(spec, dtype = float)           # return all zeros to avoid divide by zero

    return (spec - min_val) / (max_val - min_val)           # shift and scale to 0 to 1


def resize_to_match(spec_a, spec_b):
    """Crop both spectrograms to the same shape before comparing."""

    min_rows = min(spec_a.shape[0], spec_b.shape[0])        # shorter height of the two
    min_cols = min(spec_a.shape[1], spec_b.shape[1])        # shorter width of the two

    return spec_a[:min_rows, :min_cols], spec_b[:min_rows, :min_cols]   # crop both to match


def cross_correlation_score(input_spec, reference_spec):
    """Return a similarity score between two spectrograms using cross correlation."""

    a = normalize_spectrogram(input_spec)                   # normalize input
    b = normalize_spectrogram(reference_spec)               # normalize reference

    a, b = resize_to_match(a, b)                            # make sure shapes match

    a_flat = a.flatten()                                    # collapse 2D to 1D for scipy
    b_flat = b.flatten()                                    # collapse 2D to 1D for scipy

    correlation = correlate(a_flat, b_flat, mode = "valid") # compare the two signals
    score = float(np.max(correlation))                      # peak value is the similarity score

    return score                                            # higher score means more similar

# RANKING (main function the rest of the pipeline calls)

def rank_birds(input_spec, reference_specs, method = "cross_correlation"):
    """
    Compare input spectrogram against all references and return ranked results.

    Arguments:
        input_spec:      2D numpy array, the recording to identify
        reference_specs: dict of {bird name: 2D numpy array}
        method:          scoring method, "cross_correlation"

    Returns:
        List of dicts sorted best match first:
        [{"rank": 1, "bird": "Robin", "score": 245.3}, ...]
    """

    scores = {}                                             # store scores for each bird

    for bird_name, ref_spec in reference_specs.items():     # loop through each reference bird
        scores[bird_name] = cross_correlation_score(input_spec, ref_spec)

    ranked = sorted(scores.items(), key = lambda x: x[1], reverse = True)  # sort highest score first

    results = [
        {"rank": i + 1, "bird": bird, "score": round(score, 4)}
        for i, (bird, score) in enumerate(ranked)          # build result dicts with rank numbers
    ]

    return results


def print_results(results, input_label = "Input"):
    """Print ranked results to console. Placeholder until Stephen's UI is ready."""

    print(f"\n{'=' * 45}")
    print(f"  Bird ID Results for: {input_label}")
    print(f"{'=' * 45}")

    for entry in results:
        print(f"  #{entry['rank']}  {entry['bird']:<25} score: {entry['score']}")  # one line per bird
    
    print(f"{'=' * 45}\n")

# INTEGRATION HOOK (what teammates import and call)

def compare_to_references(input_spectrogram, reference_spectrograms):
    """
    Main entry point for the pipeline. Stephen's UI and Brie's spectrogram module call this.

    Arguments:
        input_spectrogram:      2D numpy array from Brie's librosa module  <-- comes from Brie
        reference_spectrograms: dict of {bird name: 2D numpy array}        <-- comes from Jake and Brie

    Returns:
        Ranked list (see rank_birds return format above)
    """

    if not isinstance(input_spectrogram, np.ndarray):          # make sure input is the right type
        raise TypeError("input_spectrogram must be a numpy array")

    if input_spectrogram.ndim != 2:                            # spectrograms must be 2D
        raise ValueError(f"Expected 2D array, got shape {input_spectrogram.shape}")

    if len(reference_spectrograms) == 0:                       # nothing to compare against
        raise ValueError("reference_spectrograms dict is empty")

    return rank_birds(input_spectrogram, reference_spectrograms)

# TEMPORARY: mock data and demo (remove once Jake and Brie's modules are ready)

def generate_mock_spectrogram(seed = 0, shape = (128, 128)):
    """Generate a fake spectrogram for testing. Replace with real data from Jake and Brie."""

    rng = np.random.default_rng(seed)                      # seed makes output reproducible
    return rng.random(shape).astype(np.float32)            # random values shaped like a real spectrogram


def run_demo():
    """Run the ranker with fake data. For testing only, remove when real audio is available."""

    print("\n[DEMO] Using placeholder spectrograms. Replace with real data from Jake and Brie.\n")

    # PLACEHOLDER bird names below. Real names come from Jake's dataset.
    demo_birds = [
        "Bird A (placeholder)",
        "Bird B (placeholder)",
        "Bird C (placeholder)",
        "Bird D (placeholder)",
        "Bird E (placeholder)",
    ]

    reference_specs = {
        bird: generate_mock_spectrogram(seed = i)           # one fake spectrogram per bird
        for i, bird in enumerate(demo_birds)
    }

    test_input = generate_mock_spectrogram(seed = 0)        # seed 0 matches Bird A, should rank first

    results = rank_birds(test_input, reference_specs)       # run the ranker
    print_results(results, input_label = "Test Input")      # print output to console


if __name__ == "__main__":
    run_demo()                                              # runs demo when file is executed directly