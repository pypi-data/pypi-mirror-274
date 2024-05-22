[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- REPLACE -->


<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/">
        <img src="images/logo.png" alt="Logo" width="80" height="80">
    </a>
    <h3 align="center">Quiz Engine for Trivia</h3>
    <p align="center">
    <!-- PROJECT DESCRIPTION -->
    <br />
    <br />
    <!-- PROJECT SCREENSHOTS -->
    <!--
    <a href="https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/blob/main/images/screenshot01.png">
        <img src="images/screenshot01.png" alt="screenshot" width="120" height="120">
    </a>
    -->
    <br />
    <a href="https://github.com/TirsvadCLI/Python.QuizEngine4Trivia"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>

  </p>
</div>

# Quiz Engine for Trivia

<!-- PROJECT DESCRIPTION -->

# Getting Started

Quiz Engine for Trivia module

Easy to create a quiz game by using this module.

## Prerequisites

You have python 3 installed.

## Use

In a terminal do following
```commandline
pip install tirsvadCLI-quiz_engine_4_trivia
```

```python
from main import QuizEngine

quiz = QuizEngine()

while quiz.still_has_questions():
    print(f"Your score : {quiz.score}")
    q_text = quiz.next_question()
    user_answer = input(f"Q.{quiz.question_number}: {q_text}")
    if quiz.check_answer(user_answer):
        print("You are right")
    else:
        print("You are wrong")
```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project

<ol>
    <li>Fork the Project</li>
    <li>Create your Feature Branch</li>
    <li>Commit your Changes</li>
    <li>Push to the Branch</li>
    <li>Open a Pull Request</li>
</ol>

Example

```commandline
git checkout -b feature
git commit -m 'Add my feature enhance to project'
git push origin feature
```

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/TirsvadCLI/Python.QuizEngine4Trivia?style=for-the-badge

[contributors-url]: https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/TirsvadCLI/Python.QuizEngine4Trivia?style=for-the-badge

[forks-url]: https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/network/members

[stars-shield]: https://img.shields.io/github/stars/TirsvadCLI/Python.QuizEngine4Trivia?style=for-the-badge

[stars-url]: https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/stargazers

[issues-shield]: https://img.shields.io/github/issues/TirsvadCLI/Python.QuizEngine4Trivia?style=for-the-badge

[issues-url]: https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/issues

[license-shield]: https://img.shields.io/github/license/TirsvadCLI/Python.QuizEngine4Trivia?style=for-the-badge

[license-url]: https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/blob/master/LICENSE

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin-url]: https://www.linkedin.com/in/jens-tirsvad-nielsen-13b795b9/
