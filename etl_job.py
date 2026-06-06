import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import (
    DropFields,
    Filter,
    RenameField,
    SelectFields,
)
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext


# ---------------------------------------------------------------------------
# Job initialisation
# ---------------------------------------------------------------------------

args = getResolvedOptions(sys.argv, ["JOB_NAME"])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args["JOB_NAME"], args)


# ---------------------------------------------------------------------------
# Extract — load raw dataset from Glue Data Catalog
# ---------------------------------------------------------------------------

datasource = glueContext.create_dynamic_frame.from_catalog(
    database="db_basicfit_jonathan",
    table_name="gym_membership_csv",
    transformation_ctx="datasource",
)


# ---------------------------------------------------------------------------
# Transform
# ---------------------------------------------------------------------------

# Filter: remove members under 16 years old.
# This corrects the Data Quality rule failure detected in the DQ job,
# where a small number of records contained invalid age values.
filtered = Filter.apply(
    frame=datasource,
    f=lambda row: row["age"] >= 16,
    transformation_ctx="filtered",
)

# Select only the columns relevant for downstream analysis.
# Unused fields (e.g. contact info, internal IDs) are excluded here.
selected = SelectFields.apply(
    frame=filtered,
    paths=[
        "id",
        "gender",
        "age",
        "abonement_type",
        "visit_per_week",
        "avg_time_in_gym",
        "personal_training",
        "uses_sauna",
    ],
    transformation_ctx="selected",
)

# Rename columns to standardised English snake_case naming convention.
renamed = RenameField.apply(
    frame=selected,
    old_name="avg_time_in_gym",
    new_name="avg_time_in_gym_minutes",
    transformation_ctx="renamed_avg_time",
)

renamed = RenameField.apply(
    frame=renamed,
    old_name="visit_per_week",
    new_name="weekly_visits",
    transformation_ctx="renamed_visits",
)

# Drop the member ID field to comply with data privacy requirements.
cleaned = DropFields.apply(
    frame=renamed,
    paths=["id"],
    transformation_ctx="cleaned",
)


# ---------------------------------------------------------------------------
# Load — write processed dataset to S3 in CSV format
# ---------------------------------------------------------------------------

glueContext.write_dynamic_frame.from_