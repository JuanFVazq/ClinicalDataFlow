from pyspark.sql import SparkSession

def createSparkSesh() ->  SparkSession:
    return(SparkSession.builder.appName("Transformer").getOrCreate())

def main():
    spark = createSparkSesh()
    print(spark.version)
    spark.stop()

if __name__ == "__main__":
    main()