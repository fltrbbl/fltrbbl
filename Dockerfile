FROM janh/alpine-ml-python3.6

WORKDIR /var/task

RUN echo "PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '" >> /root/.bashrc

# prepare for virtualenv
RUN echo 'if [ ! -d "env" ]; then' >> /root/.bashrc && \
    echo '    virtualenv env --system-site-packages --python=python3.6' >> /root/.bashrc && \
    echo 'fi' >> /root/.bashrc && \
    echo '' >> /root/.bashrc && \
    echo 'source env/bin/activate' >> /root/.bashrc
