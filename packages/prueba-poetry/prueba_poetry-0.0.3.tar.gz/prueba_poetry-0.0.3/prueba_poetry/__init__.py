product = (spark.read.format("PARQUET").load("/mnt/consumezone/Argentina/Commercial/FullDigital/AlgoSelling/Produccion/dimensiones/Product_distris").createOrReplaceTempView("product"))
