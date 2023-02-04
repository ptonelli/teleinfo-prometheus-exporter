FROM debian:bullseye

RUN apt update && \
    apt install -y python3-fastapi python3-serial python3-prometheus-client uvicorn && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

ADD main.py main.py
ADD teleinfo.py teleinfo.py
ADD docker-entrypoint.sh docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh

ENV PORT=9093
ENV HOST=0.0.0.0

ENTRYPOINT /root/docker-entrypoint.sh
