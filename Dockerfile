FROM michaelschmidtvumc/curation-base:latest AS base

#* Copy project files
COPY common ${PROJECT_ROOT}/common
COPY entrypoint.py entrypoint.py

#? For security, the host's GAC is passed via a volume flag as the file
#? `credentials.json`.  It is read-only.
ENV GOOGLE_APPLICATION_CREDENTIALS="${PROJECT_ROOT}/credentials.json"
ENV ISSUE_NUMBER='DC2263'

#ENTRYPOINT [ "python3", "-c", "import os; print(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])" ]
ENTRYPOINT [ "python", "entrypoint.py" ]
