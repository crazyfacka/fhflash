# fhflash
Automatically book gym classes for a specific gym.

## Requirements
You'll need:
* Python >=3.7

## Build
Hopefully you're using [Pipenv](https://pypi.org/project/pipenv/) to manage your dependencies.

```bash
$ pipenv install # Installs all dependencies for the project
$ cp sample.db storage.db # Rename the preconfigured sqlite3 DB to support the application
$ cp sample_confs.json confs.json # Rename the sample configuration file and fill missing data
```

## Run
Recommendation is to put this on a cronjob.

```bash
$ pipenv run python scripts/book_class.py
```
