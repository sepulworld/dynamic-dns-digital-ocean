#!/usr/bin/env python
from typing import List, Optional

import typer
import digitalocean
import logging
import requests
import os
import time
import tldextract

AUTH_TOKEN = os.environ.get("DIGITAL_OCEAN_AUTH_TOKEN", "")
LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()

logging.basicConfig(level=LOGLEVEL)


def run(check_interval: int = 300,
        digital_ocean_auth_token: str = None,
        domain: Optional[List[str]] = typer.Option(None)):
    """
    Run process to monitor and update DNS.
    Update only if current_ip isn't known yet, or different from
    gathered IP
    """
    known_ip = None

    if not domain:
        typer.echo("No domains provided")
        raise typer.Abort()

    while True:
        ip = _get_ip()

        if known_ip is None or ip != known_ip:
            logging.info(f'system public IP: {known_ip}')
            logging.warning(f'detected new system public IP: {ip}')
            for d in domain:
                tld, subdomain = _extract_domain_and_subdomain(d)
                _set_dns(tld, subdomain, ip, digital_ocean_auth_token)
            known_ip = ip
        else:
            known_ip = ip
            logging.info(f'system public IP : {known_ip}')

        time.sleep(check_interval)


def _get_ip():
    """Fetch my IP address as seen from outside world"""
    ip = requests.get("https://api.ipify.org/?format=json").json()['ip']
    return ip


def _extract_domain_and_subdomain(domain):
    subdomain = None
    extract = tldextract.extract(domain)
    tld = extract.domain + "." + extract.suffix
    if extract.subdomain:
        subdomain = extract.subdomain

    return tld, subdomain


def _set_dns(tld, subdomain, ip, token):
    domain = digitalocean.Domain(token=token, name=tld)
    records = domain.get_records()
    for r in records:
        if r.name == subdomain:
            logging.warning(f"Updating {subdomain}.{tld} to {ip}")
            r.data = ip
            r.ttl = 60
            r.save()
            break
    else:
        logging.warning(f"Creating new {subdomain} with A: {ip}")
        domain.create_new_domain_record(
            type='A',
            name=subdomain,
            data=ip
            )


if __name__ == '__main__':
    typer.run(run)
