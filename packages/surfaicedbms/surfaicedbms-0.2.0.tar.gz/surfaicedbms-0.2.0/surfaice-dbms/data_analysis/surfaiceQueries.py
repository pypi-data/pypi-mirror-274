#################################################################################################### Import Modules
from surfaicedbms import mongoTransactions
from surfaicedbms import tsdbTransactions
from surfaicedbms import dataProcessor


#################################################################################################### Initiate classes
mongo = mongoTransactions.MongoTransactions()
tsdb = tsdbTransactions.TsdbTransactions()
processor = dataProcessor.DataProcessor()

#################################################################################################### Output directory entry
print(f"Please enter an output directory: ")
output_dir = str(input())

#################################################################################################### Decision for material removal report or data export
print(f"Please type 1 for Material Removal Report, 2 for Data Visualization, 3 for Data Export: ")
decision = int(input())

if decision == 1:
    ################################################################################################# Material Removal Report
    print(f"Please enter query beginning date in following form 'yyyy-mm-dd hh:mm:sss' ")
    datetime = str(input())
    wpSince = tsdb.findItemWorkpieceSince(datetime)
    drillingOp = mongo.queryCountDrillingOperations(wpSince)
    mrByTool = mongo.queryMaterialRemovalSince(wpSince)
    processor.createPdfExport(wpSince, datetime, drillingOp, mrByTool, output_dir)
elif decision == 2:
    print(f"Please enter a workpiece id: ")
    workpiece_id = str(input())
    #################################################################################################### Collect Process Data
    df_pos = tsdb.queryPosition(workpiece_id)
    df_spindleload = tsdb.querySpindleLoad(workpiece_id)
    df_spindlespeed = tsdb.querySpindleSpeed(workpiece_id)
    df_feedrate = tsdb.queryFeedRate(workpiece_id)
    df_xacc = tsdb.queryAcceleration(workpiece_id)

    #################################################################################################### Visualize Process Data
    processor.plotProcessData(output_dir, workpiece_id, df_pos, df_xacc, df_spindleload, df_spindlespeed, df_feedrate)
    print("Process Data Visualizations have been exported.")

    #################################################################################################### Collect Quality Data
    inspectionId = mongo.findInspectionId(workpiece_id)
    print(f"Please enter a filter for quality inspection data: ")
    filterQuality = str(input())
    df_rz = tsdb.queryRz(inspectionId, filterQuality)
    df_ra = tsdb.queryRa(inspectionId, filterQuality)

    #################################################################################################### Visualize Quality Data
    processor.plotQualityData(output_dir, inspectionId, df_rz, df_ra)
    print("Quality Data Visualizations have been exported.")
elif decision == 3:
    #################################################################################################### Data Export
    print(f"Please enter a workpiece id: ")
    workpiece_id = str(input())

    #################################################################################################### Folder Structure
    planning_folder, process_folder, quality_folder = processor.createFolderStructure(workpiece_id, output_dir)

    #################################################################################################### Planning Data Export
    mongo.exportWorkpiece(workpiece_id, planning_folder)
    camSetupId = mongo.findCamSetupId(workpiece_id)
    mongo.exportPrt(camSetupId, planning_folder)
    mongo.exportPdf(camSetupId, planning_folder)

    #################################################################################################### Process Data Export
    tsdb.exportAcc(workpiece_id, process_folder)
    tsdb.exportNc(workpiece_id, process_folder)
    tsdb.exportContinousAggregate(workpiece_id, process_folder)
    processId = mongo.findProcessId(workpiece_id)
    tsdb.exportManOpt(processId, process_folder)

    #################################################################################################### Quality Data Export
    inspectionId = mongo.findInspectionId(workpiece_id)
    tsdb.exportQuality(inspectionId, quality_folder)





