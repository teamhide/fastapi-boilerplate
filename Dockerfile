FROM python:3.8.2
MAINTAINER Hide <padocon@naver.com>

COPY . /home
WORKDIR /home
RUN pip install pipenv
RUN pipenv install --system
CMD ["python3", "main.py"]