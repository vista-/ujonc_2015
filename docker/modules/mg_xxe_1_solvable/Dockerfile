FROM docker-registry.avatao.com:5000/base

MAINTAINER Gábor Molnár <gabor@molnar.es>

RUN apt-get update && apt-get install -y python-lxml python-simplejson

RUN mkdir -p /app
ADD server.py /app/
ADD flag /app/

CMD cd /app && python server.py

EXPOSE 8888
