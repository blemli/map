#!/usr/bin/env python

from flask import Flask, send_file
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests

app = Flask(__name__)

# Cache config (in-memory, simple)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)

# Rate limiter (per IP)
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["100 per hour"])

# Route aliases: /route and /r
@app.route('/route')
@app.route('/r')
@cache.cached(timeout=60)
@limiter.limit("3600 per hour")
def route_handler():
    # placeholder
    return '', 204

# Search endpoints: /search and /s
@app.route('/search/{query}')
@app.route('/s/{query}')
@cache.cached(timeout=60)
@limiter.limit("3600 per hour")
def search_handler():
    resp = requests.get(f"{os.environ['NOMINATIM_URL']}/search?q={query}&format=json&addressdetails=1&limit=1")
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
