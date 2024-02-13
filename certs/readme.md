openssl req -out cert.csr -newkey rsa:2048 -nodes -keyout cert.key -config san.cnf

# create self-signed certificate
openssl x509 -signkey cert.key -in cert.csr -req -days 700 -out cert.crt
