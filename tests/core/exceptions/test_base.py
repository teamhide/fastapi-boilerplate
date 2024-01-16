from core.exceptions import CustomException


def test_custom_exception():
    # Given
    message = "hide"

    # When
    exc = CustomException(message=message)

    # Then
    assert exc.message == message
