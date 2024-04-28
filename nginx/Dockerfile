FROM ubuntu:20:04

RUN apt update && apt install certbot
RUN apt install python3-certbot-dns-digitalocean && touch ~/certbot-creds.ini && chmod go-rwx ~/certbot-creds.ini && nano ~/certbot-creds.ini
