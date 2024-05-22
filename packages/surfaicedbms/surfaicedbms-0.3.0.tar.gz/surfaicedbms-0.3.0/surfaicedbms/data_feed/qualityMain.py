######################################################################################### workflow for quality data ingestion
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
######################################################################################### import modules
from surfaicedbms import dataProcessor
from surfaicedbms import mongoTransactions
from surfaicedbms import tsdbTransactions
from surfaicedbms import qualityApp


######################################################################################### initiate classes
tsdb = tsdbTransactions.TsdbTransactions()
mongo = mongoTransactions.MongoTransactions()
processor = dataProcessor.DataProcessor()
rarz = qualityApp.RaRz()

######################################################################################### find last workpiece
workpiece_ID = mongo.queryLastItem()
print(f"Workpiece ID: {workpiece_ID}")

######################################################################################### generate output for quality profiles and inspection id
inspectionId = processor.formQuality()
inspectionId = str(inspectionId)
print("Inspection ID:", inspectionId)
processor.formQuality()


######################################################################################### generate rarz output
output = rarz.node_calc_RaRz_static_window_size(4, inspectionId)
print("Output file has been produced")

######################################################################################### register output
tsdb.registerInspection(inspectionId)


######################################################################################### ingest output in tsdb
tsdb.ingestRarz()


######################################################################################### set inspection id in mongodb
mongo.setQuality(workpiece_ID, inspectionId)



