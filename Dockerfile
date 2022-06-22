FROM debian:bullseye

RUN apt update && \
    apt install -y python3-fastapi python3-serial python3-prometheus-client && \
    rm -rf /var/lib/apt/lists/*

ADD main.py main.py
ADD teleinfo.py main.py
