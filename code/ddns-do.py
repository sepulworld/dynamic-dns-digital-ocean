#!/usr/bin/env python

import click
import digitalocean
import logging
import requests
import os
import time
import tldextract

AUTH_TOKEN = os.environ.get("DIGITAL_OCEAN_AUTH_TOKEN", "")
logging.basicConfig(level=logging.INFO)


@click.command()
@click.option('--check-interval', '-i', default=300)
@click.option('--domain', '-d', multiple=True, required=True)
@click.option(
    '--digital-ocean-auth-token',
    '-t',
    default=AUTH_TOKEN,
    required=True
)
def run(check_interval,
        digital_ocean_auth_token,
        domain):
    """Run process to monitor and update DNS"""
    while True:
        ip = _get_ip()
        logging.info(f'current system public IP: {ip}')
        for d in domain:
            tld, subdomain = _extract_domain_and_subdomain(d)
            _set_dns(tld, subdomain, ip, digital_ocean_auth_token)
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
            logging.info(f"Updating {subdomain}.{tld} to {ip}")
            r.data = ip
            r.ttl = 60
            r.save()
            break
    else:
        logging.info(f"Creating new {subdomain} with A: {ip}")
        domain.create_new_domain_record(
            type='A',
            name=subdomain,
            data=ip
            )


if __name__ == '__main__':
    run()
