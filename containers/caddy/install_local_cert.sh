#!/bin/bash

# REF: https://caddyserver.com/docs/running#local-https-with-docker
# REF: https://chromium.googlesource.com/chromium/src/+/refs/heads/lkgr/docs/linux/cert_management.md

set -o errexit

docker compose cp \
    caddy:/data/caddy/pki/authorities/local/root.crt \
    /usr/local/share/ca-certificates/root.crt

sudo update-ca-certificates

which certutil || sudo apt-get install --yes libnss3-tools

# https://web.archive.org/web/20131212024426/https://blogs.oracle.com/meena/entry/notes_about_trust_flags

certutil \
    -d -d sql:$HOME/.pki/nssdb \
    -A -t "P,," \
    -n "Caddy self-signed root" \
    -i /usr/local/share/ca-certificates/root.crt


## Delete with:
# certutil -d sql:$HOME/.pki/nssdb -D -n "Caddy self-signed root"