# Big Data Pipeline on AWS — Basic-Fit Member Analysis

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Spark](https://img.shields.io/badge/Apache%20Spark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Apache Parquet](https://img.shields.io/badge/Apache%20Parquet-50ABF1?style=for-the-badge&logo=apacheparquet&logoColor=white)

End-to-end batch pipeline on AWS to analyze gym member behavior using real-world data.

> This is an academic project and is not officially affiliated with Basic-Fit.

## AWS Services Used

- **Amazon S3** — Zone-based storage: raw, processed, dq-results, analytics
- **AWS Glue Crawler** — Automatic dataset cataloging
- **AWS Glue Data Catalog** — Table schema registry
- **AWS Glue Data Quality** — Validation with 8 DQDL rules (score 75%)
- **AWS Glue Studio** — Visual ETL Job with transformations
- **AWS Glue Spark** — Analytical processing and KPI calculation
- **Amazon Athena** — SQL queries directly on S3
- **Power BI Desktop** — Final dashboard with KPIs and insights

## Dataset

Gym Membership Dataset from Kaggle (author: Tarek Adam, license CC0).
1,000 records · 18 columns · CSV format.

[View on Kaggle](https://www.kaggle.com/datasets/ka66ledata/gym-membership-dataset)

## Architecture

S3 raw → Glue Crawler → Glue Data Quality → Glue ETL Job → S3 processed → Spark Job → S3 analytics → Athena → Power BI

## Screenshots

| # | Description |
|---|---|
| ![01](screenshots/03_s3_bucket_zones.png) | S3 Bucket Zones |
| ![02](screenshots/04_glue_crawler.png) | Glue Crawler |
| ![03](screenshots/05_glue_data_catalog_tables.png) | Glue Data Catalog Tables |
| ![04](screenshots/06_glue_dq_ruleset.png) | Glue DQ Ruleset |
| ![05](screenshots/07_glue_dq_run_history.png) | Glue DQ Run History |
| ![06](screenshots/08_glue_dq_score_snapshot.png) | Glue DQ Score Snapshot |
| ![07](screenshots/01_glue_data_quality_results.png) | Glue Data Quality — Results |
| ![08](screenshots/09_glue_etl_job_script.png) | Glue ETL Job Script |
| ![09](screenshots/10_glue_etl_job_run_succeeded.png) | Glue ETL Job — Run Succeeded |
| ![10](screenshots/11_glue_spark_kpis_script.png) | Glue Spark KPIs Script |
| ![11](screenshots/12_athena_query_members_by_type.png) | Athena — Members by Type |
| ![12](screenshots/13_athena_query_avg_time_visits.png) | Athena — Avg Time & Visits |
| ![13](screenshots/14_athena_query_services_usage.png) | Athena — Services Usage |
| ![14](screenshots/02_powerbi_dashboard.png) | Power BI Dashboard |

## Repository Structure

- `etl_job.py` — Glue Studio ETL Job script
- `spark_kpis.py` — Spark job script (v2.0), dynamically parameterized with Parquet output
- `ruleset_dqdl.txt` — AWS Glue Data Quality ruleset
- `athena_queries.sql` — SQL queries executed in Athena
- `screenshots/` — Evidence captures for each pipeline phase

## Technical Optimizations

**Dynamic Parameterization:** The `spark_kpis.py` script was refactored using `getResolvedOptions` to receive the `--BUCKET_NAME` argument at runtime. This eliminates hardcoded paths, making the pipeline secure, reusable and production-ready across any AWS environment.

**Storage Format Evolution:** The final output of the Spark Job was upgraded to columnar **Apache Parquet** format. Although the initial deployment and Athena queries shown in the `screenshots/` folder were executed using CSV, this improvement is implemented to significantly optimize query performance and reduce S3 read costs in subsequent execution cycles.
