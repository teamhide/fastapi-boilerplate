FROM python:3.8.2
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

ENTRYPOINT ["dockerize", "-wait", "tcp://db:3306", "-timeout", "20s"]

CMD ["python3", "main.py"]