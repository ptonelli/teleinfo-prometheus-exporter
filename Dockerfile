FROM debian:bullseye

RUN apt update && \
    apt install -y python3-fastapi python3-serial python3-prometheus-client && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /root

ADD main.py main.py
ADD teleinfo.py main.py
ADD docker-entrypoint.sh docker-entrypoint.sh

ENV PORT=9093
ENV HOST=0.0.0.0
ENV VENDOR_ID=0403
ENV PRODUCT_ID=6001

ENTRYPOINT docker-entrypoint.sh
