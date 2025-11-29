FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Basic system + XFCE desktop + RDP server
RUN apt-get update && \
    apt-get install -y \
        xfce4 \
        xfce4-goodies \
        xorg \
        dbus-x11 \
        xrdp \
        sudo \
        vim \
	vim-gtk3 \
	xfce4-terminal \
        postgresql-client \
	wget \
	curl \
	w3m \
	lynx \
	links2 \
	geany \
    && rm -rf /var/lib/apt/lists/*
RUN wget -O /usr/share/keyrings/dbeaver.gpg.key https://dbeaver.io/debs/dbeaver.gpg.key
RUN echo "deb [signed-by=/usr/share/keyrings/dbeaver.gpg.key] https://dbeaver.io/debs/dbeaver-ce /" | tee /etc/apt/sources.list.d/dbeaver.list
RUN apt-get install dbeaver-ce

RUN apt-get remove -y xfce4-power-manager
RUN update-alternatives --config x-terminal-emulator

# Create a user you can log in as (user: docker / password: docker)
RUN useradd -m -s /bin/bash docker \
    && echo "docker:docker" | chpasswd \
    && adduser docker sudo

# Create a user 2 you can log in as (user: docker2 / password: docker2)
RUN useradd -m -s /bin/bash docker2 \
    && echo "docker2:docker2" | chpasswd \
    && adduser docker2 sudo

# Tell XRDP to start XFCE session
RUN echo "xfce4-session" > /home/docker/.xsession \
    && chown docker:docker /home/docker/.xsession

# Tell XRDP to start XFCE session
RUN echo "xfce4-session" > /home/docker2/.xsession \
    && chown docker2:docker2 /home/docker2/.xsession


# Some distros use startwm.sh – make sure it starts XFCE
RUN sed -i.bak '/^test -x .*startplasma-x11/ s/^/#/' /etc/xrdp/startwm.sh || true \
    && sed -i.bak '/^test -x .*gnome-session/ s/^/#/' /etc/xrdp/startwm.sh || true \
    && echo "startxfce4" >> /etc/xrdp/startwm.sh

# Expose RDP port
EXPOSE 3389

# Start xrdp services (sesman + rdp itself)
CMD ["/bin/bash", "-c", "/usr/sbin/xrdp-sesman && /usr/sbin/xrdp -nodaemon"]

