FROM docker-registry.avatao.com:5000/base

MAINTAINER Gábor Molnár <gabor@molnar.es>

RUN apt-get update -yq && apt-get install -yq libc6-i386 socat

ADD arc42_v4 /

CMD cd / && socat TCP4-LISTEN:8888,fork,rcvbuf=1,reuseaddr EXEC:"./arc42_v4 PRINTF_EQUALS_SHELL",stderr

EXPOSE 8888
