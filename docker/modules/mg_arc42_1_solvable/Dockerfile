FROM docker-registry.avatao.com:5000/base

MAINTAINER Gábor Molnár <gabor@molnar.es>

RUN apt-get update -yq && apt-get install -yq libc6-i386

ADD server.py /
ADD arc42_v1 /

CMD cd / && python server.py

EXPOSE 8888
