FROM python:3.9-buster

RUN apt-get update \
    && apt-get -y install ffmpeg libsm6 libxext6 \
    && apt-get -y install tesseract-ocr tesseract-ocr-deu

RUN pip install --upgrade pip

ADD ./requirements.txt /puzzle-solver-api/requirements.txt

WORKDIR /puzzle-solver-api

RUN pip install -r requirements.txt

COPY src ./src

EXPOSE 5001

CMD python ./src/server.py -p