FROM docker-registry.avatao.com:5000/base
MAINTAINER Gábor Molnár, Dániel Bali

WORKDIR /home/user/

RUN apt-get -qqy update && \
    apt-get -qqy install libc6-i386

ADD flag.txt /home/user/
ADD vmmigration /home/user/vmmigration
RUN chown user vmmigration
RUN chgrp user vmmigration

ADD start.sh /start.sh
CMD /start.sh

EXPOSE 8888
