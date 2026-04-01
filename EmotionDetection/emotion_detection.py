"""Core emotion detection logic using Watson NLP service."""

from __future__ import annotations

import requests

WATSON_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
WATSON_HEADERS = {
    "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
}


def emotion_detector(text_to_analyze: str) -> dict:
    """Analyze text and return all emotions with dominant emotion.

    Returns a dictionary with keys anger, disgust, fear, joy, sadness,
    and dominant_emotion. If Watson returns status code 400, all values
    are set to None as required by the project specification.
    """
    request_payload = {"raw_document": {"text": text_to_analyze}}
    try:
        response = requests.post(
            WATSON_URL,
            json=request_payload,
            headers=WATSON_HEADERS,
            timeout=10,
        )
    except requests.RequestException:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    if response.status_code == 400:
        return {
            "anger": None,
            "disgust": None,
            "fear": None,
            "joy": None,
            "sadness": None,
            "dominant_emotion": None,
        }

    response.raise_for_status()
    emotions = response.json()["emotionPredictions"][0]["emotion"]
    dominant_emotion = max(emotions, key=emotions.get)

    return {
        "anger": emotions.get("anger"),
        "disgust": emotions.get("disgust"),
        "fear": emotions.get("fear"),
        "joy": emotions.get("joy"),
        "sadness": emotions.get("sadness"),
        "dominant_emotion": dominant_emotion,
    }
