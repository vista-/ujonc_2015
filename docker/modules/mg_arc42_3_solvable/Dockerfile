FROM docker-registry.avatao.com:5000/base

MAINTAINER Gábor Molnár <gabor@molnar.es>

RUN apt-get update -yq && apt-get install -yq libc6-i386 socat

ADD arc42_v3 /
RUN touch /etc/arc42_license

CMD cd / && socat TCP4-LISTEN:8888,fork,rcvbuf=1,reuseaddr EXEC:"./arc42_v3 I_DONT_ALWAYS_PRINTF_BUT_WHEN_I_DO_I_PRINTF_PERCENT_N",stderr

EXPOSE 8888
