# blackjack

A classic game on the command line, written in Python

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

[Python 3.7](https://www.python.org/downloads/release/python-370/)

### Installing

A step by step series of examples that tell you how to play the game.

Create and activate a Python3 virtual environment.

```
python3 -m venv venv
source venv/bin/activate
```

Install Python dependencies

```
pip install -r requirements.txt
```
## Running the tests

To run the unit tests
```
coverage run -m unittest discover tests -b
```

To see coverage report

```
coverage report
```

## Play the game

To start the game 

```
python blackjack/__init__.py
```

## Built With

* [Python 3.7](https://www.python.org/downloads/release/python-370/)


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

