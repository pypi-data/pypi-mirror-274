from pymongo import MongoClient, InsertOne
from gridfs import GridFS
import os
from pymongo.errors import PyMongoError, WriteError
import yaml
import json


def load_config(config_file):
    """
    This function helps loading configuration file for accessing database connection related data
    Input: 		Directory of config.yaml file

    Output:		Case 1:	Readen configuration file
                Case 2: None
    """
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print("Error loading the configuration:", exc)
            return None

env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
config = load_config(config_path)
root_path =  os.getenv(env_name_root)



def connectMongo():
    """
    connectMongo function is used for connecting MongoDB database
    Input: 		None

    Output: 	Case 1:	- client						                ... a client instance in case its necessary
    					- db_surfaice					                ... a surfaice database instance for database related operations
    					- db_cam						                ... a cam database instance for database related operations
    					- dn_pdf						                ... a pdf database instance for database related operations
    			Case 2: None
    """
    db_surfaice = None
    db_cam = None
    db_pdf = None
    client = None
    try:
        user=config['databases']['mongoUser']
        password=config['databases']['mongoPassword']
        cluster_name=config['databases']['mongoCluster']
        connectionString=config['databases']['mongoString']
        connection_string = f"mongodb+srv://{user}:{password}@{cluster_name}.{connectionString}"
        client=MongoClient(connection_string)
        db_cam=client["CAM_Setups"]
        db_surfaice=client["Surfaice"]
        db_pdf=client["3D-PDF"]
    except PyMongoError as e:
        print(e)
    return client, db_surfaice, db_cam, db_pdf


client, db_surfaice, db_cam, db_pdf = connectMongo()
collection_workpiece=db_surfaice["Workpieces"]
collection_tools=db_surfaice["Tools"]
collection_pdf=db_pdf["fs.files"]


class MongoTransactions:

#################################################################################################################################################### UPDATE FUNCTIONS

    def setProcess(self,  WorkpieceID, process_id):
        """
        This function finds the document with a given workpiece id Workpieces collection of db_surfaice database,
        and appends a process id to link this document to the data, which is related to manufactuing process
        Input:              - WorkpieceID                                       ... workpiece id to search
                            - process_id                                        ... inspection id of quality data
        Output:             - appended process id in case of no errors
        """
        collection = db_surfaice["Workpieces"]
        filter_criteria = {'_id': WorkpieceID}
        update_query = {'$set': {'processData.processId': process_id}}
        try:
            collection.update_one(filter_criteria, update_query)
            print('Process data has been set')
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

    def setToolTotalMr(self, queryArray):
        """
        This function is used for updating total material removal fields documents in toolData collection of db_surfaice database.
        The function can not be used without queryMaterialRemovalByTool() method, there it uses the query results of that method.
        It is important to use this function only, when a real manufacturing process takes place. Therefore only in processMain script.
        Input:              - queryArray                                        ... query result of queryMaterialRemovalByTool() method. This results data format is a list with elements in form of dictionaries.
                                                                                These elements contain two data fields regarding id and total material removal of every tool used in manufacturing processes
        Output:             - updated total material removal field in case of no errors
        """
        for i in range(len(queryArray)):
            toolId = {'_id':queryArray[i]['_id']}
            setTotalMr = {'$set' : {'totalMaterialRemoval': queryArray[i]['total_mr']}}
            try:
                collection_tools.update_one(toolId, setTotalMr)
                print(f"total material removal for tool: {toolId['_id']} has been set")
            except PyMongoError as e:
                print(f"MongoDB error: {e}")

    def setQuality(self,  WorkpieceID, inspection_id):
        """
        This function finds the document with a given workpiece id Workpieces collection of db_surfaice database,
        and appends an inspection id to link this document to the data, which is related to quality measurements
        Input:              - WorkpieceID                                       ... workpiece id to search
                            - inspection_id                                     ... inspection id of quality data
        Output:             - appended inspection id in case of no errors
        """
        collection = db_surfaice["Workpieces"]
        filter_criteria = {'_id': WorkpieceID}
        update_query = {'$set': {'qualityData.inspectionId': inspection_id}}
        try:
            collection.update_one(filter_criteria, update_query)
            print('Quality data has been set')
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

#################################################################################################################################################### IMPORT OF OBJECTS

    def ingestWorkpiece(self, post, logger):
        """
        This function is used for inserting a new document to Workpieces collection of db_surfaice database.
        This document includes planning data regarding manufacturing process of workpiece after ingestion.
        processData and qualiyData fields will be loaded after setProcess and setQuality functions are applied.
        Input:              - post                                   ... an object, which reflects the concerted data model for surfaice project. This data model is generated in planningMain script.
                            - logger                                 ... logger instance for recording
        Output:             - new entry in Workpieces collection in case no error occurs
        """
        collection_workpiece = db_surfaice["Workpieces"]
        try:
            collection_workpiece.insert_one(post)
            logger.info('Workpiece has been ingested')
        except PyMongoError as e:
            logger.error(f"{e}")

    def registerMachine(self, machineData, logger):
        """
        This function is used for registering machine related data to Machines collection of db_surfaice database
        Input:              - machineData                            ... machine object generated through nx export
                            - logger                                 ... logger instance for recording
        Output:             new entry in Machines collection in case no error occurs
        """
        collection_machines = db_surfaice["Machines"]
        try:
            collection_machines.insert_one(machineData)
            logger.info('Machine has been registered to Machines Collection')
        except PyMongoError as e:
            logger.error(e)


    def registerMachiningPart(self, machiningPartsData, logger):
        """
        This function is used for registering machining part related data to MachiningParts collection of db_surfaice database
        Input:              - machiningPartsData                      ... machining part object generated through nx export
                            - logger                                  ... logger instance for recording
        Output:             new entry in MachiningParts collection in case no error occurs
        """
        collection_machiningpart = db_surfaice["MachiningParts"]
        try:
            collection_machiningpart.insert_one(machiningPartsData)
            logger.info('MachiningPart has been registered to MachiningParts Collection')
        except PyMongoError as e:
            logger.error(e)


    
    def registerTool(self, toolData, logger):
        """
        This function is used for registering tool related data to Tools collection of db_surfaice database
        Input:              - toolData                               ... tool object generated through nx export
                            - logger                                 ... logger instance for recording
        Output:             new entry in Tools collection in case no error occurs
        """
        collection_tools = db_surfaice["Tools"]	
        try:
            collection_tools.insert_one(toolData)
            logger.info('Tool has been registered to Tools Collection')
        except PyMongoError as e:
            logger.error(e)


#################################################################################################################################################### IMPORT EXPORT RELATED FUNCTIONS
    def exportWorkpiece(self, workpiece_id, planning_folder):
        document = collection_workpiece.find_one({"_id": workpiece_id})
        if document:
            filename = f"{planning_folder}/{workpiece_id}.json"
            with open(filename, "w") as file:
                json.dump(document, file, indent=4)
            print(f"Workpiece with _id '{workpiece_id}' has been downloaded in '{filename}'")
        else:
            print(f"No document found with _id '{workpiece_id}'")

    def import3DPdf(self, pdfDir, camSetupId, logger):
        """
        This function is used for uploading a pdf file to db_pdf database, where cam setup pdfs are stored.
        Additionally cam setup id is also appended to the document to ease the queries.
        Input:              - pdfDir                                   ... directory of file to upload
                            - camSetupId                               ... id of cam setup
                            - logger                                   ... logger instance for recording
        Output:             new entry in db_pdf in case no error occurs
        """
        fs = GridFS(db_pdf)
        additional_data={"_id":camSetupId}
        try:
            with open(pdfDir, "rb") as f:
                contents = f.read()
                fs.put(contents, **additional_data)
                print("file uploaded")
                logger.info('CAM-Setup has been ingested')
        except PyMongoError as e:
            logger.error(f"{e}")

    def importCamPrt(self, path, camSetupId, logger):
        """
        This function is used for uploading a prt file to db_cam database, where cam setup prt files are stored.
        Additionally cam setup id is also appended to the document to ease the queries.
        Input:              - path                                     ... directory of file to upload
                            - camSetupId                               ... id of cam setup
                            - logger                                   ... logger instance for recording
        Output:             new entry in db_cam in case no error occurs
        """
        fs = GridFS(db_cam)
        additional_data={"_id":camSetupId}
        try:
            with open(path, "rb") as f:
                contents = f.read()
                fs.put(contents, **additional_data)
                print("file uploaded")
                logger.info('CAM-Setup has been ingested')
        except PyMongoError as e:
            logger.error(f"{e}")


    def exportPrt(self, camSetupId, planning_folder):
        """
        This function is is used for exporting prt files of a certain cam setup.
        Input:      - camSetupId                               ... id of cam setup
                    - output_path                              ... directory of folder to download the file

        Output:     camSetupId.prt in given directory in case no error occurs

        """
        fs = GridFS(db_cam)
        query = {"_id": camSetupId}
        try:
            document = db_cam["fs.files"].find_one(query)
            file = fs.get(document["_id"])
            save_path = planning_folder + f"\\{camSetupId}.prt"
            with open(save_path, "wb") as f:
                f.write(file.read())
            print(f"File has been downloaded to {save_path}")
        except PyMongoError as e:
            print(e)


    def exportPdf(self, camSetupId, planning_folder):
        """
        This function is is used for exporting pdf files of a certain cam setup.
        Input:      - camSetupId                               ... id of cam setup
                    - output_path                              ... directory of folder to download the file

        Output:     camSetupId.pdf in given directory in case no error occurs

        """
        fs = GridFS(db_pdf)
        query = {"_id": camSetupId}
        try:
            document = db_pdf["fs.files"].find_one(query)
            file = fs.get(document["_id"])
            save_path = planning_folder + f"\\{camSetupId}.pdf"
            with open(save_path, "wb") as f:
                f.write(file.read())
            print(f"File has been downloaded to {save_path}")
        except PyMongoError as e:
            print(e)


#################################################################################################################################################### QUERIES
    def findCamSetupId(self, workpiece_id):
        camSetupId = None
        proId = [
            {"$match": {"_id": workpiece_id}},
            {"$project": {"planningData.CAM.camSetupId": 1}}
        ]
        try:
            result = collection_workpiece.aggregate(proId)
            for item in result:
                camSetupId = item['planningData']['CAM']['camSetupId']
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return camSetupId


    def findProcessId(self, workpiece_id):
        processId = None
        proId = [
            {"$match": {"_id": workpiece_id}},
            {"$project": {"processData.processId": 1}}
        ]
        try:
            result = collection_workpiece.aggregate(proId)
            for item in result:
                processId = item['processData']['processId']
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return processId

    def findInspectionId(self, workpiece_id):
        inspectionId = None
        inspId = [
            {"$match": {"_id": workpiece_id}},
            {"$project": {"qualityData.inspectionId": 1}}
        ]
        try:
            result = collection_workpiece.aggregate(inspId)
            for item in result:
                inspectionId = item['qualityData']['inspectionId']
        except PyMongoError as e:
                print(f"MongoDB error: {e}")
        return inspectionId

    def pdfIdQuery(self):
        """
        This function queries fs.files collection of db_pdf database for pdf file ids and returns a list of ids.
        Input:              None
        Output:             pdfIdList of resulting ids, in case no error occurs
        """
        collection_pdf = db_pdf["fs.files"]
        pdfIdList = None
        try:
            pdfIdQuery = collection_pdf.find({}, {"_id": 1})
            pdfIdList = [doc["_id"] for doc in pdfIdQuery]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return pdfIdList

    def prtIdQuery(self):
        """
        This function queries fs.files collection of db_cam database for prt file ids and returns a list of ids.
        Input:              None
        Output:             prtIdList of resulting ids, in case no error occurs
        """
        collection_prt = db_cam["fs.files"]
        prtIdList = None
        try:
            prtIdQuery = collection_prt.find({}, {"_id": 1})
            prtIdList = [doc["_id"] for doc in prtIdQuery]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return prtIdList

    def toolIdQuery(self):
        """
        This function queries Tools collection of db_surfaice database for tool ids and returns a list of ids.
        Input:              None
        Output:             toolIdList of resulting ids, in case no error occurs
        """
        collection_machiningparts = db_surfaice["Tools"]
        toolIdList = None
        try:
            toolIdQuery = collection_machiningparts.find({}, {"_id": 1})
            toolIdList = [doc["_id"] for doc in toolIdQuery]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return toolIdList

    def machiningPartIdQuery(self):
        """
        This function queries MachiningParts collection of db_surfaice database for machining part ids and returns a list of ids.
        Input:              None
        Output:             machiningPartIdList of resulting ids, in case no error occurs
        """
        collection_machiningparts = db_surfaice["MachiningParts"]
        machiningPartIdList = None
        try:
            machiningPartIdQuery = collection_machiningparts.find({}, {"_id": 1})
            machiningPartIdList = [doc["_id"] for doc in machiningPartIdQuery]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return machiningPartIdList

    def queryLastItem(self):
        """
        This function queries Workpieces collection of db_surfaice database for last uploaded document and returns its workpiece id.
        Input:              None
        Output:             workpiece id of last document in case no error occurs
        """
        idList = []
        try:
            lastItem = collection_workpiece.find({})
            for document in lastItem:
                idList.append(document['_id'])
            #idList.sort()
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return idList[-1]

    def machineIdQuery(self):
        """
        This function queries Machines collection of db_surfaice database for machine ids and returns a list of ids.
        Input:              None
        Output:             machineIdList of resulting ids, in case no error occurs
        """
        machineIdList = None
        collection_machines = db_surfaice["Machines"]
        try:
            machineIdQuery = collection_machines.find({}, {"_id": 1})
            machineIdList = [doc["_id"] for doc in machineIdQuery]
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return machineIdList

    def queryMaterialRemovalByTool(self, workpiece_id):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find the document with certain workpiece id
        $unwind -> access each element operations array
        $group  -> groups all elements of array by their toolId $ sums material removal of every element by their toolId as total_mr
        Input:              workpiece_id
        Output:             a result object, which is giving the results of query, in case no error occurs
        """
        pipeline = [
            {
                '$match': { '_id': workpiece_id }
            },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures.toolId',
                    'total_mr': {'$sum': '$planningData.CAM.machiningFeatures.materialRemoval'}
                }
            }
        ]
        result = None
        try:
            result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result

    def queryMeanMaterialRemovalByTool(self, workpiece_id):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find the document with certain workpiece id
        $unwind -> access each element operations array
        $group  -> groups all elements of array by their toolId $ exports average material removal of every element by their id as total_mr
        Input:              workpiece_id
        Output:             a resulting object, which is giving the results of query, in case no error occures
        """
        pipeline = [
            {
                '$match': { '_id': workpiece_id }
            },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures.toolId',
                    'average_mr': {'$avg': '$planningData.CAM.machiningFeatures.meanMaterialRemovalRate'}
                }
            }
        ]
        result = None
        try:
            result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result

    def queryCountTool(self, workpiece_id):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find the document with certain workpiece id
        $unwind -> access each element of operations array
        $group  -> grouping of all elements of array by their toolId $ counts the number of every element id and exports as count
        Input:              workpiece_id
        Output:             a resulting object, which is giving the results of query, in case no error occures
        """
        pipeline = [
            {
                '$match': { '_id': workpiece_id }
            },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures.toolId',
                    'count': {'$sum': 1}
                }
            }
        ]
        result = None
        try:
            result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result

    def verifyWorkpieceId(self, workpiece_id):
        """
        This function checks if the given workpiece id exists in Workpieces collection of db_surfaice database
        Input:              workpiece_id                            .... workpiece id to search
        Output:             verification or error
        """
        try:
            result = collection_workpiece.find_one({'_id': workpiece_id})
            print('workpiece id exists')
            return str(workpiece_id)
        except PyMongoError as e:
            print(e)


    def queryMaterialRemovalByToolAll(self):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find all documents with a processId
        $unwind -> access each element operations array
        $group  -> grouping of all elements of array by their toolId $ sum material removal of every element by their id and exports as total_mr
        Input:              None
        Output:             a resulting object, which is giving the results of query, in case no error occures
        """
        pipeline = [
            {
                "$match": {
                    "processData.processId": {"$exists": True}
                }
             },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures.toolId',
                    'total_mr': {'$sum': '$planningData.CAM.machiningFeatures.materialRemoval'}
                }
            }
        ]
        result = None
        try:
            result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result

    def queryMaterialRemovalByOperation(self, workpiece_id):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find the document with certain workpiece id
        $unwind -> access each element of operations array
        $group  -> grouping of all elements of array by their operationId $ sum material removal of every element by their id and exports as total_mr
        Input:              workpiece_id
        Output:             a result object, which is giving the results of query
        """
        pipeline = [
            {
                '$match': { '_id': workpiece_id }
            },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures._id',
                    'total_mr': {'$sum': '$planningData.CAM.machiningFeatures.materialRemoval'}
                }
            }
        ]
        result = None
        try:
            result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result


    def queryCountDrillingOperations(self, idList):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find every the document with given process id from idList
        $unwind -> access each element of operations array
        $match  -> filter operations by operationType drilling
        $group  -> grouping of all elements of array by their operationId and count the number of drilling operations of given process ids
        Input:              idList                                                  ... list of process ids generated by findItemWorkpieceSince() method of TsdbTransactions class
        Output:             a result object, which is giving the results of query in case no error occurs
        """
        pipeline = [
            {
                '$match': {'processData.processId': {'$in':idList}}
            },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$match': {'planningData.CAM.machiningFeatures.operationType': 'drilling'}
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures._id',
                    'count': {'$sum': 1}
                }
            }
        ]
        result = None
        try:
            result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result
    def queryMaterialRemovalByToolSince(self, idList):
        """
        This function uses an aggregation pipeline to perform following query in Workpieces collection of db_surfaice database:
        $match  -> find all documents within a given id list array
        $unwind -> access each element operations array
        $group  -> grouping of all elements of array by their toolId $ sum material removal of every element by their id and exports as total_mr
        Input:              None
        Output:             a resulting object, which is giving the results of query, in case no error occures
        """
        pipeline = [
            {
                "$match": {
                    "processData.processId": {"$in": idList}
                }
             },
            {
                '$unwind': '$planningData.CAM.machiningFeatures'
            },
            {
                '$group': {
                    '_id': '$planningData.CAM.machiningFeatures.toolId',
                    'total_mr': {'$sum': '$planningData.CAM.machiningFeatures.materialRemoval'}
                }
            }
        ]
        result = None
        try:
             result = list(collection_workpiece.aggregate(pipeline))
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result

    def queryTotalMrJSON(self):
        """
        This function uses an aggregation pipeline to perform following query in Tools collection of db_surfaice database:
        $match   -> find all documents with totalMaterialRemoval fields
        $project -> show only the _id and totalMaterialRemoval fields
        Input:              None
        Output:             tmr.json -> query output stored as a JSON file in data/outputs/workpieceOutput folder
        """
        pipeline = [
            {
                "$match": {
                    "totalMaterialRemoval": {"$exists": True}
                }
             },
            {
                '$project': {"_id":1, "totalMaterialRemoval":1}
            }
        ]
        result = None
        json_dir = root_path + "\\data\\outputs\\workpieceOutput\\tmr.json"
        try:
            result = list(collection_tools.aggregate(pipeline))
            with open(json_dir, 'w') as file:
                json.dump(result, file, indent=4)
        except PyMongoError as e:
            print(f"MongoDB error: {e}")
        return result


#################################################################################################################################################### DELETE FUNCTIONS

    def deleteField(self, workpiece_id, field_to_delete):
        """
        This function finds the document with a given workpiece id Workpieces collection of db_surfaice database, and deletes the field with a given name
        Input:              - workpiece_id                                      ... workpiece id to search
                            - field_to_delete                                   ... name of the field, which is wanted to be deleted
        Output:             - deleted field in case of no errors
        """
        collection = db_surfaice["Workpieces"]
        filter_criteria = {'_id': workpiece_id}
        update_query = {'$unset': {field_to_delete: 1}}
        try:
            collection.update_one(filter_criteria, update_query)
            print('Field has been deleted')
        except PyMongoError as e:
            print(f"MongoDB error: {e}")

    def deleteDocument(self, id, collection):
        """
        This function finds the document with a given id of a given collection of db_surfaice database, and deletes the document
        Input:              - id                                              ... id to search
                            - collection                                      ... collection to search for the id
        Output:             - deleted document in case of no errors
        """
        filter_criteria = {"_id": f"{id}"}
        try:
            result = collection.delete_one(filter_criteria)
            if result.deleted_count > 0:
                print("Document deleted successfully.")
            else:
                print("No matching document found for deletion.")
        except PyMongoError as e:
            print(f"MongoDB error: {e}")