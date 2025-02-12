# Corporación Favorita Grocery Sales Data Pipeline  
**End-to-End Data Engineering Project with Azure**  

**Overview:**
   An end-to-end data pipeline leveraging Azure Data Lake Storage (ADLS Gen2), Azure Databricks (PySpark), and Azure Data Factory (ADF) to ingest, transform, and analyze grocery sales data, with a Power BI 
   dashboard for actionable business insights.

## 🛠️ **Tools & Technologies**  
| **Stage**         | **Tools**                                  |
|--------------------|--------------------------------------------|
| **Data Ingestion** | Azure Data Lake Storage (ADLS) Gen2        |
| **Transformation** | PySpark (Azure Databricks)                 |
| **Orchestration**  | Azure Data Factory (ADF)                   |
| **Warehousing**    | Azure Synapse                              |




**Azure Architecture Diagram**
![**Azure Architecture Diagram**](screenshots/diagram.PNG)

## 📊 Dataset Source  
The raw dataset used in this project is available here:  

📂 [**Raw Data Files**](data/raw_data)  

🔹 Above folder contains the original CSV files sourced from [Kaggle](https://www.kaggle.com/datasets/ruiyuanfan/corporacin-favorita-grocery-sales-forecasting).  
🔹 These files include **sales transactions, store information, item details, holiday events, and oil price data**.  
🔹 You can download them directly from this repository without needing a Kaggle account.  


## 🚀 Data Ingestion Process

To ensure a **fully automated and dynamic data ingestion pipeline**, this project leverages **Azure Data Factory (ADF), Azure SQL Database, and Azure Data Lake Storage Gen2 (ADLS Gen2)**. The ingestion pipeline is designed to handle **multiple data sources dynamically** using **parameters**, making it flexible and scalable.

### 🔹 Pipeline Design
![**Ingestion Pipeline**](screenshots/PL_ingestion.PNG)

1️⃣ **Metadata-Driven Ingestion**  
   - The paths for all **data sources** are stored in an **Azure SQL Database** table. [](screenshots/metadataTable_sql.PNG) 
   - This table contains a **Path column**, which holds the source location of each dataset. [](screenshots/metadataTable.PNG) 
   - The ingestion process dynamically retrieves these paths and processes the data accordingly.

2️⃣ **Lookup & Iteration**  
   - The pipeline starts with a **Lookup Activity (metaDataLookup)** that retrieves the source paths from Azure SQL Database.  
   - A **ForEach Activity (ForEachFile)** iterates through each retrieved path.

3️⃣ **Dynamic Source Selection**  
   - Inside the `ForEach` loop, a **Switch Activity (SwitchSourceType)** dynamically selects the appropriate source type.  
   - This allows the pipeline to handle **multiple source types without hardcoding paths**.

4️⃣ **Data Movement & Storage**  
   - Based on the source type, the **Copy Activity (CopySqlSrv)** moves the data to **Azure Data Lake Storage Gen2 (ADLS Gen2)**.  
   - The pipeline supports **multiple data sources**, including:  
     ✔ **Azure File Share**  
     ✔ **Azure Blob Storage**  
     ✔ **On-Premises SQL Server**  

### 📸 Pipeline Workflow  
<!-- Replace 'pipeline_image.png' with the actual filename of your uploaded image -->
![Data Ingestion Pipeline](pipeline_image.png)

### ✅ Key Benefits of This Approach  
✔ **Automated & Scalable** → No manual intervention needed; new sources can be added dynamically.  
✔ **Metadata-Driven** → Azure SQL Database controls the ingestion process.  
✔ **Multi-Source Support** → Handles data from different sources seamlessly.  
✔ **Optimized for Cloud Storage** → Stores all ingested data in **ADLS Gen2** for further processing.  

This **ingestion pipeline** serves as the **foundation** for the data engineering workflow, ensuring a **robust, scalable, and flexible** solution for managing diverse data sources. 🚀  





  





  
2. **Transformation**:  
   - PySpark code in Databricks cleans and aggregates data (e.g., filtering nulls, joining tables).  
3. **Orchestration**:  
   - ADF pipelines automate data movement from ADLS to Databricks.  
4. **Analysis**:  
   - Mock Power BI dashboard created locally due to Azure account restrictions.  

💡 **Tip**: Replace `adf_pipeline.png` with your actual screenshot filename. Add a 1-2 line description for each stage.

---

## 🔍 **Key Screenshots & Code Snippets**  

### 1. **ADLS Gen2 Configuration**  
![ADLS Folders](pipelines/screenshots/adls_config.png)  
*Raw and transformed data folders in Azure Data Lake Storage.*  

### 2. **PySpark Transformation Code**  
```python  
# Load raw transactions data from ADLS Gen2 (example)
transactions_df = spark.read.csv("adls://raw/transactions.csv")

# Clean data: Remove nulls and filter valid sales
clean_df = transactions_df.dropna().filter("sales_amount > 0")

# Write transformed data to ADLS Gen2 in Parquet format
clean_df.write.parquet("adls://transformed/clean_transactions.parquet")
