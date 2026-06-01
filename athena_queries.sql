-- Creación de la tabla externa en Athena
CREATE EXTERNAL TABLE IF NOT EXISTS socios_basicfit (
    id INT,
    gender STRING,
    birthday STRING,
    age INT,
    abonement_type STRING,
    visit_per_week INT,
    days_per_week INT,
    attend_group_lesson BOOLEAN,
    fav_group_lesson STRING,
    avg_time_check_in DOUBLE,
    avg_time_check_out DOUBLE,
    avg_time_in_gym DOUBLE,
    drink_abo BOOLEAN,
    fav_drink STRING,
    personal_training BOOLEAN,
    uses_sauna BOOLEAN,
    name_personal_trainer STRING,
    visit_stars INT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://bigdata-basicfit-jonathan/raw/'
TBLPROPERTIES ('skip.header.line.count'='1');

-- Consulta 1: Distribución por tipo de abono
SELECT abonement_type, COUNT(*) as total_socios
FROM socios_basicfit
GROUP BY abonement_type
ORDER BY total_socios DESC;
-- Resultado: Standard 507 / Premium 493

-- Consulta 2: Tiempo medio y visitas por tipo de abono
SELECT abonement_type,
       ROUND(AVG(avg_time_in_gym), 2) as tiempo_medio,
       ROUND(AVG(visit_per_week), 2) as visitas_medias
FROM socios_basicfit
GROUP BY abonement_type;
-- Resultado: Premium 104.87 min / Standard 101.96 min - mismas visitas medias (2.68)

-- Consulta 3: Uso de servicios por tipo de abono
SELECT abonement_type,
       COUNT(*) as total_socios,
       SUM(CASE WHEN personal_training = true THEN 1 ELSE 0 END) as usan_personal_training,
       SUM(CASE WHEN uses_sauna = true THEN 1 ELSE 0 END) as usan_sauna
FROM socios_basicfit
GROUP BY abonement_type;
-- Resultado: Premium 101 personal training, 99 sauna / Standard 90 personal training, 87 sauna
