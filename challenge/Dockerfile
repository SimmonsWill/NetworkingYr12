FROM alpine:3.19
RUN apk add --no-cache python3
WORKDIR /srv/www
COPY index.html .
WORKDIR /srv
EXPOSE 8090
CMD ["python3", "-m", "http.server", "8090", "--directory", "www"]
