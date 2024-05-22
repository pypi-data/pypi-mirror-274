import html

from Models.trivia_data_model import TriviaDataModel
from Models.trivia_api_model import TriviaApiModel


class QuizEngine:
    api: TriviaApiModel
    data: TriviaDataModel

    question_number: int = 0
    score: int = 0
    current_question: dict = {}


    def __init__(self) -> None:
        """
        QuestionEngine fetch question from trivia api
        """
        self.api = TriviaApiModel()
        self.trivial_data_model = TriviaDataModel(self.api)

    def still_has_questions(self):
        """
        Is there still more question in the deck
        :return boolean:
        """
        return self.question_number < len(self.trivial_data_model.data)

    def next_question(self) -> str:
        """
        Return the next question from deck
        :return str: question
        """
        self.current_question = self.trivial_data_model.data[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question['question'])
        return f"Q.{self.question_number}: {q_text}:"

    def check_answer(self, user_answer: str) -> bool:
        """
        Checking user answer 'true' | 'false'

        :param user_answer:
        :return boolean:
        """
        correct_answer = self.current_question['correct_answer']
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False
