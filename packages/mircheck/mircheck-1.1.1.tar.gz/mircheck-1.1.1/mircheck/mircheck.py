#!/usr/bin/env python3

import argparse
import requests
from time import time
import json
import os
import pkg_resources

def fetch_mirrors(country_code):
    url = f"http://mirrors.ubuntu.com/{country_code}.txt"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download mirror list. Status code: {response.status_code}")
    return response.text.splitlines()

def test_speed(mirror, distribution):
    url = f"{mirror}dists/{distribution}/Release"
    try:
        start_time = time()
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get('content-length', 0))
        if total_size == 0:
            return 0, "Mirror Not Live"

        downloaded_size = 0
        for data in response.iter_content(chunk_size=4096):
            downloaded_size += len(data)
            if time() - start_time > 0:
                break
        duration = time() - start_time
        speed_bps = downloaded_size / duration
        speed_kbps = speed_bps / 1024

        return speed_kbps, None
    except requests.exceptions.RequestException as e:
        return 0, "Mirror Not Live"

def get_country_code(country_name):
    json_path = pkg_resources.resource_filename(__name__, 'country-list.json')
    with open(json_path) as f:
        countries = json.load(f)
        for country in countries:
            if country['en'].lower() == country_name.lower():
                return country['alpha2'].upper()
    return None

def get_country_name(country_code):
    json_path = pkg_resources.resource_filename(__name__, 'country-list.json')
    with open(json_path) as f:
        countries = json.load(f)
        for country in countries:
            if country['alpha2'].upper() == country_code.upper():
                return country['en']
    return None

def main():
    try:
        parser = argparse.ArgumentParser(
            description="Update Debian sources.list with the fastest mirror.",
            formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument('distribution', type=str, help="Distribution code name (e.g., jammy, bionic).")
        parser.add_argument('country', type=str, help="Country code or name.")
        parser.add_argument('-a', '--arch', type=str, default=None, help="Specify architecture (e.g., amd64, arm64).")
        parser.add_argument('-s', '--sources', action='store_true', help="Include deb-src lines.")
        parser.add_argument('-o', '--outfile', type=str, default='./sources.list', help="Output file for sources.list.")
        parser.add_argument('-n', '--nonfree', action='store_true', help="Include non-free section.")
        parser.add_argument('-d', '--distribution_type', type=str, default='stable', choices=['stable', 'testing', 'unstable', 'experimental', 'release_codename', 'sid'], help="Specify which distribution of Debian to use.")
        args = parser.parse_args()

        if len(args.country) == 2:
            country_code = args.country.upper()
            country_name = get_country_name(country_code)
        else:
            country_name = args.country
            country_code = get_country_code(country_name)

        if not country_code:
            print(f"Invalid country: {args.country}")
            return

        print(f"Fetching mirror list for country code: {country_code}...")
        mirrors = fetch_mirrors(country_code)
        if not mirrors:
            print(f"No mirrors found for country code: {country_code}.")
            return

        print("Testing mirror speeds...")
        fastest_mirror = ""
        fastest_speed = 0

        for mirror in mirrors:
            speed, error = test_speed(mirror, args.distribution)
            if error:
                print(f"Speed for {mirror}: {error}")
            else:
                print(f"Speed for {mirror}: {speed:.2f} KB/s")
                if speed > fastest_speed:
                    fastest_speed = speed
                    fastest_mirror = mirror

        if not fastest_mirror:
            print("No valid mirrors found.")
            return

        print(f"Fastest mirror: {fastest_mirror} with speed {fastest_speed:.2f} KB/s")

        lines = [
            f"deb {fastest_mirror} {args.distribution} main restricted universe multiverse",
            f"deb {fastest_mirror} {args.distribution}-updates main restricted universe multiverse",
            f"deb {fastest_mirror} {args.distribution}-backports main restricted universe multiverse",
            f"deb {fastest_mirror} {args.distribution}-security main restricted universe multiverse"
        ]

        if args.sources:
            lines.extend([
                f"deb-src {fastest_mirror} {args.distribution} main restricted universe multiverse",
                f"deb-src {fastest_mirror} {args.distribution}-updates main restricted universe multiverse",
                f"deb-src {fastest_mirror} {args.distribution}-backports main restricted universe multiverse",
                f"deb-src {fastest_mirror} {args.distribution}-security main restricted universe multiverse"
            ])

        if args.nonfree:
            lines = [line + " non-free" for line in lines]

        with open(args.outfile, 'w') as f:
            f.write("\n".join(lines))

        print(f"Updated sources.list written to {args.outfile}")

    except KeyboardInterrupt:
        print("\nActivity cancelled")

if __name__ == "__main__":
    main()
