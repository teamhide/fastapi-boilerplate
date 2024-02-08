FROM --platform=$BUILDPLATFORM python:3.11 as builer

ENV PYTHONFAULTHANDLER=1
RUN apt update \
    && apt install -y build-essential curl \
    && apt install -y curl wget \
    && apt install -y pkg-config \
    && apt install -y libcurl4-openssl-dev \
    && apt install -y libssl-dev \
    && apt install -y supervisor\
    && apt-get install -y lsb-release inetutils-tools


WORKDIR /app
COPY pyproject.toml /app
COPY poetry.lock /app
COPY install.sh /app
RUN bash ./install.sh

#
COPY . /app

RUN chmod +x .docker/entrypoint.sh
ENTRYPOINT [".docker/entrypoint.sh"]