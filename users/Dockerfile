FROM python:3.6

ENV HOME /opt/sanic_test
RUN mkdir $HOME
WORKDIR $HOME

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .