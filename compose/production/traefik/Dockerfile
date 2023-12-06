FROM traefik:2.10.7
RUN mkdir -p /etc/traefik/acme \
  && touch /etc/traefik/acme/acme.json \
  && chmod 600 /etc/traefik/acme/acme.json
COPY ./compose/production/traefik/traefik.yml /etc/traefik

RUN mkdir -p /etc/certs
COPY ./certs/cert.crt /etc/certs
COPY ./certs/cert.key /etc/certs
RUN chmod 644 /etc/certs/cert.crt \
  && chmod 600 /etc/certs/cert.key
