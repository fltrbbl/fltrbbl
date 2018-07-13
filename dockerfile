FROM python:alpine3.7

RUN apk update \
    && apk upgrade \
    && apk add \
    bash \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    && pip install virtualenv

WORKDIR /var/task

RUN echo "PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '" >> /root/.bashrc

# prepare for virtualenv
RUN echo 'if [ ! -d "env" ]; then' >> /root/.bashrc && \
    echo '    virtualenv env --python=python3.7' >> /root/.bashrc && \
    echo 'fi' >> /root/.bashrc && \
    echo '' >> /root/.bashrc && \
    echo 'source env/bin/activate' >> /root/.bashrc


