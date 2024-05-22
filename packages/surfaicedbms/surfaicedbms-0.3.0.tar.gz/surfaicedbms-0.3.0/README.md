# Autor Info
- Autor: Atahan Kap
- Version: 0.0.1
- Date: 07-05-2024
- Python Version: 3.10

# Global Installation
1.  Make sure, python version 3.10. is installed
2.  Opening command line within repository folder and running commands:
    - pip install -e ./nxopen-export-lea/
    - pip install -e .
    - pip show surfaicedbms
3.  copy the value of Location field, e.g.: c:\users\your_user_name\appdata\local\programs\python\python310\lib\site-packages
4.  set following environment variables:
    - surfaice_dbms_root:     ...\site-packages\surfaicedbms
    - surfaice_dbms_config:   ...\site-packages\surfaicedbms\data\config.yaml

# Decription

This software is designed to store, analyze, import, and export available data in the context of “surfaice” project. Supplied data has a heterogenous nature as it consists of:
 - Unstructured data types with pdf or prt extensions. For these types of data, it is not possible to be processed by conventional tools, due to the lack of their predefined model.
 - Semi-structured data types such as JSON, which provide a flexible data model as it doesn’t force for a rigid data structure. 
 - Structured data as data frames or any table-based components, where the data is organized into columns and rows.
surfaicedbms handles the storage of this heterogenous data by saving unstructured and semi-structured data into a NoSQL database and, the structured data to a conventional database.
With conventional database higher validation and transaction safety have been achieved by using trigger functions and constraints as primary or foreign keys.
Additionally, for handling the time-series an extension to the conventional database PostgreSQL the TimescaleDB has been used to access its additional functionalities as continuous aggregates.

# Software Architecture

surfaicedbms consist of three different layers:
- Database layer includes on the one hand storage units in available Mongo DB and PostgreSQL connections such as tables, views, collections or documents, on the other hand further functionalities
such as functions, triggers and constraints to perform efficient management of a certain data model.
- API layer includes classes, which are relevant for providing methods for generating processing data, as well as methods used for sending read, write, update or delete requests to the databases.
- Application layer includes workflows both for data acquisition of a workpiece data model from different phases of product life cycle, and data analysis from acquired data.

# Folder Content

    - MANIFEST.in : File contains information, which files to include in package
    - pyproject.toml: File containing information for the build of the package
    - README.md: File containing descriptions regarding surfaicedbms package

## tests folder:
    - planningMainV2.py: Script for building an alternative schema version of workpiece data model.
    - testMongoExport.py: Script for exporting files with .pdf and .prt extension
    . testTsdbExport.py: Script for exporting files with .csv extension


## visuals folder: 
Contains visualisations regarding the workflows of main files, data model and ER diagram of DBMS.

## src folder:
1. surfaicedbms.egg-info: Folder, which holds metadata about surfaicedbms package
2. surfaicedbms: Installable package, shared over a git repository

## surfaicedbms folder:
  - config.yaml: File containing information regarding the database connections.
  - dataProcessor.py: Script contains DataProcessor Class, which provides methods for data preparation and process
  - edgeApp.py: Script contains EdgeApplication Class, which provides live manufacturing mock data
  - mongoTransactions.py: Script contains MongoTransactions Class, which provides methods for database related operations in Mongo DB.
  - tsdbTransactions.py: Script contains TsdbTransactions Class, which provides methods for databased related operations in PostgreSQL connection.
  - nxOperations.py: Script contains NxOperations Class, which provides methods for generating a workpiece instance.
  - qualityApp.py: Script contains RaRz Class, which provides a method for calculation of Ra and Rz values from quality profiles. 
  
## 1. build folder:
    - buildRelationalDb.py: Script, which includes the workflow for creating and configuring relational database tables for applying workpiece data model.
    - destructRelationalDb.py: Script, which includes the workflow for deleting relational tables, in case the database need to be restarted.
   
## 2. data folder:

### 2.1. inputs folder:

#### 2.1.1. camSetup folder:
    - camSetupId.prt: File with .prt extension, which includes information regarding CAM-Setup, and will be stored in Mongo DB connection.


#### 2.1.2. mockFiles folder:

##### 2.1.2.1. 15th_experiment folder: 
Folder includes files from live manufacturing process, which will be used for generation of mock data in a simulated edgeApplication.


#### 2.1.3. Profiles folder: 
Folder includes files from quality measurements, which will be used for generation of mock data in a simulated qualityApplication.



### 2.2. outputs folder:

#### 2.2.1. 3dPdf folder:
    - camSetupId.pdf: File with .pdf extension, which includes information regarding CAM-Setup, and will be stored in Mongo DB connection.

#### 2.2.2. formedProfiles folder:
    - merged_data.csv: File with .csv extension, which has been generated after data preparation process of quality profiles under "data.input.Profiles" folder.

#### 2.2.3. logger folder:
    - workpiece_id.csv: File with .log extension, in order to keep records regarding data acquisition from the workpiece data model.

#### 2.2.4. manufacturing_operations_metadata folder:
    - manopt_optput.csv.gz: File with .csv.gz extension regarding metadata of live manufacturing process, which has been generated after data preparation process data gained from edgeApplication.
    This dataset will be stored in available PostgreSQL connection over ingestManufacturingOperations() method.

#### 2.2.5. processed_manufacturing_data folder:
    - acc_output.csv.gz: File with .csv.gz extension regarding acceleration sensor data of live manufacturing process, which has beeen generated after data preparation process data gained from edgeApplication.
    This dataset will be stored in an available Hypertable in Timescale DB, which is accessed over PostgreSQL connection. The data ingestion occurs with ingestAcc() method.
    - nc_output.csv.gz: File with .csv.gz extension regarding cnc machine data of live manufacturing process, which has beeen generated after data preparation process data gained from edgeApplication.
    This dataset will be stored in an available Hypertable in Timescale DB, which is accessed over PostgreSQL connection. The data ingestion occurs with ingestNc() method.

#### 2.2.6. rarz folder:
    - rarz_output.csv.gz: File with .csv.gz extension regarding quality data. This file has been generated after application of a method for calculation of relevant Ra and Rz values, which provided by Rarz class.
    The dataset will be stored in available PostgreSQL connection over ingestRarz() method.

#### 2.2.7. workpieceOutput folder:
    - lastWorkpiece.json: File with .json extension, which contains objects regarding workpiece data model. This file is the starting point for generation of a document structure for a workpiece in available Mongo DB connection, and contains the last uploaded item to the workpieces collection.
    The data will be generated by using planningMain.py script over Siemens NX plug-in, and the ingestion of this file occurs over ingestWorkpiece() method.
    - G_CODE.ptp: File with .ptp extension, which contains g-code extracted from available CAM-Setup 


### 2.3. data_analysis folder:
    - surfaiceQueries.py: Script, which contains specified query results on workpiece data model


### 2.4. data_feed folder: 
Folder contains scripts for the data acquisition of workpiece data model.

    - planningMain.py: Script, which is used for planning data acquisition, which is run over Siemens NX Plug-in.
    - processMain.py: Script, which is used for process data acquisition.
    - qualityMain.py: Script, which is used for quality data acquisition.

 
