import requests

from QuizEngine4Trivia.Models.trivia_api_model import TriviaApiModel


class TriviaDataModel:
    data: list[dict] = []

    def __init__(self, trivia_api: TriviaApiModel):
        """
        Trivia data model. Holds all the requested data from the key ['results'] in TriviaDataModel.data field

        :param trivia_api: An TriviaApiModel
        """
        response = requests.get(url=trivia_api.url, params=trivia_api.url_params)
        response.raise_for_status()
        self.data = response.json()['results']
