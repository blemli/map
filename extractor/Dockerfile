FROM ubuntu:24.04
RUN apt-get update && apt-get install -y osmium-tool wget
WORKDIR /data
COPY winterthur-extractor.sh /usr/local/bin/winterthur-extractor.sh
RUN chmod +x /usr/local/bin/winterthur-extractor.sh
ENTRYPOINT ["winterthur-extractor.sh"]
