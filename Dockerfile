FROM python:3.9-buster

RUN pip install --upgrade pip

ADD ./requirements.txt /puzzle-solver-api/requirements.txt

WORKDIR /puzzle-solver-api

RUN pip install -r requirements.txt

COPY . /puzzle-solver-api

EXPOSE 5001

CMD python ./src/server.py