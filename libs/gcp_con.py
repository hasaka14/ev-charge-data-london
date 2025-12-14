from google.cloud import bigquery
from google.oauth2 import service_account

def get_bq_client(project_id, key_path):
    """
    Create BigQuery client using service account JSON.
    """
    credentials = service_account.Credentials.from_service_account_file(key_path)
    client = bigquery.Client(project=project_id, credentials=credentials)
    return client