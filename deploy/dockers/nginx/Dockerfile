FROM nginx:1.24-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY create-cert.sh .
COPY renew-cert.sh .


ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1
RUN apk add python3 python3-dev py3-pip build-base libressl-dev musl-dev libffi-dev
RUN pip3 install pip --upgrade
RUN pip3 install certbot-nginx
