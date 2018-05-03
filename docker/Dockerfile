FROM ubuntu:16.04
MAINTAINER astepenko@aqueti.com

RUN apt-get update
RUN apt-get -y install apt-transport-https duplicity python-pip avahi-utils avahi-daemon libnss-mdns systemd rsyslog apt-utils sudo vim ssh python3-pip fabric libavahi-common-dev libavahi-client-dev net-tools lsof iputils-*

RUN adduser --quiet --disabled-password --shell /bin/bash --home /home/mosaic --gecos "User" mosaic

RUN usermod -aG sudo,root mosaic

RUN echo "mosaic:DARPAaware" | chpasswd

RUN echo 'mosaic ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir /tmp/install

COPY install /tmp/install

WORKDIR /tmp/install

RUN dpkg -i AquetiAPI-linux64.deb

RUN tar -xzf homunculus.tar.gz

RUN cp setup.sh Homunculus

WORKDIR /tmp/install/Homunculus

RUN sh setup.sh

EXPOSE 5004

CMD ["/usr/bin/supervisord", "-n"]
