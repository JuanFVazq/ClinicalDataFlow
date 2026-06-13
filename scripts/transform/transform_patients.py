from pyspark.sql import SparkSession
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_PATIENT_PATH = PROJECT_ROOT/"data"/"raw"/"fhir_api"/"patient"

def createSparkSesh() ->  SparkSession:
    return(SparkSession.builder.appName("Transformer").getOrCreate())






def main():
    spark = createSparkSesh()
    patientFiles = list(RAW_PATIENT_PATH.glob("*.json"))
    rawBundleDF = (spark.read.option("multiline", "true").json([str(file) for file in patientFiles]))

    rawBundleDF.printSchema()


    print(spark.version)
    spark.stop()






if __name__ == "__main__":
    main()