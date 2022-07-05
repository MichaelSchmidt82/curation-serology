docker pull michaelschmidtvumc/curation-base:latest
docker build --tag michaelschmidtvumc/curation-serology .
docker push michaelschmidtvumc/curation-serology
docker image rm michaelschmidtvumc/curation-serology
# docker run \
#     -it \
#     --rm \
#     -v $GOOGLE_APPLICATION_CREDENTIALS:/project/curation/credentials.json:ro \
#     curation-serology


