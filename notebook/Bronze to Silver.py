# Databricks notebook source
# DBTITLE 1,Library
from pyspark.sql.functions import desc, asc
from pyspark.sql.functions import when, split
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number

# COMMAND ----------

display(dbutils.fs.mounts())

# COMMAND ----------

# DBTITLE 1,Importing data
dfClientSRC = spark.read.csv("/mnt/saneobankpocs/bronze/NeoBank_Modelling.csv", header = True)


# COMMAND ----------

# DBTITLE 1,Only to run in the frist time (empty silver)
#dfClientSRC.coalesce(1).write.mode('overwrite').parquet(path="/mnt/saneobankpocs/silver/NeoBank_Modelling.parquet")
#lembrar de mudar no resto do código

# COMMAND ----------



dfClientTRG = spark.read.parquet("/mnt/saneobankpocs/silver/NeoBank_Modelling.parquet")

display(dfClientTRG)


# COMMAND ----------

dfClientSRC.filter(dfClientSRC.CustomerId == '15628319').show()

# COMMAND ----------

display(dfClientTRG)

# COMMAND ----------

# DBTITLE 1,Transforming
dfClientSRC = dfClientSRC.filter(dfClientSRC.IsActiveMember == 1)
print(dfClientSRC.columns)

# COMMAND ----------

dfClientSRC = dfClientSRC.withColumnRenamed('RowNumber','RowNumber_SRC')\
    .withColumnRenamed('CustomerID','CustomerID_SRC')\
    .withColumnRenamed('Surname','Surname_SRC')\
    .withColumnRenamed('CPF','CPF_SRC')\
    .withColumnRenamed('CEP','CEP_SRC')\
    .withColumnRenamed('CreditScore','CreditScore_SRC')\
    .withColumnRenamed('Geography','Geography_SRC')\
    .withColumnRenamed('Gender','Gender_SRC')\
    .withColumnRenamed('Age','Age_SRC')\
    .withColumnRenamed('Tenure','Tenure_SRC')\
    .withColumnRenamed('Balance','Balance_SRC')\
    .withColumnRenamed('NumOfProducts','NumOfProducts_SRC')\
    .withColumnRenamed('HasCrCard','HasCrCard_SRC')\
    .withColumnRenamed('IsActiveMember','IsActiveMember_SRC')\
    .withColumnRenamed('EstimatedSalary','EstimatedSalary_SRC')\
    .withColumnRenamed('Exited','Exited_SRC')\
    

# COMMAND ----------

dfClientTRG = dfClientTRG.withColumnRenamed('RowNumber','RowNumber_TRG')\
    .withColumnRenamed('CustomerID','CustomerID_TRG')\
    .withColumnRenamed('Surname','Surname_TRG')\
    .withColumnRenamed('CPF','CPF_TRG')\
    .withColumnRenamed('CEP','CEP_TRG')\
    .withColumnRenamed('CreditScore','CreditScore_TRG')\
    .withColumnRenamed('Geography','Geography_TRG')\
    .withColumnRenamed('Gender','Gender_TRG')\
    .withColumnRenamed('Age','Age_TRG')\
    .withColumnRenamed('Tenure','Tenure_TRG')\
    .withColumnRenamed('Balance','Balance_TRG')\
    .withColumnRenamed('NumOfProducts','NumOfProducts_TRG')\
    .withColumnRenamed('HasCrCard','HasCrCard_TRG')\
    .withColumnRenamed('IsActiveMember','IsActiveMember_TRG')\
    .withColumnRenamed('EstimatedSalary','EstimatedSalary_TRG')\
    .withColumnRenamed('Exited','Exited_TRG')\
    

# COMMAND ----------

# DBTITLE 1,Join
dfClientJoin = dfClientSRC.join(dfClientTRG,dfClientSRC.CustomerID_SRC == dfClientTRG.CustomerID_TRG, how= 'left')
display(dfClientJoin)

# COMMAND ----------

# DBTITLE 1,Novos Clientes
dfNewRegister = dfClientJoin.where('CustomerID_TRG is null')

dfNewRegister = dfNewRegister.select('RowNumber_SRC', 'CustomerID_SRC','Surname_SRC','CPF_SRC','CEP_SRC','CreditScore_SRC','Geography_SRC','Gender_SRC','Age_SRC', 'Tenure_SRC','Balance_SRC','NumOfProducts_SRC','HasCrCard_SRC','IsActiveMember_SRC','EstimatedSalary_SRC','Exited_SRC')
display(dfNewRegister)

# COMMAND ----------

display(dfNewRegister)

# COMMAND ----------

# DBTITLE 1,Update
dfUpdate = dfClientJoin.where('(CustomerId_SRC == CustomerId_TRG)'
                              'and (IsActiveMember_SRC == 1)'
                              'and (IsActiveMember_TRG == 1)'
                              )

dfUpdate = dfUpdate.where('(CreditScore_SRC != CreditScore_TRG)'
                          'or (Surname_SRC != Surname_TRG)'
                          'or (Geography_SRC != Geography_TRG)'
                          'or (Gender_SRC != Gender_TRG)'
                          'or (Age_SRC != Age_TRG)'
                          'or (Tenure_SRC != Tenure_TRG)'
                          'or (Balance_SRC != Balance_TRG)'
                          'or (NumOfProducts_SRC != NumOfProducts_TRG)'
                          'or (HasCrCard_SRC != HasCrCard_TRG)'
                          'or (IsActiveMember_SRC != IsActiveMember_TRG)'
                          'or (EstimatedSalary_SRC != EstimatedSalary_TRG)')

display(dfUpdate) 

dfUpdateInativar = dfUpdate
dfUpdate = dfUpdate.dropDuplicates(['CustomerID_SRC'])

# COMMAND ----------

dfUpdate = dfUpdate.select('RowNumber_SRC', 'CustomerID_SRC','Surname_SRC','CPF_SRC','CEP_SRC','CreditScore_SRC','Geography_SRC','Gender_SRC','Age_SRC', 'Tenure_SRC','Balance_SRC','NumOfProducts_SRC','HasCrCard_SRC','IsActiveMember_SRC','EstimatedSalary_SRC','Exited_SRC')

dfUpdateInativar = dfUpdateInativar.select('RowNumber_TRG', 'CustomerID_TRG','Surname_TRG','CPF_TRG','CEP_TRG','CreditScore_TRG','Geography_TRG','Gender_TRG','Age_TRG', 'Tenure_TRG','Balance_TRG','NumOfProducts_TRG','HasCrCard_TRG','IsActiveMember_TRG','EstimatedSalary_TRG','Exited_TRG')

dfUpdate.show()
dfUpdateInativar.show()


# COMMAND ----------

dfUpdateInativar = dfUpdateInativar.select('*').withColumn('IsActiveMember_TRG',when(dfUpdateInativar.IsActiveMember_TRG == '1', '0').otherwise(dfUpdateInativar.IsActiveMember_TRG))
display(dfUpdateInativar)

# COMMAND ----------

# DBTITLE 1,Unindo dataframe
dfmerge= dfClientTRG.unionAll(dfUpdateInativar)

# COMMAND ----------

dfmerge = dfmerge.withColumn('_row_number',row_number().over(Window.partitionBy('CustomerId_TRG').orderBy('IsActiveMember_TRG')))
display(dfmerge.filter(dfmerge.CustomerID_TRG == '15628319'))

# COMMAND ----------

if dfUpdateInativar.isEmpty:
    dfmerge = dfmerge
else:
    dfmerge = dfmerge.select('*').where('_row_number == 1 '
                                        'or (IsActiveMember_TRG == 0)'
                                        )
display(dfmerge)

# COMMAND ----------

display(dfmerge.filter(dfmerge.CustomerID_TRG == '15628319'))

# COMMAND ----------

# DBTITLE 1,Apagar coluna auxiliar
dfmerge = dfmerge.drop('_row_number')
dfmerge.show()

# COMMAND ----------

dfmerge.show()

# COMMAND ----------

# DBTITLE 1,Acrescentar novos + registros + update 
dfversionfinal = dfmerge.unionAll(dfNewRegister).unionAll(dfUpdate)

# COMMAND ----------

dfversionfinal = dfversionfinal.withColumnRenamed('RowNumber_TRG','RowNumber')\
    .withColumnRenamed('CustomerID_TRG','CustomerID')\
    .withColumnRenamed('Surname_TRG','Surname')\
    .withColumnRenamed('CPF_TRG','CPF')\
    .withColumnRenamed('CEP_TRG','CEP')\
    .withColumnRenamed('CreditScore_TRG','CreditScore')\
    .withColumnRenamed('Geography_TRG','Geography')\
    .withColumnRenamed('Gender_TRG','Gender')\
    .withColumnRenamed('Age_TRG','Age')\
    .withColumnRenamed('Tenure_TRG','Tenure')\
    .withColumnRenamed('Balance_TRG','Balance')\
    .withColumnRenamed('NumOfProducts_TRG','NumOfProducts')\
    .withColumnRenamed('HasCrCard_TRG','HasCrCard')\
    .withColumnRenamed('IsActiveMember_TRG','IsActiveMember')\
    .withColumnRenamed('EstimatedSalary_TRG','EstimatedSalary')\
    .withColumnRenamed('Exited_TRG','Exited')


# COMMAND ----------

dfversionfinal.filter(dfversionfinal.CustomerID == '15628319').show()

# COMMAND ----------

dfversionfinal.coalesce(1).write.mode('overwrite').parquet(path="/mnt/saneobankpocs/silver/NeoBank_Modelling.parquet")

# COMMAND ----------



# COMMAND ----------

