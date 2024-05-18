import numpy as np

from classification_model.predict import make_prediction
from sklearn.metrics import accuracy_score


def test_make_prediction(sample_input_data):
    """
    The argument sample_input_data is a fixture from conftest.py,
    where the return value of sample_input_data is test_data 
    i.e., treat sample_input_data logically as test_data.
    """
    # Given
    expected_no_predictions = 179

    # When
    result = make_prediction(input_data=sample_input_data)

    # Then
    predictions = result.get("predictions")
    assert isinstance(predictions, np.ndarray)
    assert isinstance(predictions[0], np.int64)
    assert result.get("errors") is None
    assert len(predictions) == expected_no_predictions

    y_test = sample_input_data["Survived"]
    accuracy = accuracy_score(y_test, predictions)

    assert accuracy > 0.75
