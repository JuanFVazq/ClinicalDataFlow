from pyspark.sql import SparkSession
from pyspark.sql.functions import (col, explode, when, floor, datediff, current_date, to_date)
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATIENT_PATH = PROJECT_ROOT/"data"/"raw"/"fhir_api"/"patient"

def createSparkSesh() ->  SparkSession:
    return(SparkSession.builder.appName("Transformer").getOrCreate())

def runDataValidation(patients) -> None:
    rowCount = patients.count()

    nullPatients = patients.filter(col("patient_id").isNull()).count()
    duplicatePatients = (patients.groupBy("patient_id").count().filter(col("count") > 1).count())
    invalidBirthPatients = patients.filter(col("birth_date") > current_date()).count()

    if nullPatients > 0:
        raise ValueError(f"Data Validation failed: {nullPatients} Null Patient IDs Found")

    if duplicatePatients > 0:
        raise ValueError(f"Data Validation failed: {duplicatePatients} Duplicate Patient IDs Found")
    
    if invalidBirthPatients > 0:
        raise ValueError(f"Data Validation failed: {invalidBirthPatients} Invalid Birth Dates Found Found")



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
    patients = patients.withColumn("deceased_flag", when(col("deceased_datetime").isNotNull(), True).otherwise(False))

    patients = patients.withColumn("age", floor(datediff(when(col("deceased_datetime").isNotNull(),to_date(col("deceased_datetime")))
                                                         .otherwise(current_date()),col("birth_date"))/365.25))
    
    patients = patients.withColumn("age_group", when(col("age") < 18, "0-17")
                                   .when((col("age") >= 18) & (col("age") <= 34), "18-34")
                                   .when((col("age") >= 35) & (col("age") <= 49), "35-49")
                                   .when((col("age") >= 50) & (col("age") <= 64), "50-64")
                                   .otherwise("65+")
                                   )
    
    
    
    patients.printSchema()
    patients.show(10)
    runDataValidation(patients)

    print(spark.version)
    spark.stop()






if __name__ == "__main__":
    main()