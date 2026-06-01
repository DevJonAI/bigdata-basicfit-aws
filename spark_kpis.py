import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Lectura desde S3
df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv("s3://bigdata-basicfit-jonathan/raw/gym_membership.csv")

# Filtro: eliminar socios menores de 16
df_filtrado = df.filter(F.col("age") >= 16)

# Campo derivado: segmento de visitas
df_segmentado = df_filtrado.withColumn("segmento_visitas",
    F.when(F.col("visit_per_week") >= 4, "Alta frecuencia")
     .when(F.col("visit_per_week") >= 2, "Media frecuencia")
     .otherwise("Baja frecuencia"))

# KPIs agregados por tipo de abono
df_kpis = df_segmentado.groupBy("abonoment_type").agg(
    F.count("*").alias("total_socios"),
    F.round(F.avg("avg_time_in_gym"), 2).alias("tiempo_medio_gym"),
    F.round(F.avg("visit_per_week"), 2).alias("visitas_medias"),
    F.sum(F.when(F.col("personal_training") == True, 1).otherwise(0)).alias("usan_personal_training"),
    F.sum(F.when(F.col("uses_sauna") == True, 1).otherwise(0)).alias("usan_sauna")
)

df_kpis.show()

# Guardar resultado en S3
df_kpis.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("s3://bigdata-basicfit-jonathan/analytics/kpis_por_abono/")

print("Proceso Spark completado. Resultados guardados en S3.")

job.commit()
