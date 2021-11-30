FROM python:3.9

WORKDIR /code
RUN pip install --upgrade pip
RUN pip install pipenv
RUN pip install pipenv-to-requirements
COPY Pipfile* /code
RUN pipenv run pipenv_to_requirements -f
RUN pip install -r requirements.txt
COPY . /code/
