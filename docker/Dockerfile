FROM ubuntu:16.04
MAINTAINER astepenko@aqueti.com

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get -y install apt-transport-https duplicity python-pip avahi-utils avahi-daemon libnss-mdns systemd rsyslog apt-utils sudo vim ssh python3-pip libavahi-common-dev libavahi-client-dev python3-venv supervisor tzdata wget iputils-*

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN adduser --quiet --disabled-password --shell /bin/bash --home /home/www --gecos "User" www

RUN usermod -aG sudo,root www

RUN echo "www:www" | chpasswd

RUN echo 'www ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir /tmp/install

COPY install /tmp/install

RUN dpkg -i /tmp/install/AquetiAPI*.deb

RUN tar -xf /tmp/install/homunculus.tar.gz -C /home/www/

RUN cp /tmp/install/supervisord.conf /etc/supervisor/
RUN cp -r /tmp/install/conf.d/* /etc/supervisor/conf.d/

WORKDIR /home/www/Homunculus

ENV LC_ALL=C

RUN pip install --upgrade pip setuptools wheel virtualenv supervisor-stdout

RUN pyvenv-3.5 venv

RUN /bin/bash -c "source venv/bin/activate && pip install -Ur requirements.txt"

EXPOSE 5000

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]
