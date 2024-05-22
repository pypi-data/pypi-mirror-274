import os
from IFT.IFTBase import IFTCore, IFTCAMSetup
from IFT.IFTTool import IFTToolCollection, IFTTool
from IFT.IFTMachiningPart import IFTMachiningPart, IFTMachiningPartCollection
from IFT.IFTOperation import IFTOperationCollection, IFTOperation
from IFT.IFTMachine import IFTMachine
from IFT.IFTMachiningFeature import IFTMachiningFeature, IFTMachiningFeatureCollection
import json
import logging

env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
root_path =  os.getenv(env_name_root)
storage_dir = root_path + "\\data\\outputs\\workpieceOutput"
class NxOperations:

    def camSetupInstance(self):
        """
        Generates a CAM Setup instance using IFTCAMSetup() method
        Input:		None

        Output:		CAM Setup instance
        """
        cam_setup = IFTCAMSetup()
        cam_setup.set_id() # set identifier for json file
        cam_setup.set_editor() # sets the current editor of the CAM setup
        cam_setup.set_setup_id_revision_and_creator() # sets setup id and finds revision number
        return cam_setup

    def generateTool(self):
        """
        Generates a tool collection instance using IFTToolCollection() method and extracts tool related informations from CAM Setup
        Input:		None

        Output:		- toolData										.... contains data fields regarding tools used in cam setup, wich will be used to register to toolData collection if not already exists
                    - toolIds										.... contains ids of corresponding toolData, which will be appended to workpiece docunent
        """
        tool_collection = IFTToolCollection()
        for i in range(tool_collection.nx_counter):
            temp_tool = IFTTool(tool_collection, i)
            temp_tool.get_data_attributes()
        toolData = list()
        for tool in tool_collection.ift_objects.values():
            toolData.append(tool.get_data_dict())
        for i in range(len(toolData)):
            toolData[i]['_id'] = toolData[i]['toolId']
            del toolData[i]['toolId']
        toolIds = []
        for i in range(len(toolData)):
            toolIds.append(toolData[i]["_id"])
        return toolData, toolIds

    def generateMachiningPart(self):
        """
        Generates a machining part collection instance using IFTMachiningPartCollection() method and extracts machining part related informations from CAM Setup
        Input:		None

        Output:		machiningPartsData							... contains data fields regarding machining part used in cam setup, wich will be used to register to machiningPartsData collection if not already exists
        """
        machining_part_collection = IFTMachiningPartCollection()
        for i in range(machining_part_collection.nx_counter):
            temp_machining_part = IFTMachiningPart(machining_part_collection, i)
            temp_machining_part.get_data_attributes()
        machiningPartsData = list()
        for machining_part in machining_part_collection.ift_objects.values():
            machiningPartsData.append(machining_part.get_data_dict())
        machiningPartsData[0]['_id'] = machiningPartsData[0]['machiningPartId']
        del machiningPartsData[0]['machiningPartId']
        return machiningPartsData

    def generateMachine(self):
        """
        Generates a machine instance using IFTMachine() method and extracts machine related informations from CAM Setup
        Input:		None

        Output:		- machine								... machine instance to generating g code
                    - machineData							... contains data fields regarding manufacturing machine used in cam setup, which will be used to register to machineData collection if not already exists
        """
        machine = IFTMachine()
        machine.get_data_attributes()
        machineData = machine.get_data_dict()
        machineData['_id'] = machineData['machineId']
        del machineData['machineId']
        return machine, machineData

    def generateDesignFeatures(self):
        """
        Generates a design feature collection instance using IFTMachiningFeatureCollection() method and extracts design feature related informations from CAM Setup
        Input:		None

        Output:		designFeaturesData							... contains data fields regarding design features used in cam setup, which will be used in workpiece data model.
        """
        design_feature_collection = IFTMachiningFeatureCollection()
        for i in range(design_feature_collection.nx_counter):
            temp_machining_feature = IFTMachiningFeature(design_feature_collection, i)
            temp_machining_feature.get_data_attributes()
        designFeaturesData = list()
        for design_feature in design_feature_collection.ift_objects.values():
            designFeaturesData.append(design_feature.get_data_dict())
        for i in range(len(designFeaturesData)):
            designFeaturesData[i]['_id'] = designFeaturesData[i]['machiningFeatureId']
            del designFeaturesData[i]['machiningFeatureId']
        return designFeaturesData

    def generateMachiningFeatures(self):
        """
        Generates a machining feature collection instance using IFTOperationCollection() method and extracts machining feature related informations from CAM Setup
        Input:		None

        Output:		machiningFeaturesData		... contains data fields regarding machining features used in cam setup, which will be used in workpiece data model
        """
        machining_feature_collection = IFTOperationCollection()
        for i in range(machining_feature_collection.nx_counter):
            temp_operation = IFTOperation(machining_feature_collection, i)
            temp_operation.get_data_attributes()
        machiningFeaturesData = list()
        for machining_feature in machining_feature_collection.ift_objects.values():
            machiningFeaturesData.append(machining_feature.get_data_dict())
        for i in range(len(machiningFeaturesData)):
            machiningFeaturesData[i]['_id'] = machiningFeaturesData[i]['operationId']
            del machiningFeaturesData[i]['operationId']
        return machiningFeaturesData

    def generateGcode(self, machine):
        """
        Generates and stores a gcode instances for storing in workpiece data in Mongo DB and file system
        Input:		- storage_dir								... storage location in file system
                    - machine									... machine instance for generating g code

        Output:		- nc_post									... object contains g code as string
                    - nc_dir									... storage directory of generated gcode
        """
        nc_dir = storage_dir + "\\G_CODE.ptp"
        machine.get_nc_code(nc_dir)
        nc_post = {}
        with open(nc_dir, "r") as file:
            nc_post["NCcode"] = file.read()
        file.close()
        return nc_post, nc_dir

    def generatePost(self, cam_setup, machiningPartsData, machineData, toolIds, nc_post, designFeaturesData, machiningFeaturesData):
        """
        Generates a workpiece data model using cam setup, machining part, machine, tool, operation, machining features, gcode instances for storage in Mongo DB
        Input:		None

        Output:		post										... object contains workpiece related data fields, which will be stored with a unique workpiece id
        """
        post = cam_setup.get_data_dict()
        revision = post["revison"]
        cam_setup_id = post["setupId"]
        del post["revison"]
        del post["setupId"]
        del post['3DPDF']
        del post['NCCode']

        post['planningData'] = {
            "CAD": {"machiningPartId": machiningPartsData[0]["_id"],
                    "designFeatures": designFeaturesData,
                    "pmis": [],
                    "geometricData": None,
                    "cadMetaData": None
                    },
            "CAM": {"revision": revision,
                    "machineId": machineData["_id"],
                    "camSetupId": cam_setup_id,
                    "machiningFeatures": machiningFeaturesData,
                    },
            "CAPP": {"toolset": [],
                    "tools": toolIds,
                    "g-code": nc_post
                    }
        }
        post['schemaVersion'] = 1.0
        return post


    def generatePostV2(self, cam_setup, machiningPartsData, machineData, toolIds, nc_post, designFeaturesData, machiningFeaturesData):
        """
        Generates a workpiece data model using cam setup, machining part, machine, tool, operation, machining features, gcode instances for storage in Mongo DB
        Input:		None

        Output:		post										... object contains workpiece related data fields, which will be stored with a unique workpiece id
        """
        ########################################################################### another example datamodel
        post = cam_setup.get_data_dict()
        revision = post["revison"]
        cam_setup_id = post["setupId"]
        del post["revison"]
        del post["setupId"]
        del post['3DPDF']
        del post['NCCode']

        post['planningData'] = {
            "CAD": {"machiningPartId": machiningPartsData[0]["_id"],
                    "designFeatures": designFeaturesData,
                    "pmis": [],
                    "geometricData": None,
                    "cadMetaData": None
                    },
            "CAM": {"revision": revision,
                    "machineId": machineData["_id"],
                    "camSetupId": cam_setup_id,
                    "machiningFeatures": machiningFeaturesData,
                    },
            "CAPP": {"toolset": [],
                    "tools": toolIds,
                    "g-code": nc_post
                    }
        }
        post['schemaVersion'] = 2.0
        return post

    def savePost(self, post):
        """
        Stores workpiece instance in file system and returns workpiece id as string
        Input:		- post										... workpiece instance to store
                    - storage dir								... storage directory in file system

        Output:		- workpiece_ID								... a string giving information about workpiece id of current workpiece
        """
        json_dir = storage_dir + f"\\lastWorkpiece.json"
        json_file = open(json_dir, "w")
        json.dump(post, json_file, indent=4)
        json_file.close()
        IFTCore.emphasize()
        IFTCore.print_nx(f"WORKPIECE OBJECT HAS BEEN RESTRUCTURED AND SAVED IN {json_dir}")
        IFTCore.emphasize()

    def createLogger(self, workpiece_id):
        """
        Creates a logger instance for reporting regarding current transactions
        Input:		- root_path									... project directory root
                    - logger_time								... certain timestamp format to name the file

        Output:		logger										... an object to write log registers
        """
        logger = None
        logger_path = f"\\data\\outputs\\logger\\log_{workpiece_id}.log"
        try:
            logging.basicConfig(
                filename=root_path + logger_path,
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s]: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            logger = logging.getLogger(f"log_{workpiece_id}.log")
            IFTCore.print_nx(f"logger instance is created")
        except Exception as e:
            IFTCore.print_nx(f"{e}")
        return logger