import requests
from .config import BASE_URL
from .exceptions import ModelNotFoundError, APIRequestError

class SentrifyAI:
    def __init__(self):
        pass

    def list_models(self):
        try:
            # Send a GET request to retrieve the list of models
            response = requests.get(f'{BASE_URL}models')
            response.raise_for_status()  # Raise an error for non-200 status codes
            return response.json()['models']  # Extract and return the list of models
        except requests.exceptions.RequestException as e:
            # Handle any request-related exceptions
            raise APIRequestError(f'Request exception occurred: {e}')

    def classify_message(self, model_slug, message):
        try:
            # Prepare parameters for the request
            params = {
                'model': model_slug,
                'message': message
            }
            # Send a GET request to classify the message
            response = requests.get(f'{BASE_URL}moderation', params=params)
            response.raise_for_status()  # Raise an error for non-200 status codes
            return response.json()  # Return the classification result
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors, including 404 (Model not found)
            if response.status_code == 404:
                raise ModelNotFoundError(f'Model {model_slug} not found.')
            else:
                raise APIRequestError(f'HTTP error occurred: {e}')
        except requests.exceptions.RequestException as e:
            # Handle any other request-related exceptions
            raise APIRequestError(f'Request exception occurred: {e}')
