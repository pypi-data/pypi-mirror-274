from setuptools import setup, find_packages

with open(file="README.md", mode="r") as f:
    description = f.read()

setup(
    name='tirsvadCLI-quiz-engine-4-trivia',
    version='0.0.4',
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/TirsvadCLI",
    download_url='https://github.com/TirsvadCLI/Python.QuizEngine4Trivia/releases/download/v0.0.1a2/tirsvadcli_quiz_engine_4_trivia-0.0.1a2.tar.gz',
    author="Jens Tirsvad Nielsen",
    author_email="jenstirsvad@gmail.com",

    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires='>=3.10',
    install_requires=[
        'requests'
    ],
)
