## Timestamp Microservice Project


Project for studies purpose based on the freeCodeCamp Timestamp Microservice Project.

### Built With
- Python (version 3.10.9)
    - Flask
    - TDD

### Installation

1. Clone the repo
```sh
git clone https://github.com/XXX
```

2. Install requirements
```sh
pip install -r requirements
```

3. Set environment variable
```sh
export CONFIGURATION_SETUP="config.DevelopmentConfig"
```

### Usage
- Go to project folder
`python app.py` or `flask run`

### API Endpoints
| HTTP Verb | Endpoint | Action |
| --- | --- | --- |
| GET | /api/:date |  Converts date to a unix timestamp|
| GET | /api/:timestamp |  Converts unix timestamp to date|
| GET | /api/: | Empty param return current time |