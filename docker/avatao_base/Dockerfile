FROM ubuntu:14.04

# Set the locale
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install packages
RUN apt-get -qqy update && \
    apt-get -qqy dist-upgrade && \
    apt-get -qqy install \
        build-essential \
        vim \
        nano \
        openssh-server \
        screen \
        tmux \
        python-pip \
        python-flask \
        python3-pip \
        python3-flask \
        man-db \
        netcat \
        psmisc \
        git \
        npm \
        nodejs-legacy \
    && \
    apt-get clean

# Add "user" user
RUN adduser --disabled-password --gecos ",,," user

# Create directory needed by sshd
RUN mkdir -p /var/run/sshd

#Install codebox
WORKDIR /opt
RUN mkdir codebox && chown user codebox &&  sudo -u user git clone https://github.com/CodeboxIDE/codebox.git && cd codebox && sudo -u user git checkout 0.8.x
WORKDIR /opt/codebox
RUN npm install -g grunt-cli
RUN sudo -u user HOME=/home/user USER=user npm install
RUN sudo -u user HOME=/home/user USER=user /usr/local/bin/grunt build
RUN sudo -u user HOME=/home/user USER=user bin/codebox.js run -n @please_just_die_after_adding addons@ || echo 'Error is expected as we need it to terminate after adding plugins. This is dirty.'
RUN sudo -u user HOME=/home/user USER=user rm -R addons/cb.debug addons/cb.deploy addons/cb.git addons/cb.help addons/cb.offline addons/cb.panel.outline addons/cb.project
WORKDIR /

RUN touch /start.sh

# Add python libraries
ADD filemanager.py /usr/lib/python3/dist-packages/
