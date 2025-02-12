dbutils.secrets.list(scope = "dbrSeAzKv")
storage_account_key = dbutils.secrets.get(scope = "dbrSeAzKv", key = "s-adls")
storage_account_name = "dlgen2forproj"
container_name = "bronze"
transformed_container_name = "silver"
output_path = f"abfss://{transformed_container_name}@{storage_account_name}.dfs.core.windows.net"

dbutils.widgets.text("fileName","")
fileName = dbutils.widgets.get("fileName")

from pyspark.sql import SparkSession
# Set up the configuration for accessing the storage account
spark.conf.set(f"fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", storage_account_key)

# Reading the data 
filePath = f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{fileName}"

df = spark.read.format("csv").\
    option("header", "true").\
        option("inferSchema", "true").\
            load(filePath)



# This function checks for missing values in the dataset and replaces them with 0

from pyspark.sql.functions import col

def replace_missing_values(df):

    columns = df.columns
    missing_values_condition = col(columns[0]).isNull()
    for col_name in columns[1:]:
        missing_values_condition = missing_values_condition | col(col_name).isNull()

    missing_values_df = df.filter(missing_values_condition)

    if missing_values_df.count() > 0:
        print("Rows with missing values:")
        missing_values_df.show()
        # fill missing values with 0
        df_cleaned = df.fillna(0,subset=columns)

    else:
        print("No rows with missing values found.")
        df_cleaned = df
    
    
    return df_cleaned


from pyspark.sql import functions as F

def check_and_remove_duplicates(df):
    
    columns = df.columns

    # Count the number of duplicate rows
    duplicates_df = df.groupBy(columns).count().filter(F.col("count") > 1)
    

    if duplicates_df.count() > 0:

        # Join the original DataFrame with the duplicate DataFrame

        duplicate_rows = df.join(duplicates_df.select(columns), on=columns, how="inner")
        
         # Remove duplicates across all columns
    
        print("Data after removing duplicates:")
        df_cln = df.dropDuplicates()
        df_final = df_cln.orderBy("date","store_nbr")

        
    else:
        print("No duplicate rows found.")
        df_final = df

    return df_final

df_cleaned1 = replace_missing_values(df)  
df_cleaned2 = check_and_remove_duplicates(df_cleaned1)
from pyspark.sql import functions as F

if fileName == "dbo.items.txt" : 
    df_items = df_cleaned2

    df_items_final = df_items.withColumn("is_perishable", F.when(F.col("perishable") == True, "Yes").otherwise("No")).\
        drop("perishable").\
            withColumn("family",F.lower(F.col("family")))

    df_items_final.write.mode("overwrite").parquet(output_path+"/items")


if fileName == "holidays_events.csv" :
    df_holidays = df_cleaned2

    df_holidays_final = df_holidays.withColumn("type", F.lower(F.col("type"))).\
        withColumn("transferred_holiday", F.when(F.col("transferred") == True, "Yes").\
            otherwise("No")).drop("transferred").\
                withColumn("day_of_week", F.date_format(F.col("date"), "EEEE")).\
                    withColumn("is_weekend", F.when(F.col("day_of_week").isin("Saturday", "Sunday"), "Yes").otherwise("No"))
    
  

    df_holidays_final.write.mode("overwrite").parquet(output_path+"/holidays")
    
if fileName == "oil.csv" :
    df_oil = df_cleaned2
    df_final_oil = df_oil.withColumnRenamed("dcoilwtico", "daily_wti_oil_price")
    df_final_oil.show()


    df_final_oil.write.mode("overwrite").parquet(output_path+"/oil")
if fileName == "stores.csv" :
    df_stores = df_cleaned2
    df_stores_final = df_stores.withColumn("city", F.lower(F.col("city"))).\
        withColumn("state", F.lower(F.col("state"))).\
            withColumn("Store_Category",F.when(F.col("type") == "A", "Large Store")
                       .when(F.col("type") == "B", "Medium Store")
                        .when(F.col("type") == "C", "Small Store")
                        .when(F.col("type") == "D", "Specialty Store"))
    

    df_stores_final.write.mode("overwrite").parquet(output_path+"/stores")
if fileName == "transactions.csv" :
    df_transactions = df_cleaned2
    df_transactions_final = df_transactions.withColumn("day_of_week",F.date_format(F.col("date"), "EEEE"))


    df_transactions_final.write.mode("overwrite").parquet(output_path+"/transactions")
