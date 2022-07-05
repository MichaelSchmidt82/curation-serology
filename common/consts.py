# JINJA
import jinja2

#* Third party - Google Auth constants
TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
IMPERSONATION_LIFETIME = 3600

DEFAULT_SCOPES = [
    'https://www.googleapis.com/auth/devstorage.read_only',
    'https://www.googleapis.com/auth/bigquery.read_only',
]

CDR_SCOPES = [
    'https://www.googleapis.com/auth/bigquery',
    'https://www.googleapis.com/auth/devstorage.read_write',
    'https://www.googleapis.com/auth/trace.append'
]


#* Third party - Jinja constants
JINJA_ENV = jinja2.Environment(
    # block tags on their own lines
    # will not cause extra white space
    trim_blocks=True,
    lstrip_blocks=True,
    # syntax highlighting should be better
    # with these comment delimiters
    comment_start_string='--',
    comment_end_string=' --',
    # in jinja2 autoescape is for html; jinjasql supports autoescape for sql
    # TODO Look into jinjasql for sql templating
    autoescape=False)

#* Project Level - Queries
PERSON_QUERY = JINJA_ENV.from_string("""
CREATE TABLE `{{project_id}}.{{dest_dataset_id}}.serology_person`
LIKE `{{project_id}}.{{source_dataset_id}}.person` AS
SELECT
  serology_person_id
  , collection_date
  , NULL AS sex_at_birth
  , NULL AS age
  , NULL AS race
  , NULL AS state,
  control_status,
  person_id
FROM `{{project_id}}.{{source_dataset_id}}.person`
WHERE control_status IN ('Negative', 'Non-Control')
AND person_id IN (
  SELECT person_id
  FROM `{{project_id}}.{{ct_dataset_id}}.person`)
UNION ALL
# non AoU pids
SELECT *
FROM `{{project_id}}.{{source_dataset_id}}.person`
WHERE control_status NOT IN ('Negative', 'Non-Control')""")

TITER_QUERY = JINJA_ENV.from_string("""
CREATE TABLE `{{project_id}}.{{dest_dataset_id}}.titer`
LIKE `{{project_id}}.{{source_dataset_id}}.titer` AS
SELECT *
FROM `{{project_id}}.{{source_dataset_id}}.titer`
WHERE serology_person_id IN (
  SELECT serology_person_id
  FROM `{{project_id}}.{{dest_dataset_id}}.serology_person`)""")

ROCHE_ORTHO_QUERY = JINJA_ENV.from_string("""
CREATE TABLE `{{project_id}}.{{dest_dataset_id}}.roche_ortho`
LIKE `{{project_id}}.{{source_dataset_id}}.roche_ortho` AS
SELECT  *
FROM `{{project_id}}.{{source_dataset_id}}.roche_ortho`
WHERE serology_person_id IN (
  SELECT serology_person_id
  FROM `{{project_id}}.{{dest_dataset_id}}.serology_person`)""")

TEST_QUERY = JINJA_ENV.from_string("""
CREATE TABLE `{{project_id}}.{{dest_dataset_id}}.test`
LIKE `{{project_id}}.{{source_dataset_id}}.test` AS
SELECT *
FROM `{{project_id}}.{{source_dataset_id}}.test`
WHERE serology_person_id IN (
  SELECT serology_person_id
  FROM `{{project_id}}.{{dest_dataset_id}}.serology_person`)""")

RESULT_QUERY = JINJA_ENV.from_string("""
CREATE TABLE `{{project_id}}.{{dest_dataset_id}}.result`
LIKE `{{project_id}}.{{source_dataset_id}}.result` AS
SELECT *
FROM `{{project_id}}.{{source_dataset_id}}.result`
WHERE test_id IN (
  SELECT distinct test_id
  FROM `{{project_id}}.{{dest_dataset_id}}.test`)""")

#* Project level - serology constants
PERSON = 'person'
S_TITER = 'titer'
S_ROCHE_ORTHO = 'roche_ortho'
S_TEST = 'test'
S_RESULT = 'result'

SEROLOGY_TABLES = [PERSON, S_TITER, S_ROCHE_ORTHO, S_TEST, S_RESULT]
SEROLOGY_QUERIES = {
    PERSON: PERSON_QUERY,  # All table creation queries depend on person
    S_TITER: TITER_QUERY,
    S_ROCHE_ORTHO: ROCHE_ORTHO_QUERY,
    S_TEST: TEST_QUERY,
    S_RESULT: RESULT_QUERY  # Result table creation query depends on test
}