FROM python:3.6

ENV http_proxy http://10.11.1.245:3128/
ENV https_proxy http://10.11.1.245:3128/
ENV HOME /opt/sanic_test
RUN mkdir $HOME
WORKDIR $HOME

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
