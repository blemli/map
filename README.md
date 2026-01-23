## map

*free geocoding and routing service for winterthur*

![mapli-cover](assets/mapli-cover.png)



## cli

there is a cool cli:

```bash
 pipx install git+https://github.com/blemli/map.git
 map route problemli analogattack
```

> [!TIP]
>
> you can set your home with: `map config set home "<ADDRESS>"` and remove it with `map config reset home`.
> Afterwards you can omit the source when your at home and only do: `map route analaogattack`

for everything else see `map --help`



## osm export

There is a daily OSM-Export containing Winterthur County:

https://map.problem.li/data/winterthur.osm.pbf

```curl 
curl -L https://map.problem.li/data/winterthur.osm.pbf
```



## api

apps without an api are like milk without milk

- the `/route` endpoint (alias `/r`) calculates the quickest bicycle route between two points. If you only supply one point the start defaults to PHQ.

- the `/search` endpoint (alias`/s`) returns coordinates for an address (geocoding)

  ... and hopefully more to come (maybe `/open`?)



## deployment

is  as easy as:

```bash
gh repo clone blemli/map && cd map
docker build -t blemli/osrm-backend ./route/
docker push blemli/osrm-backend
kamal deploy
kamal accessory reboot osrm
kamal accessory reboot nominatim
kamal open
```

> [!CAUTION]
>
> until the extractor is working, you need to also upload the plane file: `scp route/winterthur.osm.pbf webhost:/opt/winterthur-data/`



> [!NOTE]
>
> you might need to install some prerequisites first:`app install 1password 1password-cli ruby gh && gem install kamal`



## todo

nominatim replication url?



## Profile improvement

| From      | To               | date             | Measured | Base      | V1   |
| --------- | ---------------- | ---------------- | -------- | --------- | ---- |
| problemli | Ruhtalstrasse 22 | 2025-05-15 09:55 |          | 6 min 57s |      |
|           |                  |                  |          |           |      |
|           |                  |                  |          |           |      |
|           |                  |                  |          |           |      |





## development

don't be an egoist, contribute :heart:

here are some hints for you:

### an overview over the components

```mermaid
architecture-beta
 group map(cloud)[map]

    service main(server)[app] in map
    service extractor(server)[Extractor osmium] in map
    service osrm(server)[Route OSRM] in map
    service nominatim(server)[Search Nominatim] in map

		main:B -- T:extractor
		main:R -- L:osrm
		main:L -- R:nominatim
		nominatim:B -- L:extractor
    osrm:B -- R:extractor
```



### the right tool for the right job

```bash
brew install osmium-tool gdal curl
```



| tool          | Job  | Beispiel                                      |
| ------------- | ---- | --------------------------------------------- |
| `osmium-tool` |      | osmium fileinfo --extended winterthur.osm.pbf |
| `gdal`        |      | `ogrinfo -ro -al -so winterthur.osm.pbf`      |
| `curl`        |      |                                               |

### get pbf of winterthur

```bash
curl "https://download.geofabrik.de/europe/switzerland-latest.osm.pbf" --output switzerland.osm.pbf
osmium extract --overwrite -b 8.6404,47.4389,8.8169,47.5616 -o winterthur.osm.pbf switzerland.osm.pbf
osmium export -o winterthur.geojson winterthur.osm.pbf
```

 



## run nominatim locally for testing

```bash
docker run -it --rm \
  -v "$(pwd)/winterthur.osm.pbf:/nominatim/data/winterthur.osm.pbf" \
  -e PBF_PATH=/nominatim/data/winterthur.osm.pbf \
  -p 8080:8080 \
  --name nominatim \
  mediagis/nominatim:4.3
```

test it: http://127.0.0.1:8080/search?q=cameo&addressdetails=1&limit=1

> [!IMPORTANT]
>
> Be patient, It can take a long time until its up and running



## run osrm locally for testing

[get pbf](#get-pbf-of-winterthur)

```bash
cd route
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/bicycle.lua /data/winterthur.osm.pbf
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/winterthur.osrm
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/winterthur.osrm
docker run -t -i -p 5001:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --algorithm mld /data/winterthur.osrm
```

Test it: http://127.0.0.1:5001/route/v1/cycling/8.727788982270633,47.499053788622724;8.718605739005532,47.495018136217375?overview=full&geometries=geojson



## run app.py locally for testing





## links

- [nominatim quickstart](https://www.afi.io/blog/building-a-free-geocoding-and-reverse-geocoding-service-with-openstreetmap/?ref=blog.afi.io)
- [Geofabrik pbf download of switzerland](https://download.geofabrik.de/europe/switzerland.html)
- [Osrm-backend on dockerhub](https://hub.docker.com/r/osrm/osrm-backend)
- [qgis for viewing .pbf files](https://qgis.org/)
- [draw bouding boxes](https://norbertrenner.de/osm/bbox.html)
