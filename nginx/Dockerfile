FROM nginx

COPY ./default.conf /etc/nginx/config.d/default.conf

USER root

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

USER nginx
