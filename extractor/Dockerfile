FROM alpine:3.17
RUN apk add --no-cache osmium-tool wget
WORKDIR /data
COPY winterthur-extractor.sh /usr/local/bin/winterthur-extractor.sh
RUN chmod +x /usr/local/bin/winterthur-extractor.sh
ENTRYPOINT ["winterthur-extractor.sh"]
