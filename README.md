# Final Project - Emotion Detector

This repository contains the Final Project submission for the Emotion Detector application.

Emotion Detector is a Flask-based web application that uses the Watson NLP
EmotionPredict endpoint to infer emotions from user-provided text.

## Project Structure

- `EmotionDetection/`: package for emotion detection logic
- `server.py`: Flask web app deployment
- `test_emotion_detection.py`: unit tests

## Setup

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
pytest -q
```

## Run Static Analysis

```bash
pylint server.py
```

## Run App

```bash
python server.py
```
