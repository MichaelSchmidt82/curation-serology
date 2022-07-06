FROM michaelschmidtvumc/curation-base:latest AS base


ENV PROJECT_NAME="serology"
ENV PROJECT_ROOT="/project/${PROJECT_NAME}"
ENV PROJECT_SECRETS="/secrets"

#* Copy project files
RUN git clone \
    --depth=1 \
    https://github.com/MichaelSchmidt82/curation-serology.git ${PROJECT_ROOT} \
    && rm -rf ${PROJECT_ROOT}/.git \
    && rm ${PROJECT_ROOT}/*.sh

#? For security, the host's GAC is passed via a volume flag as the file
#? `credentials.json`.  It should be marked as is read-only.
ENV GOOGLE_APPLICATION_CREDENTIALS="${PROJECT_SECRETS}/credentials.json"
ENV ISSUE_NUMBER='DC2263'

# ENTRYPOINT [ "python" ]
# ENTRYPOINT [ "sh", "-c", "python ${PROJECT_ROOT}/entrypoint.py" ]