FROM conda/miniconda3:latest

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

ENV SHELL /bin/bash

# install setuptools before pipenv because pipenv installation crashed otherwise for some reason
RUN conda install -y -c conda-forge \
    setuptools \
    jupyterlab \
    matplotlib && \
    pip install pipenv

WORKDIR /workspace
ADD Pipfile Pipfile.lock ./
RUN pipenv install --dev

ADD test_images ./test_images/
ADD pytest.ini .
ADD tests ./tests
ADD white_brush ./white_brush/

EXPOSE 8888
CMD ["jupyter", "lab", "--ip='*'", "--no-browser", "--NotebookApp.token=''",  "--notebook-dir=/workspace", "--allow-root"]