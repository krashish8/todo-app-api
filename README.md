# Todo App API Setup

## Setting up the project

- Make sure `python` and `pip` are installed. Install [pyenv](https://github.com/pyenv/pyenv#installation) and [poetry](https://python-poetry.org/docs/#installation)
- Install python version 3.7.10 using `pyenv install 3.7.10`
- Activate python version using `pyenv local` inside the directory
- To activate this project's virtualenv, run `poetry shell` and then `poetry install` to install dependencies.
- Run `python manage.py migrate` to apply migrations.
- Start the development server using `python manage.py runserver`

## Deployment on Render

- build command: `pip install -r requirements.txt && python3 manage.py migrate`
- deploy command: `gunicorn todo.wsgi`
- Add environment variable `DATABASE_URL` for a hosted postgres database.

## Creating Superuser for production

- enter the virtualenv using `poetry shell`
- export the production database URL as in render using `export DATABASE_URL="<POSTGRES_URL">`
- apply migrations on database by `python3 manage.py migrate`
- create superuser now using `python3 manage.py createsuperuser`
