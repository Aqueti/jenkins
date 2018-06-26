FROM ubuntu:16.04
MAINTAINER astepenko@aqueti.com

RUN apt-get update && apt-get -y install apt-transport-https duplicity python-pip avahi-utils avahi-daemon libnss-mdns systemd rsyslog apt-utils sudo vim ssh python3-pip libavahi-common-dev libavahi-client-dev python3-venv supervisor iputils-*

RUN adduser --quiet --disabled-password --shell /bin/bash --home /home/www --gecos "User" www

RUN usermod -aG sudo,root www

RUN echo "www:www" | chpasswd

RUN echo 'www ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

RUN mkdir /tmp/install

COPY install /tmp/install

RUN dpkg -i /tmp/install/AquetiAPI-linux64.deb

RUN tar -xzf /tmp/install/homunculus.tar.gz -C /home/www/

RUN cp -r /tmp/install/conf.d/* /etc/supervisor/conf.d/

WORKDIR /home/www/Homunculus

RUN pip install --upgrade pip setuptools wheel virtualenv

RUN pyvenv-3.5 venv

RUN /bin/bash -c "source venv/bin/activate && pip install -Ur requirements.txt"

EXPOSE 5000

CMD ["/usr/bin/supervisord"]
