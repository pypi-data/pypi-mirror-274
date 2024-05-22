	# nx: threaded
from IFT.IFTTool import IFTToolCollection, IFTTool
from IFT.IFTBase import IFTCore, IFTCAMSetup
from IFT.IFTPDF import IFTPDF
from surfaicedbms import nxOperations
import os

env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
root_path =  os.getenv(env_name_root)
storage_dir = root_path + "data\\outputs\\workpieceOutput"

########################################################################### starting data export
nx = nxOperations.NxOperations()
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

########################################################################### collect every object into the workpiece data model
post = nx.generatePost(cam_setup, machiningPartsData, machineData, toolIds, nc_post, designFeaturesData, machiningFeaturesData)

########################################################################### save workpiece as a json file
nx.savePost(post)

########################################################################### workpiece is exported as a json file
IFTCore.emphasize()
IFTCore.print_nx("DATA EXPORT FINISHED")
IFTCore.emphasize()