from libs.gcp_con import *

# Load → Merge → Drop staging

def load_and_merge_to_bigquery(
    df,
    project_id,
    dataset_id,
    staging_table,
    key_path,
    schema=None
):
    """
    Upload DataFrame to a staging table, merge into target table, drop staging table.
    
    Parameters:
        df (pd.DataFrame): Data to upload
        project_id (str): GCP project ID
        dataset_id (str): BigQuery dataset name
        staging_table (str): Temporary table for staging
        key_path (str): Service account JSON path
        schema (list, optional): BigQuery schema definition (list of SchemaField)

    Returns:
        None
    """

    client = get_bq_client(project_id, key_path)

    staging_table_id = f"{project_id}.{dataset_id}.{staging_table}"


    #Create staging table if it doesn't exist
    try:
        client.get_table(staging_table_id)
        print(f"Staging table {staging_table_id} exists, it will be overwritten.")
    except Exception:
        print(f"Staging table {staging_table_id} does not exist. Creating it...")
        table = bigquery.Table(staging_table_id, schema=schema)
        client.create_table(table)
        print("Staging table created.")


    #Load DataFrame into staging
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # overwrite existing staging table
        autodetect=True if schema is None else False,
        schema=schema
    )

    print(f"Uploading data to staging table: {staging_table_id}")
    load_job = client.load_table_from_dataframe(df, staging_table_id, job_config=job_config)
    load_job.result()
    print("Data uploaded to staging table.")


    #MERGE staging to target
    merge_query = f"""
        MERGE `stone-passage-247604.data_ev.ev_tbl` T
        USING `stone-passage-247604.staging_ev.staging_tbl` S
        ON
        T.UUID = S.UUID
        AND T.CONNECTIONID = S.CONNECTIONID
        WHEN MATCHED THEN
        UPDATE SET
            USAGECOST                 = S.USAGECOST,
            NUMBEROFPOINTS            = S.NUMBEROFPOINTS,
            STATUSTYPEID              = S.STATUSTYPEID,
            ADDRESSINFOID             = S.ADDRESSINFOID,
            TITLE                     = S.TITLE,
            ADDRESSLINE1              = S.ADDRESSLINE1,
            ADDRESSLINE2              = S.ADDRESSLINE2,
            TOWN                      = S.TOWN,
            STATEORPROVINCE           = S.STATEORPROVINCE,
            POSTCODE                  = S.POSTCODE,
            COUNTRYID                 = S.COUNTRYID,
            LATITUDE                  = S.LATITUDE,
            LONGITUDE                 = S.LONGITUDE,
            DISTANCEUNIT              = S.DISTANCEUNIT,
            POWERKW                   = S.POWERKW,
            AMPS                      = S.AMPS,
            VOLTAGE                   = S.VOLTAGE,
            QUANTITY                  = S.QUANTITY,
            LEVELID                   = S.LEVELID,
            CONNECTIONTYPEID          = S.CONNECTIONTYPEID,
            STATUSTYPEID_CONNECTION   = S.STATUSTYPEID_CONNECTION,
            CURRENTTYPEID             = S.CURRENTTYPEID

        WHEN NOT MATCHED THEN
        INSERT (
            ID,
            UUID,
            USAGECOST,
            NUMBEROFPOINTS,
            STATUSTYPEID,
            ADDRESSINFOID,
            TITLE,
            ADDRESSLINE1,
            ADDRESSLINE2,
            TOWN,
            STATEORPROVINCE,
            POSTCODE,
            COUNTRYID,
            LATITUDE,
            LONGITUDE,
            DISTANCEUNIT,
            CONNECTIONID,
            POWERKW,
            AMPS,
            VOLTAGE,
            QUANTITY,
            LEVELID,
            CONNECTIONTYPEID,
            STATUSTYPEID_CONNECTION,
            CURRENTTYPEID
        )
        VALUES (
            S.ID,
            S.UUID,
            S.USAGECOST,
            S.NUMBEROFPOINTS,
            S.STATUSTYPEID,
            S.ADDRESSINFOID,
            S.TITLE,
            S.ADDRESSLINE1,
            S.ADDRESSLINE2,
            S.TOWN,
            S.STATEORPROVINCE,
            S.POSTCODE,
            S.COUNTRYID,
            S.LATITUDE,
            S.LONGITUDE,
            S.DISTANCEUNIT,
            S.CONNECTIONID,
            S.POWERKW,
            S.AMPS,
            S.VOLTAGE,
            S.QUANTITY,
            S.LEVELID,
            S.CONNECTIONTYPEID,
            S.STATUSTYPEID_CONNECTION,
            S.CURRENTTYPEID
        );
    """

    query_job = client.query(merge_query)
    query_job.result()
    print("Merge completed.")

    #Drop staging table
    print(f"Dropping staging table: {staging_table_id}")
    client.delete_table(staging_table_id, not_found_ok=True)
    print("Staging table removed.")



