# Open Charge Map → BigQuery Data Pipeline

## Overview

This project ingests electric vehicle (EV) charging station data from the **Open Charge Map (OCM) API**, transforms and normalizes the data using Python, loads it into **Google BigQuery**, and enables downstream **analytics and visualization**.

The pipeline follows the following pattern:

1. Retrieve data from the Open Charge Map API
2. Normalize and enrich the API response
3. Load data into a temporary BigQuery staging table
4. Merge data into the target BigQuery table (`data_ev.ev_tbl`)
5. Drop the staging table after successful merge

---

## Architecture & Flow

```
Open Charge Map API
        ↓
Python (extract & transform)
        ↓
BigQuery Staging Table
        ↓
MERGE (UUID + ConnectionID)
        ↓
BigQuery Target Table (data_ev.ev_tbl)
        ↓
Visualization / Analytics
```

---

## Folder Structure

```
project-root/
│
├── libs/
│   └── gcp_con.py
│       └─ BigQuery connection utilities
│
├── sql/
│   └── ev_tbl.sql
│       └─ BigQuery DDL / SQL statements for target table
│
├── src/
│   ├── bigquery_load.py
│   │   └─ Functions to load data into staging and MERGE into target table
│   │
│   └── get_city.py
│       └─ Reverse geocoding utility
│            Takes latitude & longitude
│            Used to fill missing city values
│
├── main.py
│   └─ Main orchestration script
│       • Fetch data from Open Charge Map API
│       • Normalize nested JSON data
│       • Filter data using London city boundary geometry
│       • Fill missing city values using latitude/longitude (reverse geocoding)
│       • Load, merge, and clean up data in BigQuery
│
├── requirements.txt
│   └─ Python dependencies
│
├── service-account.json
│   └─ GCP service account credentials (not committed)
│
└── README.md
```

---

## Key Components

### 1. Data Extraction

* Uses **Open Charge Map REST APIs** to retrieve EV charging station data
* Handles pagination and API response validation

### 2. Data Transformation

* Normalizes nested OCM JSON (POI → Connections)
* Produces one row per charging connection
* Filters data to the **London city area** using open street maps api
* Derives city names from latitude/longitude when missing


### 3. Data Loading (BigQuery)

* Uploads transformed data into a **temporary staging table**
* Executes a **MERGE** into the target table using:

  * `UUID`
  * `ConnectionID`
* Updates existing records and inserts new ones
* Drops the staging table after a successful merge

### 4. Target Table

* BigQuery table: `data_ev.ev_tbl`
* Designed for analytics and visualization
* Optimized for incremental loads using MERGE

---

## Data Dictionary

A **data dictionary** has been created for all fields extracted from the Open Charge Map API, including:

* POI identifiers
* Address and location attributes
* Charging connection specifications

Refer to the docs/README.md file for detailed field-level definitions.

---

## How to Use

### 1. Prerequisites

* Python 3.9+
* Google Cloud Project with BigQuery enabled
* Service account with BigQuery permissions

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure BigQuery Access

* Create a **GCP service account** with BigQuery permissions
* Download the key file as `service-account.json`
* Place it in the **project root directory**

```
project-root/
└── service-account.json
```

### 4. Config for OCM API Key in .env

* Add OCM API Key inside .env file

### 5. Run the Pipeline

```bash
python main.py
```

This will:

* Fetch data from Open Charge Map
* Transform and enrich the data
* Load and merge it into BigQuery
* Remove the staging table

---

## Visualization

Once loaded into BigQuery, the data can be visualized using:

* Power BI


---

## Author

Built using Python, BigQuery, and Open Charge Map APIs for EV infrastructure analytics.



## Open Charge Map License

This project uses data from **Open Charge Map** under their official license.

* Data Source: [https://openchargemap.org](https://openchargemap.org)
* License: Open Charge Map is made available under the **Creative Commons Attribution-ShareAlike (CC BY-SA)** license.

Users of this project must comply with Open Charge Map’s attribution and usage requirements.

---