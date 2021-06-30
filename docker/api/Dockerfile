FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
MAINTAINER Hide <padocon@naver.com>

COPY . /home
WORKDIR /home
ENV ENV=development
RUN pip install pipenv mysqlclient
RUN pipenv install --system
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN chmod +x /home/docker/api/startup.sh
ENTRYPOINT /home/docker/api/startup.sh