FROM ubuntu:24.04

# Install basic tools and SSH server
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    python3 \
    iproute2 \
    iputils-ping \
    net-tools \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH
RUN mkdir /var/run/sshd
RUN echo 'root:sysmind' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
