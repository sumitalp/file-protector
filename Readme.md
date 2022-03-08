Assignment
====================

## Author

__Ahsanuzzaman Khan__

## Project Description
You need to create a simple application which:

1. File or URL can be protected.
2. System should generate short-url and password after uploading.
3. File or URL should be password protected.


## Requirements
- Python 3.9
- PostgreSQL
- Django
- Django REST Framework
- Faker
- Docker
- Celery
- Redis

## Developer requirements
- Factory Boy
- Pytest Django

## Installation
- Install `docker`
- Download this git repo
- Then go to project directory
- And run `make setup`

## To Run project
Go to project folder and run 
- `make runserver`

## Test project
Go to project folder and run 
- `make test`

## Project urls
- For apis: `http://localhost:8100/`

## Report url
- URL shows last 7 days data (if GET parameters not provided): `http://localhost:8100/report/`
- URL shows date range data (if GET parameters provided): `http://localhost:8100/report/?start_date=2022-03-01&end_date=2022-03-03`

## Live URL
- `https://file-protector.herokuapp.com/`


## Improvements
- Full testcases can't be covered but functionalities are completed.
