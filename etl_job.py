import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Fuente: Glue Data Catalog
datasource = glueContext.create_dynamic_frame.from_catalog(
    database="db_basicfit_jonathan",
    table_name="gym_membership_csv",
    transformation_ctx="datasource"
)

# Filtro: eliminar socios menores de 16 (corrección del fallo de Data Quality)
filtered = Filter.apply(
    frame=datasource,
    f=lambda row: (row["age"] >= 16),
    transformation_ctx="filtered"
)

# Selección de columnas útiles
selected = SelectFields.apply(
    frame=filtered,
    paths=["id", "gender", "age", "abonement_type", "visit_per_week", "avg_time_in_gym", "personal_training", "uses_sauna"],
    transformation_ctx="selected"
)

# Renombrar avg_time_in_gym a tiempo_medio_gym
renamed1 = RenameField.apply(
    frame=selected,
    old_name="avg_time_in_gym",
    new_name="tiempo_medio_gym",
    transformation_ctx="renamed1"
)

# Renombrar visit_per_week a visitas_por_semana
renamed2 = RenameField.apply(
    frame=renamed1,
    old_name="visit_per_week",
    new_name="visitas_por_semana",
    transformation_ctx="renamed2"
)

# Eliminar columna id por privacidad
dropped = DropFields.apply(
    frame=renamed2,
    paths=["id"],
    transformation_ctx="dropped"
)

# Destino: S3 carpeta processed
glueContext.write_dynamic_frame.from_options(
    frame=dropped,
    connection_type="s3",
    connection_options={"path": "s3://bigdata-basicfit-jonathan/processed/"},
    format="csv",
    transformation_ctx="output"
)

job.commit()
