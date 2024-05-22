class TriviaApiModel:
    trivia_dict: dict = {}
    # trivia_encode: str | None  # Not in use
    trivia_difficulty_dict = {
        "Any Difficulty": None,
        'easy': 'easy',
        'medium': 'medium',
        'hard': 'hard'
    }
    trivia_category_dict = {
        "Any Category": None,
        "General Knowledge": 9,
        "Entertainment: Books": 10,
        "Entertainment: Film": 11,
        "Entertainment: Music": 12,
        "Entertainment: Musicals & Theatres": 13,
        "Entertainment: Television": 14,
        "Entertainment: Video Games": 15,
        "Entertainment: Board Games": 16,
        "Science & Nature": 17,
        "Science: Computers": 18,
        "Science: Mathematics": 19,
        "Mythology": 20,
        "Sports": 21,
        "Geography": 22,
        "History": 23,
        "Politics": 24,
        "Art": 25,
        "Celebrities": 26,
        "Animals": 27,
        "Vehicles": 28,
        "Entertainment: Comics": 29,
        "Science: Gadgets": 30,
        "Entertainment: Japanese Anime & Manga": 31,
        "Entertainment: Cartoon & Animations": 32
    }
    trivia_type_dict = {
        "Any type": None,
        "Multiple choices": "multiple",
        "True / False": "boolean",
    }
    trivia_encode_dict = {
        "Default Encoding": None,
        "Legacy URL Encoding": "urlLegacy",
        "URL Encoding (RFC 3986)": "url3986",
        "Base64 Encoding": "base64"
    }

    url: str = "https://opentdb.com/api.php"
    url_params: dict = {}

    def __init__(
            self,
            trivia_amount: int = 10,
            trivia_difficulty: str | None = None,
            trivia_category: int | None = None,
            # trivia_type: str ='boolean',  # Not in use
            # encode=None # Not in use
    ) -> None:
        """

        :param trivia_amount:
        :param trivia_difficulty:
        :param trivia_category:
        """

        trivia_type = "boolean"

        # Validate params
        if trivia_difficulty is not None and trivia_difficulty not in self.trivia_difficulty_dict.values():
            raise ValueError(f"trivia_difficulty value is wrong")
        if trivia_category is not None and trivia_category not in self.trivia_category_dict.values():
            raise ValueError(f"trivia_category value is wrong")
        if trivia_type is not None and trivia_type not in self.trivia_type_dict.values():
            raise ValueError(f"trivia_type value is wrong")

        self.trivia_dict.update({'trivia_amount': trivia_amount})
        self.trivia_dict.update({'trivia_difficulty': trivia_difficulty})
        self.trivia_dict.update({'trivia_category': trivia_category})
        self.trivia_dict.update({'trivia_type': trivia_type})

        self._create_api_url()

    def _create_api_url(self) -> None:
        self.url_params = {}
        for k in self.trivia_dict.keys():
            if self.trivia_dict[k] is not None:
                key = k.split('_')[1]
                self.url_params.update({key: self.trivia_dict[k]})
