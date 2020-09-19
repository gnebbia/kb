FROM python:3

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt && \
    python setup.py install && \
    cat /app/docker/aliases >> ~/.bashrc

WORKDIR /data
