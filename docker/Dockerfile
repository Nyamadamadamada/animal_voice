FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./app /code/app

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
