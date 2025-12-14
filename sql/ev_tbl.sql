CREATE TABLE `stone-passage-247604.data_ev.ev_tbl`
(
  ID                        INT64,
  UUID                      STRING,
  UsageCost                 STRING,
  NumberOfPoints            FLOAT64,
  StatusTypeID              FLOAT64,
  AddressInfoID             INT64,
  Title                     STRING,
  AddressLine1              STRING,
  AddressLine2              STRING,
  Town                      STRING,
  StateOrProvince           STRING,
  Postcode                  STRING,
  CountryID                 INT64,
  Latitude                  FLOAT64,
  Longitude                 FLOAT64,
  DistanceUnit              INT64,
  ConnectionID              INT64,
  PowerKW                   FLOAT64,
  Amps                      FLOAT64,
  Voltage                   FLOAT64,
  Quantity                  FLOAT64,
  LevelID                   FLOAT64,
  ConnectionTypeID          INT64,
  StatusTypeID_Connection   FLOAT64,
  CurrentTypeID             FLOAT64
)
CLUSTER BY UUID, ConnectionID;