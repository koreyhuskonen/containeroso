FROM ubuntu:18.04

RUN apt-get update &&\
    #apt-get -y upgrade &&\
    apt-get -y install vim net-tools nmap openssh-server &&\
    apt-get -y autoremove

RUN mkdir /var/run/sshd

RUN useradd -m virtuoso
RUN echo 'virtuoso:password' | chpasswd
RUN usermod -a -G sudo virtuoso
RUN usermod -s /bin/bash virtuoso

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
