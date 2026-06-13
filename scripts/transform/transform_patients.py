from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, explode)
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATIENT_PATH = PROJECT_ROOT/"data"/"raw"/"fhir_api"/"patient"

def createSparkSesh() ->  SparkSession:
    return(SparkSession.builder.appName("Transformer").getOrCreate())






def main():
    spark = createSparkSesh()
    patientFiles = list(RAW_PATIENT_PATH.glob("*.json"))
    rawBundleDF = (spark.read.option("multiline", "true").json([str(file) for file in patientFiles]))

    #rawBundleDF.printSchema()

    patientResourcesDF = (rawBundleDF.select(explode(col("entry")).alias("entry"))).select(col("entry.resource").alias("patient"))

    patients = patientResourcesDF.select(
        col("patient.id").alias("patient_id"),
        col("patient.gender").alias("gender"),
        col("patient.birthDate").alias("birth_date"),
        col("patient.address")[0]["city"].alias("city"),
        col("patient.address")[0]["state"].alias("state"),
        col("patient.address")[0]["postalCode"].alias("postalCode"),
        col("patient.maritalStatus.text").alias("marital_status"),
        col("patient.deceasedDateTime").alias("deceased_datetime")
    )
    patients.printSchema()
    patients.show(10)

    print(spark.version)
    spark.stop()






if __name__ == "__main__":
    main()