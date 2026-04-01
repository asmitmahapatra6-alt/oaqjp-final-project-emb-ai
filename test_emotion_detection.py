"""Unit tests for the EmotionDetection package."""

from unittest.mock import patch

from EmotionDetection import emotion_detector


def _mock_response_for(label: str):
    """Build a mocked Watson API response for a dominant emotion label."""
    emotions = {
        "anger": 0.01,
        "disgust": 0.01,
        "fear": 0.01,
        "joy": 0.01,
        "sadness": 0.01,
    }
    emotions[label] = 0.95

    class MockResponse:  # pylint: disable=too-few-public-methods
        """Simple response stub with the JSON payload used by emotion_detector."""

        status_code = 200

        @staticmethod
        def json():
            return {"emotionPredictions": [{"emotion": emotions}]}

        @staticmethod
        def raise_for_status():
            return None

    return MockResponse()


def test_emotion_anger() -> None:
    """Emotion detector returns anger for anger-focused text."""
    with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
        mock_post.return_value = _mock_response_for("anger")
        response = emotion_detector("I am mad and furious right now.")
    assert response["dominant_emotion"] == "anger"


def test_emotion_disgust() -> None:
    """Emotion detector returns disgust for disgust-focused text."""
    with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
        mock_post.return_value = _mock_response_for("disgust")
        response = emotion_detector("This spoiled food makes me feel sick and disgusted.")
    assert response["dominant_emotion"] == "disgust"


def test_emotion_fear() -> None:
    """Emotion detector returns fear for fear-focused text."""
    with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
        mock_post.return_value = _mock_response_for("fear")
        response = emotion_detector("I am afraid I might fail the exam tomorrow.")
    assert response["dominant_emotion"] == "fear"


def test_emotion_joy() -> None:
    """Emotion detector returns joy for joy-focused text."""
    with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
        mock_post.return_value = _mock_response_for("joy")
        response = emotion_detector("I am so happy and delighted with my result!")
    assert response["dominant_emotion"] == "joy"


def test_emotion_sadness() -> None:
    """Emotion detector returns sadness for sadness-focused text."""
    with patch("EmotionDetection.emotion_detection.requests.post") as mock_post:
        mock_post.return_value = _mock_response_for("sadness")
        response = emotion_detector("I feel very sad and disappointed today.")
    assert response["dominant_emotion"] == "sadness"
