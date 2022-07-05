"""
PYTHONPATH=./:$PYTHONPATH python tools/snapshot_serology_dataset.py \
-p aou-res-curation-prod \
-t 2022q2r3 \
-s R2020q4r1_antibody_quest \
-c C2022q2r3_deid \
-r cdr-ops@aou-res-curation-prod.iam.gserviceaccount.com
"""

# coding=utf-8
"""
Script to generate the serology dataset in the form C{release_tag}_antibody_quest
containing tables from R2020q4r1_antibody_quest as done in DC-1981.
These will be used to create C{release_tag}_serology in the output project.
Issue: DC-2263
"""
#* STD Python imports
import os
import logging

#* Third party imports
from google.cloud.bigquery import Dataset
from google.cloud.bigquery import Client as BigQueryClient

#* Project imports
from common import auth, consts


LOGGER = logging.getLogger(__name__)


def create_serology_tables(client, snapshot_dataset_id: str,
                           ct_dataset_id: str) -> None:
    """
    Generate id_match tables in the specified snapshot dataset

    :param client: a BigQueryClient
    :param snapshot_dataset_id: Identifies the snapshot dataset (destination)
    :param src_serology_dataset_id: Identifies the source serology dataset
    :param ct_dataset_id: Identifies the Controlled tier dataset
    :return: None
    """
    for table in consts.SEROLOGY_TABLES:
        job = client.query(consts.SEROLOGY_QUERIES[table].render(
            project_id=client.project,
            source_dataset_id=os.environ['SRC_SEROLOGY_DATASET_ID'],
            dest_dataset_id=snapshot_dataset_id,
            ct_dataset_id=ct_dataset_id))
        job.result()
        LOGGER.info(f'Created table {snapshot_dataset_id}.{table}')


def create_serology_snapshot(bq_client: BigQueryClient) -> str:
    """
    Generates the serology snapshot dataset based on the release tag

    :param bq_client: a BigQueryClient
    :param release_tag: Release tag for the CDR run
    :param src_serology_dataset_id: Identifies the source serology dataset
    :return: str: Identifies the created snapshot serology dataset
    """

    import pdb; pdb.set_trace()
    dataset_id = f'C{os.environ["RELEASE_TAG"]}_antibody_quest'
    dataset = Dataset(f'{bq_client.project}.{dataset_id}')
    dataset.description = (f'Source dataset: {os.environ["SRC_SEROLOGY_DATASET_ID"]}'
                           f' *_ct views; JIRA issue number: {os.environ["ISSUE_NUMBER"]}')

    dataset.labels = {'release_tag': os.environ['RELEASE_TAG'], 'data_tier': 'controlled'}
    dataset = bq_client.create_dataset(dataset)
    LOGGER.info(f'Successfully created empty dataset {dataset.dataset_id}')
    return dataset.dataset_id


def main():

    # get credentials and create client
    # impersonation_creds = auth.get_impersonation_credentials(
    #     os.environ['RUN_AS_EMAIL'], consts.CDR_SCOPES)


    bq_client = BigQueryClient(os.environ['PROJECT_ID'])
    #bq_client = BigQueryClient(os.environ['PROJECT_ID'], credentials=impersonation_creds)

    # Create serology dataset
    dataset_id = create_serology_snapshot(bq_client)

    # Create serology tables
    create_serology_tables(bq_client, dataset_id, os.environ['CT_DATASET_ID'])


if __name__ == '__main__':
    main()
