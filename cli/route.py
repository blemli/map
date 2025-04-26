#!/usr/bin/env python

import os
import json
import webbrowser
import logging

from dotenv import load_dotenv, find_dotenv
import click
import requests
import polyline
import folium


# Load .env if present
load_dotenv(find_dotenv())

logger = logging.getLogger(__name__)

@click.command()
@click.argument('from_', metavar='FROM')  # "lat,long"
@click.argument('to', metavar='TO')        # "lat,long"
@click.option('--profile', default='bicycle', show_default=True, help='Routing profile (e.g. bicycle, car, foot)')
@click.option('--json', 'json_output', is_flag=True, help='Print raw JSON response')
@click.option('--host', default=None, help='OSRM host. Falls back to OSRM_HOST in .env or 127.0.0.1:5000')
@click.option('--show', is_flag=True, help='Generate route.html and open in browser')
@click.option('--verbose', is_flag=True, help='Enable debug output')
def main(from_, to, profile, json_output, host, show, verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
        logger.debug(f"Raw arguments: from={from_}, to={to}, profile={profile}, host={host}")

    # parse coords (OSRM expects lon,lat)
    try:
        lat1, lon1 = map(float, from_.split(','))
        lat2, lon2 = map(float, to.split(','))
    except ValueError:
        click.echo("Invalid FROM/TO format. Use lat,long", err=True)
        raise SystemExit(1)
    if verbose: logger.debug(f"Coordinates: lon1={lon1}, lat1={lat1}, lon2={lon2}, lat2={lat2}")
    # determine host
    if not host:
        host = os.getenv('OSRM_HOST', '127.0.0.1:5000')
    if not host.startswith(('http://', 'https://')):
        host = f'http://{host}'
    if verbose: logger.debug(f"Using OSRM host: {host}")

    # build URL
    url = (
        f"{host}/route/v1/{profile}/"
        f"{lon1},{lat1};{lon2},{lat2}"
        "?overview=full&geometries=polyline&steps=false"
    )
    if verbose:
        logger.debug(f"Request URL: {url}")

    # send request
    resp = requests.get(url)
    if verbose:
        logger.debug(f"HTTP status: {resp.status_code}")
    resp.raise_for_status()

    data = resp.json()
    if verbose:
        logger.debug(f"Response JSON: {json.dumps(data, indent=2)}")

    if json_output:
        click.echo(json.dumps(data, indent=2))
        return

    # extract metrics
    route = data['routes'][0]
    dist_km = route['distance'] / 1000.0
    dur_s = route['duration']
    mins = int(dur_s // 60)
    secs = int(dur_s % 60)

    click.echo(f"Distance: {dist_km:.2f} km")
    click.echo(f"Duration: {mins} min {secs} s")

    if show:
        coords = polyline.decode(route['geometry'])
        m = folium.Map(location=coords[0], zoom_start=14)
        folium.PolyLine(locations=coords, weight=5).add_to(m)
        out_file = "route.html"
        m.save(out_file)
        webbrowser.open(f"file://{os.path.abspath(out_file)}")

if __name__ == '__main__':
    main()
