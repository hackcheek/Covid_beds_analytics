from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.utils import AnalysisException


def spark_session() -> SparkSession:

    if SparkSession.getActiveSession():
        return SparkSession.getActiveSession()

    else:
        spark: SparkSession = (
            SparkSession
            .builder
            .master("local")
            .appName("Proyecto individual #2")
            .config('spark.driver.host', '127.0.0.1')
            .config('spark.driver.bindAddress', '127.0.0.1')
            .config("spark.ui.port", "4040")
            .getOrCreate()
        )
        return spark


def updata(spark: SparkSession) -> DataFrame:

    data: DataFrame = spark.read.csv(
        "./datasets/COVID-19_Reported_Patient_Impact_and_Hospital_Capacity_by_State_Timeseries.csv",
        header=True,
    )

    try:
        spark.sql("SELECT * FROM data")

    except AnalysisException:
        data.registerTempTable("data")

    return data
