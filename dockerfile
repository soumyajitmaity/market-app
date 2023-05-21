FROM python:3.10.6
RUN pip install pipenv
WORKDIR /app
COPY ./requirements/Pipfile ./requirements/Pipfile.lock /app/
RUN pipenv install --system --deploy
COPY ./src /app
CMD ["python3", "-m", "flask", "run", "--host","0.0.0.0"]