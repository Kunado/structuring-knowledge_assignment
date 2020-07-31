# Structuring-Knowledge_Assignment

## Requirements
* Poetry
* Docker and Docker Compose

## Set up
### Install dependent packages
```
$ poetry install
```

### Download data and model
```
$ ./setup.sh
```

### Build Docker image
```
$ docker-compose build
```

### Importing data into ElasticSearch
```
$ docker-compose up
$ poetry run data_import.py
```

