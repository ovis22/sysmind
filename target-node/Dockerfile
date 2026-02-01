FROM ubuntu:24.04

# Install basic tools, SSH server, and SRE diagnosis utilities
RUN apt-get update && apt-get install -y \
    openssh-server \
    sudo \
    python3 \
    iproute2 \
    iputils-ping \
    net-tools \
    curl \
    vim \
    rsyslog \
    stress-ng \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Configure SSH for fallback testing
RUN mkdir /var/run/sshd
RUN echo 'root:sysmind' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Expose SSH port
EXPOSE 22

# Start rsyslog and then SSHD
CMD rsyslogd && /usr/sbin/sshd -D
