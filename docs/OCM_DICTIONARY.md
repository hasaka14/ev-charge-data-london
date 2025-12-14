## Open Charge Map (OCM) Data Dictionary

This section describes the fields extracted from the **Open Charge Map (OCM) API** and loaded into BigQuery.  
Each row in the dataset represents a **single charging connection** at an EV charging location.

### 📍 Point of Interest (POI) & Address Fields

| Field Name | Description | Codes / Example Values |
|-----------|------------|------------------------|
| ID | Unique numeric identifier for the charging location (POI) in Open Charge Map. | `123456` |
| UUID | Globally unique identifier for the charging location. Remains stable across updates. | `A69BBFCB-B6E8-40AB-8D8A-04479B47C0C9` |
| UsageCost | Cost information for using the charging point. | `Free`, `Paid`, `£0.30/kWh` |
| NumberOfPoints | Total number of charging points available at the location. | `1`, `2`, `4` |
| StatusTypeID | Operational status of the charging location. | `50 = Operational`, `75 = Planned`, `100 = Decommissioned` |
| AddressInfoID | Unique identifier for the address record. | `987654` |
| Title | Name or title of the charging location. | `Tesco Superstore EV Charging` |
| AddressLine1 | Primary street address of the charging location. | `123 High Street` |
| AddressLine2 | Secondary address information. | `Car Park Level 2` |
| Town | City or town where the charging location is located. | `London` |
| StateOrProvince | State, province, or region. | `Greater London` |
| Postcode | Postal or ZIP code. | `SW1A 1AA` |
| CountryID | Country identifier (OCM reference). | `1 = UK`, `2 = USA`, `105 = Germany` |
| Latitude | Latitude coordinate of the charging location. | `51.5074` |
| Longitude | Longitude coordinate of the charging location. | `-0.1278` |
| DistanceUnit | Unit used for distance measurement. | `0 = KM`, `1 = Miles` |

---

### 🔌 Charging Connection Fields

| Field Name | Description | Codes / Example Values |
|-----------|------------|------------------------|
| ConnectionID | Unique identifier for a charging connection. | `470868` |
| PowerKW | Maximum power output in kilowatts. | `7.0`, `22.0`, `50.0`, `150.0` |
| Amps | Maximum current supported by the connection. | `16`, `32`, `63` |
| Voltage | Electrical voltage supported. | `230`, `400`, `800` |
| Quantity | Number of identical connectors. | `1`, `2` |
| LevelID | Charging level classification. | `1 = Level 1`, `2 = Level 2`, `3 = DC Fast` |
| ConnectionTypeID | Connector type identifier. | `25 = Type 2`, `33 = CCS`, `2 = CHAdeMO` |
| StatusTypeID_Connection | Operational status of the charging connection. | `50 = Operational`, `75 = Planned` |
| CurrentTypeID | Electrical current type. | `10 = AC Single Phase`, `20 = AC Three Phase`, `30 = DC` |

---

