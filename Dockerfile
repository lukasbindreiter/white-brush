FROM jjanzic/docker-python3-opencv:latest

RUN pip install \
    opencv-python \
    jupyterlab \
    numpy \
    matplotlib \
    scipy \
    sklearn

RUN pip install ipywidgets && jupyter nbextension enable --py widgetsnbextension

ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

ENV SHELL /bin/bash
WORKDIR /workspace
ENV PYTHONPATH="/workspace"

ADD . .

EXPOSE 8888
CMD ["jupyter", "lab", "--ip='*'", "--no-browser", "--NotebookApp.token=''",  "--notebook-dir=/workspace", "--allow-root"]
