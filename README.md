# PostureAI

PostureAI is a simple Streamlit web app that analyzes a user-uploaded front-view or side-view image and provides a basic posture screening. It uses MediaPipe pose estimation to detect key body landmarks and highlights possible posture patterns such as uneven shoulders, uneven hips, forward head posture, and rounded shoulders.

## Features

- Upload a JPG or PNG image
- Choose between front-view and side-view posture analysis
- Detect body landmarks with MediaPipe
- Display an annotated pose overlay
- Show posture screening findings with simple explanations and exercise suggestions
- Include a warning that the app is not a medical diagnosis tool

## Project structure

- app.py — Streamlit app entry point
- pose_detector.py — MediaPipe pose detection and landmark drawing
- posture_analysis.py — Basic posture analysis logic
- reccomendations.py — Exercise and stretch suggestions
- utils.py — Image preprocessing helpers
- models/pose_landmarker.task — MediaPipe pose model file
- requirements.txt — Python dependencies
- run.sh — Helper script to run the app

## Requirements

- Python 3.9+
- A local environment with the dependencies from requirements.txt

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd postureAI
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Make sure the MediaPipe model file is present:
   ```bash
   ls models/pose_landmarker.task
   ```

## Running the app

You can run the app with Streamlit directly:

```bash
streamlit run app.py
```

Or use the included helper script:

```bash
./run.sh
```

Then open the local URL shown in the terminal, typically:

```text
http://localhost:8501
```

## Usage

1. Open the app in your browser.
2. Upload a clear full-body image.
3. Select whether the image is a front view or side view.
4. Review the detected pose and the posture screening results.

## Notes

This project provides a lightweight screening tool for educational or personal use. It is not intended to replace professional medical advice. If you experience pain, injury, numbness, or other concerning symptoms, consult a doctor or physical therapist.
