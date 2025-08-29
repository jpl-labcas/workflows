ARG python_version=3.11
FROM python:${python_version}-bullseye

WORKDIR /app

# TODO install from pypi when ready
RUN pip install 'labcas.workflow[ml_worker]==0.1.12'
# For the dashboard to run
RUN pip install "bokeh!=3.0.*,>=2.4.2"


EXPOSE 8786/tcp
EXPOSE 8787

ENTRYPOINT ["dask"]
CMD ["scheduler"]










