	# nx: threaded
from IFT.IFTTool import IFTToolCollection, IFTTool
from IFT.IFTBase import IFTCore, IFTCAMSetup
from IFT.IFTPDF import IFTPDF
from surfaicedbms import nxOperations
from surfaicedbms import mongoTransactions
from surfaicedbms import tsdbTransactions
from datetime import datetime
import time
import os

env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
root_path =  os.getenv(env_name_root)
storage_dir = root_path + "data\\outputs\\workpieceOutput"

########################################################################### script info
autor = "Atahan Kap"
autor_email = "e1129028@student.tuwen.ac.at"
last_changed = "2023_02_04"


########################################################################### starting data export
nx = nxOperations.NxOperations()
mongo = mongoTransactions.MongoTransactions()
tsdb = tsdbTransactions.TsdbTransactions()
print_nx = IFTCore.print_nx
nx_logger = IFTCore.nx_logger
IFTCore.emphasize()
IFTCore.print_nx("STARTING WITH DATA EXPORT")

########################################################################### generate cam setup instance
cam_setup = nx.camSetupInstance()

IFTCore.emphasize()
IFTCore.print_nx("CAM SETUP INSTANCE HAS BEEN GENERATED")

########################################################################### generate tools object
toolData, toolIds = nx.generateTool()

IFTCore.emphasize()
IFTCore.print_nx("TOOLS OBJECT HAS BEEN GENERATED")

########################################################################### generate machining part object
machiningPartsData = nx.generateMachiningPart()
IFTCore.emphasize()
IFTCore.print_nx("MACHINING PART OBJECT HAS BEEN GENERATED")

########################################################################### generate machine object
machine, machineData = nx.generateMachine()
IFTCore.emphasize()
IFTCore.print_nx("MACHINE OBJECT HAS BEEN GENERATED")


########################################################################### generate design feature object
designFeaturesData = nx.generateDesignFeatures()
IFTCore.emphasize()
IFTCore.print_nx("DESIGN FEATURE OBJECT HAS BEEN GENERATED")

########################################################################### generate machining feature object
machiningFeaturesData = nx.generateMachiningFeatures()
IFTCore.emphasize()
IFTCore.print_nx("MACHINING FEATURE OBJECT HAS BEEN GENERATED")

########################################################################### generate a g-code object and save it to output folder
nc_post, nc_dir = nx.generateGcode(machine)
IFTCore.emphasize()
IFTCore.print_nx(f"G-CODE OBJECT HAS BEEN GENERATED AND SAVED IN: {nc_dir}")

########################################################################### arrange data structure
post = nx.generatePost(cam_setup, machiningPartsData, machineData, toolIds, nc_post, designFeaturesData, machiningFeaturesData)
workpiece_ID = post['_id']
########################################################################### save post as a json file
nx.savePost(post)

########################################################################### logger

logger = nx.createLogger(workpiece_ID)
creator = "user_planning"

########################################################################### register id metadata
editor = str(post["editor"])
tsdb.registerIdMetaData(workpiece_ID, editor, logger)
IFTCore.emphasize()
IFTCore.print_nx("ID METADATA HAS BEEN REGISTERED")
IFTCore.emphasize()

########################################################################### register machine

current_time=datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

machineIdList = mongo.machineIdQuery()
if machineData["_id"] not in machineIdList:
	mongo.registerMachine(machineData, logger)
	IFTCore.emphasize()
	IFTCore.print_nx("Machine is registered to Mongo DB")
	tsdb.registerMachine(machineData, current_time, creator, logger)
	IFTCore.emphasize()
	IFTCore.print_nx("Machine is registered to items table")
else:
	IFTCore.emphasize()
	IFTCore.print_nx("Machine is already registered")


########################################################################### register machining part
	
machiningPartIdList = mongo.machiningPartIdQuery()

for i in range(len(machiningPartsData)):
	if machiningPartsData[i]["_id"] not in machiningPartIdList:
		mongo.registerMachiningPart(machiningPartsData[i], logger)
		IFTCore.emphasize()
		IFTCore.print_nx("Machining part is registered to Mongo DB")
	else:
		IFTCore.emphasize()
		IFTCore.print_nx("Machining part is already registered")

########################################################################### register tool
toolIdList = mongo.toolIdQuery()
for i in range(len(toolData)):
	if toolData[i]["_id"] not in toolIdList:
		mongo.registerTool(toolData[i], logger)
		IFTCore.emphasize()
		IFTCore.print_nx("Tool: "+ str(toolData[i]["_id"]) + " is registered to Mongo DB")
		tsdb.registerTool(str(toolData[i]["_id"]), current_time, creator, logger)
		IFTCore.emphasize()
		IFTCore.print_nx("Tool: "+ str(toolData[i]["_id"]) + " is registered to items table")
	else:
		IFTCore.emphasize()
		IFTCore.print_nx("Tool: "+ str(toolData[i]["_id"]) + " is already registered")

########################################################################### import cam setup as prt file
camSetupId = post["planningData"]["CAM"]["camSetupId"]														## get cam setup id
camSetupPath = root_path + "\data\inputs\camSetup\\" + str(camSetupId) + ".prt"								## Change if new cam setup comes

prtIdList = mongo.prtIdQuery()
if camSetupId not in prtIdList:
	mongo.importCamPrt(camSetupPath, camSetupId, logger)
	IFTCore.emphasize()
	IFTCore.print_nx("PRT-File of CAM Setup is saved to Mongo DB")
else:
	IFTCore.emphasize()
	IFTCore.print_nx("PRT-File of CAM Setup is already saved to Mongo DB")

########################################################################### import 3dPdf
	

outputPath = root_path + "\data\outputs\\3dPdf" 
pdfIdList = mongo.pdfIdQuery()
if camSetupId not in pdfIdList:
	tool_collection = IFTToolCollection()
	pdfDir = outputPath + f"\\3D_{camSetupId}.pdf"	
	IFTPDF.export_cam_pdf(tool_collection, pdfDir)
	mongo.import3DPdf(pdfDir, camSetupId, logger)
	IFTCore.emphasize()
	IFTCore.print_nx("PDF-File of CAM Setup is saved to Mongo DB")
else:
	IFTCore.emphasize()
	IFTCore.print_nx("PDF-File of CAM Setup is already saved to Mongo DB")


########################################################################### query total material removal
queryTool = mongo.queryMaterialRemovalByToolAll()

IFTCore.emphasize()
IFTCore.print_nx("TOTAL MATERIAL REMOVAL BY TOOL ID OF DOCUMENTS WITH PROCESS ID")
IFTCore.emphasize()

for i in range(len(queryTool)):
	IFTCore.emphasize()
	IFTCore.print_nx("Tool ID: " + str(queryTool[i]['_id']))
	IFTCore.print_nx("Total Material Removal: " + str(queryTool[i]['total_mr']))
	IFTCore.emphasize()

########################################################################### register id metadata

mongo.ingestWorkpiece(post, logger)
IFTCore.emphasize()
IFTCore.print_nx("WORKPIECE HAS BEEN INGESTED")
IFTCore.emphasize()

########################################################################### query total material removal by operation id for current planning data acquisition
query = mongo.queryMaterialRemovalByOperation(workpiece_ID)

IFTCore.emphasize()
IFTCore.print_nx("MATERIAL REMOVAL BY OPERATION ID FOR CURRENT PLANNING DATA EXPORT")
IFTCore.emphasize()

for i in range(len(query)):
	IFTCore.emphasize()
	IFTCore.print_nx("Operation ID: " + str(query[i]['_id']))
	IFTCore.print_nx("Total Material Removal: " + str(query[i]['total_mr']))
	IFTCore.emphasize()

IFTCore.emphasize()
IFTCore.print_nx("DATA EXPORT FINISHED")
IFTCore.emphasize()