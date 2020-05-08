# dynamic-dns-digital-ocean

Simple Docker supported dynamic DNS updater for DNS hosted on Digital Ocean 

Run on a Docker host in your home :)

### Requirements

* Digital Ocean API Token
* Your domain's name server must be pointing to Digital Ocean NS for your domain


### Docker Compose

Update docker compose with your your domains to keep up to date.

```
export DIGITAL_OCEAN_TOKEN=mytokenhere; docker-compose up -d
```
