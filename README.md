# dynamic-dns-digital-ocean

Simple dynamic DNS updater for DNS hosted on Digital Ocean 

Designed to run on a Docker host at home.

### Requirements

* Digital Ocean API Token
* Your domain's name server must be pointing to Digital Ocean


### Docker Compose

Update docker compose with your your domains to keep up to date.

```
export DIGITAL_OCEAN_TOKEN=mytokenhere; docker-compose up -d
docker-compose logs -f
```
Or save in `.env` file in same directory as your docker-compose.yml and docker-compose will load for you

```
cat .env
DIGITAL_OCEAN_TOKEN=mytokenhere
```

### Variables

#### Environment Variables

`DIGITAL_OCEAN_TOKEN=""`
`LOGLEVEL="WARNING"`

#### CLI Variables

```
Usage: ddns-do.py [OPTIONS]

Options:
  -i, --check-interval INTEGER
  -d, --domain TEXT               [required]
  -t, --digital-ocean-auth-token TEXT
                                  [required]
  --help                          Show this message and exit.
```
