## map

*free geocoding and routing service for winterthur*



## cli

there is a cool cli:

```bash
 pipx install git+https://github.com/blemli/map.git
 map route problemli analogattack
```

> [!TIP]
>
> you can set your home with: `map home set "<ADDRESS>"` and remove it with `map home clear`.
> Afterwards you can omit the source when your home and only do: `map route analaogattack`

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



## deployment

is  as easy as:

```bash
gh repo clone blemli/map && cd map
kamal deploy
```



> [!NOTE]
>
> you might need to install some prerequisites first:`app install 1password 1password-cli ruby && gem install kamal`



## development

don't be an egoist, contribute :heart:

### check if acessory is running

kamal accessory details winterthur-extractor


## links

- [nominatim quickstart](https://www.afi.io/blog/building-a-free-geocoding-and-reverse-geocoding-service-with-openstreetmap/?ref=blog.afi.io)
- [Geofabrik pbf download of switzerland](https://download.geofabrik.de/europe/switzerland.html)
- [Osrm-backend on dockerhub](https://hub.docker.com/r/osrm/osrm-backend)
- [qgis for viewing .pbf files](https://qgis.org/)
