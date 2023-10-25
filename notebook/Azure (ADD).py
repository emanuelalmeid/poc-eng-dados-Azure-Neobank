# Databricks notebook source
application_id = "<a.id>"
tenant_id = "<tenant.id>"
client_secret = "<c.s>"

storage_account_name = "saneobankpocs"
container = "bronze"
container2 = "gold"
container3 = "silver"

# COMMAND ----------

configs = {"fs.azure.account.auth.type": "OAuth",
          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
          "fs.azure.account.oauth2.client.id": f"{application_id}",
          "fs.azure.account.oauth2.client.secret": f"{client_secret}",
          "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"}

# COMMAND ----------

dbutils.fs.mount(
  source = f"abfss://{container}@{storage_account_name}.dfs.core.windows.net/",
  mount_point = f"/mnt/{storage_account_name}/{container}",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.mount(
  source = f"abfss://{container2}@{storage_account_name}.dfs.core.windows.net/",
  mount_point = f"/mnt/{storage_account_name}/{container2}",
  extra_configs = configs)

# COMMAND ----------

dbutils.fs.mount(
  source = f"abfss://{container3}@{storage_account_name}.dfs.core.windows.net/",
  mount_point = f"/mnt/{storage_account_name}/{container3}",
  extra_configs = configs)

# COMMAND ----------

display(dbutils.fs.mounts())