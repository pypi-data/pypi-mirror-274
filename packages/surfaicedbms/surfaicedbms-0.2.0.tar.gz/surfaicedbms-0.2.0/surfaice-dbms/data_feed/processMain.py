########################################################################################################### workflow for process data ingestion
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
################################################################################ import modules
from surfaicedbms import dataProcessor
from surfaicedbms import mongoTransactions
from surfaicedbms import tsdbTransactions
from surfaicedbms import edgeApp

################################################################################ initiate classes
tsdb=tsdbTransactions.TsdbTransactions()
edge = edgeApp.EdgeApplication()
processor = dataProcessor.DataProcessor()
mongo = mongoTransactions.MongoTransactions()


################################################################################ find last ingested workpiece id
workpiece_ID = mongo.queryLastItem()
print(f"Workpiece ID: {workpiece_ID}")

################################################################################ generate output from edge application
data = edge.mock_data()
processId, fake_metadata, fake_rawdata= data
print(f"Process ID: {processId}")
processor.formRawData(fake_rawdata, workpiece_ID)
print("Raw data has been formed")
processedMetaData = processor.formMetaData(fake_metadata, processId)
print("Meta data has been formed")

################################################################################ ingest raw data
tsdb.ingestAcc()
tsdb.ingestNc()

################################################################################ process id has been registered
tsdb.registerProcess(processId)

################################################################################ ingest meta data
tsdb.ingestManufacturingOperations()

################################################################################ set process data in mongo db
mongo.setProcess(workpiece_ID,processId)
queryArray = mongo.queryMaterialRemovalByToolAll()
mongo.setToolTotalMr(queryArray)
print("total material removal of tools have been set")












