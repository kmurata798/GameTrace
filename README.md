# GameTrace Website Link (Heroku app):  https://gametrace.herokuapp.com
![GameTrace image](/images/GameTrace-Thumbnail.jpg)

### Need to make changes to database to postgre ==> heroku keeps reseting database


## Description

GameTrace gives users the ability to keep track of his/her in-game achievements, trophies, gameplay, etc when they are away from home base (their preferred gaming system). The current state of the project is an MVP, in which additional changes are being planned for implementation.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [Deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

All dependencies are listed in the requirements.txt file in the repository.

### Installing

Clone this repository (Don't include the $. This symbol indicates that you need to write this command in the commandline in this repository):

```
$ git clone https://github.com/kmurata798/GameTrace.git
```

Traverse into the this repository:

```
$ cd /path/to/file/GameTrace
```

Run virtual environment which carries all the dependencies needed for this program:

```
$ source venv/bin/activate
```

Run the server in development mode:

```
$ export FLASK_ENV=development
$ python3 run.py
```

Example of Running server:
![example of development server](images/GameTrace-installment.png)

## Deployment
Clone this repository and follow the instructions provided at this link [Heroku deployment](https://devcenter.heroku.com/articles/git)

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [Heroku](https://www.heroku.com) - Deployment

## Authors

* **Kento Murata** - *Initial work* - [kmurata798](https://github.com/kmurata798)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
