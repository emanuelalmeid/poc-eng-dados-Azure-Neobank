# Databricks notebook source
display(dbutils.fs.mounts())
dfClientSRC = spark.read.parquet("/mnt/saneobankpocs/silver/NeoBank_Modelling.parquet", header = True)
display(dfClientSRC)

# Remove secret columns

 dfClientSRC = dfClientSRC.drop('CEP','CPF')
 display(dfClientSRC)

# COMMAND ----------

dfClientSRC.coalesce(1).write.mode('overwrite').parquet(path="/mnt/saneobankpocs/gold/NeoBank_Modelling.parquet")



# COMMAND ----------

