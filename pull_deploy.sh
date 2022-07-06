docker pull michaelschmidtvumc/curation-serology:latest
docker run \
    -it \
    --rm \
    --env-file=environment \
    -v $GOOGLE_APPLICATION_CREDENTIALS:/secrets/credentials.json:ro \
    michaelschmidtvumc/curation-serology
