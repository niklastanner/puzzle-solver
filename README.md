# Puzzle Solver

Table of Contents
=================

- [Puzzle Solver](#puzzle-solver)
    - [About](#about)
    - [Prerequisites](#prerequisites)
    - [Running](#running)
    - [How it works](#how-it-works)

## About

This project is meant to provide a restful API for solving different kind of puzzles.

Currently implemented puzzles are:

- Sudoku

Planned to be implemented in the future:

- Binoxxo

## Prerequisites

- [Docker](https://www.docker.com/get-started/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)

## Running

Build the docker container using:\
`docker build -t puzzle-solver/api:latest`

Run it with:\
`docker run -it -p 5001:5001 --name puzzle-solver-api -d puzzle-solver/api:latest`

The API is now up and running. It is available at `localhost:5001`.
To solve a Sudoku for example upload an image using a `POST` request to `localhost:5001/sudoku`.
As Payload use Form Data and declare the key `image` with the corresponding image file.

## How it works

The API is provided using [Flask](https://flask.palletsprojects.com/en/2.1.x/)
and [Waitress](https://docs.pylonsproject.org/projects/waitress/en/latest/).
The image is being split into pieces using Hough Transformation.
These parts of the image are being scanned by Tesseract OCR.
To solve the Sudoku [OR-Tools](https://github.com/google/or-tools) is used.