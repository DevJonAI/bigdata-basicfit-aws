-- =============================================================================
-- Athena SQL Queries — Basic-Fit Member Analysis
-- Database: db_basicfit_jonathan
-- Source: S3 raw zone (gym_membership.csv)
-- =============================================================================


-- -----------------------------------------------------------------------------
-- Table definition — external table pointing to the S3 raw zone
-- -----------------------------------------------------------------------------

CREATE EXTERNAL TABLE IF NOT EXISTS socios_basicfit (
    id                      INT,
    gender                  STRING,
    birthday                STRING,
    age                     INT,
    abonement_type          STRING,
    visit_per_week          INT,
    days_per_week           INT,
    attend_group_lesson     BOOLEAN,
    fav_group_lesson        STRING,
    avg_time_check_in       DOUBLE,
    avg_time_check_out      DOUBLE,
    avg_time_in_gym         DOUBLE,
    drink_abo               BOOLEAN,
    fav_drink               STRING,
    personal_training       BOOLEAN,
    uses_sauna              BOOLEAN,
    name_personal_trainer   STRING,
    visit_stars             INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://bigdata-basicfit-jonathan/raw/'
TBLPROPERTIES ('skip.header.line.count' = '1');


-- -----------------------------------------------------------------------------
-- Query 1: Member distribution by membership type
-- Result: Standard 507 / Premium 493
-- -----------------------------------------------------------------------------

SELECT
    abonement_type,
    COUNT(*) AS total_members
FROM socios_basicfit
GROUP BY abonement_type
ORDER BY total_members DESC;


-- -----------------------------------------------------------------------------
-- Query 2: Average gym time and weekly visits by membership type
-- Result: Premium 104.87 min / Standard 101.96 min — same avg visits (2.68)
-- -----------------------------------------------------------------------------

SELECT
    abonement_type,
    ROUND(AVG(avg_time_in_gym), 2)  AS avg_time_in_gym_minutes,
    ROUND(AVG(visit_per_week), 2)   AS avg_weekly_visits
FROM socios_basicfit
GROUP BY abonement_type;


-- -----------------------------------------------------------------------------
-- Query 3: Additional services usage by membership type
-- Result: Premium — 101 personal training, 99 sauna
--         Standard — 90 personal training, 87 sauna
-- -----------------------------------------------------------------------------

SELECT
    abonement_type,
    COUNT(*)                                                        AS total_members,
    SUM(CASE WHEN personal_training = true THEN 1 ELSE 0 END)      AS uses_personal_training,
    SUM(CASE WHEN uses_sauna = true THEN 1 ELSE 0 END)             AS uses_sauna
FROM socios_basicfit
GROUP BY abonement_type;