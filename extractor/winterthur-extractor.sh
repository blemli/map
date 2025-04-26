#!/bin/sh
set -e
URL="https://download.geofabrik.de/europe/switzerland-latest.osm.pbf"
while true; do
  wget -q -O switzerland.osm.pbf "$URL"
  osmium extract --overwrite -r 1691239 switzerland.osm.pbf -o winterthur.osm.pbf
  sleep 28800  # 8 Stunden
done
