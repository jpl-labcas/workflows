ARG python_version=3.9
FROM python:${python_version}-bullseye

# TODO remove when package is deployed on pypi
#RUN apt update; apt install -y git

# required for scikit-image
#RUN apk add --no-cache build-base python3-dev py3-pip

WORKDIR /app

# TODO install from pypi when ready
RUN git clone https://github.com/jpl-labcas/workflows.git; cd workflows; pip install .


EXPOSE 8786/tcp
EXPOSE 8787

ENTRYPOINT ["dask"]
CMD ["scheduler"]










