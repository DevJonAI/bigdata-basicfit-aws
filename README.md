# 🏋️ Big Data Pipeline en AWS — Análisis de socios Basic-Fit

Proyecto final del Módulo Big Data. Pipeline batch completo en AWS para analizar el comportamiento de socios de gimnasio.

> ⚠️ Este proyecto es académico y no está afiliado oficialmente a Basic-Fit.

## 🛠️ Servicios AWS utilizados

- **Amazon S3** — Almacenamiento por zonas: raw, processed, dq-results, analytics
- **AWS Glue Crawler** — Catalogación automática del dataset
- **AWS Glue Data Catalog** — Registro del esquema de la tabla
- **AWS Glue Data Quality** — Validación con 8 reglas DQDL (score 75%)
- **AWS Glue Studio** — ETL Job visual con transformaciones
- **AWS Glue Spark** — Procesamiento analítico y cálculo de KPIs
- **Amazon Athena** — Consultas SQL sobre S3
- **Power BI Desktop** — Dashboard final con KPIs e insights

## 📊 Dataset

Gym Membership Dataset de Kaggle (autor: Tarek Adam, licencia CC0).
1.000 registros, 18 columnas, formato CSV.
👉 https://www.kaggle.com/datasets/tarekAdam/gym-membership-dataset

## 🏗️ Arquitectura

S3 raw → Glue Crawler → Glue Data Quality → Glue ETL Job → S3 processed → Spark Job → S3 analytics → Athena → Power BI

## 📁 Estructura del repositorio

- `etl_job.py` — Script del ETL Job de Glue Studio
- `spark_kpis.py` — Script del job de Spark para calcular KPIs
- `ruleset_dqdl.txt` — Reglas de calidad de AWS Glue Data Quality
- `athena_queries.sql` — Consultas SQL ejecutadas en Athena
- `screenshots/` — Capturas de evidencia de cada fase
