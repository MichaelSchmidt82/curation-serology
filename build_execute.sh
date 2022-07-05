docker build --tag curation-serology .
docker run \
    -it \
    --rm \
    -v $GOOGLE_APPLICATION_CREDENTIALS:/project/curation/credentials.json:ro \
    curation-serology


