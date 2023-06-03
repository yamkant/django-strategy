FROM nginx:1.21.6

RUN apt-get update
RUN apt-get install -y openssl

COPY ./entrypoint.sh /entrypoint.sh
COPY ./code/templates /etc/nginx/templates

COPY ./staticfiles /static

ENV NGINX_HOST localhost
ENV INITIAL_START 1

CMD ["/bin/bash", "/entrypoint.sh"]
