FROM python:3.11-alpine

# TODO remove when package is deployed on pypi
RUN apk update; apk add --no-cache git

# required for scikit-image
RUN apk add --no-cache build-base python3-dev py3-pip

WORKDIR /app

# TODO install from pypi when ready
RUN git clone https://github.com/jpl-labcas/workflows.git; cd workflows; pip install .









