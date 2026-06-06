import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import functions as F


# ---------------------------------------------------------------------------
# Job initialisation
# ---------------------------------------------------------------------------

args = getResolvedOptions(sys.argv, ["JOB_NAME", "BUCKET_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Retrieve the S3 bucket name passed as a runtime argument.
# Using getResolvedOptions eliminates hardcoded paths, making the job
# reusable across environments without modifying the script.
bucket_name = args["BUCKET_NAME"]


# ---------------------------------------------------------------------------
# Extract — read raw dataset from S3
# ---------------------------------------------------------------------------

df = (
    spark.read
    .option("header", "true")
    .option("inferSchema", "true")
    .csv(f"s3://{bucket_name}/raw/gym_membership.csv")
)


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------

# Filter: remove members under 16 years old, consistent with the ETL job.
df_filtered = df.filter(F.col("age") >= 16)

# Derived field: classify members into visit frequency segments.
# This enables behavioural segmentation downstream (e.g. in Power BI).
df_segmented = df_filtered.withColumn(
    "visit_frequency_segment",
    F.when(F.col("visit_per_week") >= 4, "High frequency")
     .when(F.col("visit_per_week") >= 2, "Medium frequency")
     .otherwise("Low frequency"),
)

# Aggregate KPIs grouped by membership type.
# Metrics: total members, average gym time, average weekly visits,
# and count of members using personal training or sauna.
df_kpis = df_segmented.groupBy("abonoment_type").agg(
    F.count("*").alias("total_members"),
    F.round(F.avg("avg_time_in_gym"), 2).alias("avg_time_in_gym_minutes"),
    F.round(F.avg("visit_per_week"), 2).alias("avg_weekly_visits"),
    F.sum(
        F.when(F.col("personal_training") == True, 1).otherwise(0)
    ).alias("uses_personal_training"),
    F.sum(
        F.when(F.col("uses_sauna") == True, 1).otherwise(0)
    ).alias("uses_sauna"),
)

df_kpis.show()


# ---------------------------------------------------------------------------
# Load — write KPI results to S3 in Parquet format
# ---------------------------------------------------------------------------

# Parquet is used over CSV for columnar storage efficiency,
# significantly reducing Athena scan costs on subsequent queries.
(
    df_kpis.write
    .mode("overwrite")
    .parquet(f"s3://{bucket_name}/analytics/kpis_por_abono/")
)

print("Spark job completed. KPI results saved in Parquet format to S3.")


# ---------------------------------------------------------------------------
# Commit job
# ---------------------------------------------------------------------------

job.commit()