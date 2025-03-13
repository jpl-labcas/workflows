ARG python_version=3.9
FROM python:${python_version}-bullseye

WORKDIR /app

# TODO install from pypi when ready
RUN git clone https://github.com/jpl-labcas/workflows.git; cd workflows; pip install '.[ml_worker]'
# For the dashboard to run
RUN pip install "bokeh!=3.0.*,>=2.4.2"


EXPOSE 8786/tcp
EXPOSE 8787

ENTRYPOINT ["dask"]
CMD ["scheduler"]










