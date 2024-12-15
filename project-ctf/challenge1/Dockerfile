FROM ubuntu:latest


RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    debootstrap \
    && rm -rf /var/lib/apt/lists/*

RUN debootstrap --variant=buildd focal /home/chroot-jail http://archive.ubuntu.com/ubuntu/

COPY jail_setup.sh /home/chroot-jail/jail_setup.sh

RUN chmod +x /home/chroot-jail/jail_setup.sh

RUN chroot /home/chroot-jail ./jail_setup.sh

RUN rm -rf /home/chroot-jail/jail_setup.sh

COPY notes.txt /home/chroot-jail/home/notes.txt
COPY key.txt /home/chroot-jail/home/key.txt

WORKDIR /home

COPY rag.py /home/rag.py
COPY requirements.txt /home/requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "rag.py"]