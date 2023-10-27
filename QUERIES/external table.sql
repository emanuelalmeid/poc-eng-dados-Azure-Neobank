IF NOT EXISTS (SELECT * FROM sys.external_file_formats WHERE name = 'SynapseParquetFormat') 
	CREATE EXTERNAL FILE FORMAT [SynapseParquetFormat] 
	WITH ( FORMAT_TYPE = PARQUET)
GO

IF NOT EXISTS (SELECT * FROM sys.external_data_sources WHERE name = 'gold_saneobankpocs_dfs_core_windows_net') 
	CREATE EXTERNAL DATA SOURCE [gold_saneobankpocs_dfs_core_windows_net] 
	WITH (
		LOCATION = 'abfss://gold@saneobankpocs.dfs.core.windows.net',
		CREDENTIAL = credencialneobank
	)
GO


CREATE EXTERNAL TABLE dbo.cliente (
	[RowNumber] nvarchar(4000),
	[CustomerID] nvarchar(4000),
	[Surname] nvarchar(4000),
	[CreditScore] nvarchar(4000),
	[Geography] nvarchar(4000),
	[Gender] nvarchar(4000),
	[Age] nvarchar(4000),
	[Tenure] nvarchar(4000),
	[Balance] nvarchar(4000),
	[NumOfProducts] nvarchar(4000),
	[HasCrCard] nvarchar(4000),
	[IsActiveMember] nvarchar(4000),
	[EstimatedSalary] nvarchar(4000),
	[Exited] nvarchar(4000)
	)
	WITH (
	LOCATION = '<location>t',
	DATA_SOURCE = [gold_saneobankpocs_dfs_core_windows_net],
	FILE_FORMAT = [SynapseParquetFormat]
	)
GO


SELECT TOP 100 * FROM dbo.cliente
GO