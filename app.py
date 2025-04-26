#!/usr/bin/env python

from flask import Flask, send_file
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests,os,logging


app = Flask(__name__)

# Cache config (in-memory, simple)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Rate limiter (per IP)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per hour"])

@app.route('/')
def index():
    #serve assets/mapli-cover.png
    return send_file('assets/mapli-cover.png',
                     as_attachment=False)
# Route aliases: /route and /r
@app.route('/route/<start>/<end>')
@app.route('/r/<start>', defaults={'end': "Problemli GmbH"})
@app.route('/r/<start>/<end>')
@app.route('/route/<start>', defaults={'end': "Problemli GmbH"})
#@cache.cached(timeout=60)
@limiter.limit("3600 per hour")
def route_handler(start, end):
    start_coords= reverse_geocode(start)
    end_coords= reverse_geocode(end)
    if start_coords is None or end_coords is None:
        return {'error': 'Invalid coordinates'}, 400
    # Construct the OSRM query
    query = f"{start_coords['lon']},{start_coords['lat']};{end_coords['lon']},{end_coords['lat']}"
    try:
        resp =requests.get(f"{os.environ['OSRM_URL']}/route/v1/cycling/{query}")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {'error': str(e)}, 500
    return resp.json(), resp.status_code

def reverse_geocode(location):
    # Reverse geocode the address to get coordinates
    try:
        resp = requests.get(f"{os.environ['NOMINATIM_URL']}/search?q={location}&format=json&addressdetails=1&limit=1")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None
    if resp.status_code == 200 and len(resp.json()) > 0:
        return resp.json()[0]
    else:
        return None

# Search endpoints: /search and /s
@app.route('/search/<query>')
@app.route('/s/<query>')
#@cache.cached(timeout=1)
@limiter.limit("3600 per hour")
def search_handler(query):
    try:
        resp = requests.get(f"{os.environ['NOMINATIM_URL']}/search?q={query}&format=json&addressdetails=1&limit=1")
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return {'error': str(e)}, 500
    return resp.json(), resp.status_code

# Health check
@app.route('/up')
def health_check():
    return 'OK', 200


# Serve winterthur.osm.pbf from mounted volume
@app.route('/data/winterthur.osm.pbf')
@limiter.exempt
def serve_data():
    # assumes /data is mounted in container
    return send_file('/data/winterthur.osm.pbf',
                     as_attachment=True,
                     download_name='winterthur.osm.pbf',
                     mimetype='application/octet-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
