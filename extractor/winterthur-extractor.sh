#!/bin/sh
set -e
URL="https://download.geofabrik.de/europe/switzerland-latest.osm.pbf"
curl https://api.openstreetmap.org/api/0.6/relation/1691239/full > winterthur.osm
while true; do
  wget -q -O switzerland.osm.pbf "$URL"
  osmium extract --overwrite -p winterthur.osm switzerland.osm.pbf -o winterthur.osm.pbf
  sleep 28800  # 8 Stunden
done
