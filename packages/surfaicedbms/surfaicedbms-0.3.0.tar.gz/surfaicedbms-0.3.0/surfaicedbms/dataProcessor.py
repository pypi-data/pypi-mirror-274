import os
import pandas as pd
import numpy as np
from datetime import datetime
import shutil
import csv
import time
from fpdf import FPDF
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages



env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
root_path =  os.getenv(env_name_root)

class DataProcessor:
    def interpolateTimestamp(df):
        """
        This function is used for interpolating used for replacing repeated values of a pandas dataframe with interpolated timestamp values.
        Input:              - df                                             ... dataframe with a timestamp column, which has to be interpolated

        Output:             - df                                             ... resulting dataframe
        """
        duplicates = df['timestamp'].duplicated(keep='first')

        df.loc[duplicates, 'timestamp'] = np.nan

        nan_mask = df['timestamp'].isna()

        indices = np.arange(len(df))

        arr = np.interp(indices, indices[~nan_mask], df['timestamp'].dropna())
        # if round
        # rounded_array = np.round(arr, decimals=6)
        # if round
        # df['timestamp'] = rounded_array

        df['timestamp'] = arr
        return df

    def convertTimestampToDatetime(dataframe):
        """
        This function is used for converting timestamp values to a certain date time format
        Input:              - dataframe                                      ... dataframe with a timestamp column, which has to be converted.

        Output:             - dataframe                                      ... resulting dataframe
        """
        date_format = "%Y-%m-%d %H:%M:%S.%f"
        dataframe.reset_index(drop=True, inplace=True)
        dataframe['timestamp'] = pd.to_datetime(dataframe['timestamp'], unit='s')
        return dataframe

#################################################################################################################################################### MANUFACTURING PROCESS DATA PROCESS
    def formRawData(self, fake_rawdata, workpiece_id):
        """
        This function is used for converting manufacturing process related tabular raw data of edge application to a desired format.
        The data processing includes following steps:
        - Grouping dataframes into acceleration sensor data or cnc data
        - Naming columns
        - Merging groups in themselves
        - Linear interpolation of repeated timestamp values
        - Timestamp conversion to a desired datetime format
        - Inserting a new column with an input value of workpiece_id
        - Exporting the file in a compressed gzip format to ease data ingestion
        Input:              - fake_rawdata                                                                ... input gained from the output of edge application, which is related to manufactiong process data
                            - workpiece_id                                                                ... workpiece id to insert to dataframe
        Output:             - result_df_1                                                                 ... resulting dataframe of cnc data
                            - nc_output.csv.gz in data\outputs\processed_manufacturing_data directory     ... resulting output file for cnc data
                            - result_df_2                                                                 ... resulting dataframe of acceleration sensor data
                            - acc_output.csv.gz in data\outputs\processed_manufacturing_data directory    ... resulting output file for acceleration sensor data

        """
        relative_path = os.path.join(root_path, 'data\outputs\processed_manufacturing_data')

        # RESTRUCTURE
        group1 = fake_rawdata[:3]
        group2 = fake_rawdata[3:6]

        # NAME COLUMNS
        columns_nc = ["timestamp", "featureMeas", "featureTotal", "xAbs", "yAbs", "zAbs", "cAbs", "aAbs", "xServo",
                      "yServo",
                      "zServo", "cServo", "aServo", "spindleLoad", "feedrate", "spindlespeed"]

        columns_acc = [ "counter", "timestamp", "xacc"]

        for df in range(len(group1)):
            group1[df].reset_index(drop=True, inplace=True)
            group1[df].columns = columns_nc

        for df in range(len(group2)):
            group2[df].reset_index(drop=True, inplace=True)
            group2[df].columns = columns_acc
        # MERGE DFS #
        result_df_1 = pd.concat(group1, ignore_index=True)
        result_df_2 = pd.concat(group2, ignore_index=True)

        # if interpolate
        result_df_1 = DataProcessor.interpolateTimestamp(result_df_1)

        # UNIX TIMESTAMP CONVERSION
        result_df_1 = DataProcessor.convertTimestampToDatetime(result_df_1)
        result_df_2 = DataProcessor.convertTimestampToDatetime(result_df_2)

        # ADD WORKPIECE ID
        result_df_1.insert(0, 'WorkpieceID', workpiece_id)
        result_df_2.insert(0, 'WorkpieceID', workpiece_id)

        # TEMPORARY STORAGE WITH GZIP #
        result_df_1.to_csv(relative_path+"\\nc_output.csv.gz", index=False, compression='gzip')
        result_df_2.to_csv(relative_path+"\\acc_output.csv.gz", index=False, compression='gzip')

        return result_df_1, result_df_2


    def formMetaData(self, fake_metadata, process_id):
        """
        This function is used for converting manufacturing process related metadata of edge application regarding manufacturing operations to a desired format.
        The data processing includes following steps:
        - Restructring the metadata into a tabular form
        - Exporting the file in a compressed gzip format to ease data ingestion
        - Returning the manufacturing operation ids for further process                                                                                                                [Excluded]

        Input:              - fake_metadata                                                                                 ... input gained from the output of edge application, which is related to manufactiong process data
                            - process_id                                                                                    ... process id to insert to dataframe
        Output:             - manopt_output.csv.gz in data\outputs\manufacturing_operations_metadata directory              ... resulting tabular data after data processing
                            - Output['manopt_id']                                                                           ... resulting array of manufacturing operation ids          [Excluded]

        """
        relative_path = os.path.join(root_path,'data\outputs\manufacturing_operations_metadata')
        date_format = '%Y_%m_%d_%H_%M_%S'
        columns = ['process_id', 'manopt_id', 'ts_operation_start', 'ts_operation_end', 'ts_position_start',
                   'ts_position_end', 'ts_acc_start', 'ts_acc_end']
        # RESTRUCTURING METADATA
        Output = pd.DataFrame(columns=columns)
        for i in range(len(fake_metadata)):
            tempOutput = pd.DataFrame(columns=columns)
            tsOperationStart = []
            tsOperationEnd = []
            tsPositionStart = []
            tsPositionEnd = []
            tsAccStart = []
            tsAccEnd = []
            tsOperationStart.append(fake_metadata[i][1][0])
            tsOperationEnd.append(fake_metadata[i][1][1])
            tsPositionStart.append(fake_metadata[i][2][0])
            tsPositionEnd.append(fake_metadata[i][2][1])
            tsAccStart.append(fake_metadata[i][3][0])
            tsAccEnd.append(fake_metadata[i][3][1])
            OperationIdInSec = int(fake_metadata[i][0].split("_")[0])
            OperationIdIndex = fake_metadata[i][0].split("_")[1]
            OperationIdInDatetime = "opr_" + datetime.fromtimestamp(OperationIdInSec).strftime(
                date_format) + "_" + OperationIdIndex
            OperationList = []
            OperationList.append(OperationIdInDatetime)
            OperationList = OperationList * 3
            ProcessList = []
            ProcessList.append(str(process_id))
            ProcessList = ProcessList * 3
            tempOutput['process_id'] = ProcessList
            tempOutput['manopt_id'] = OperationList
            tempOutput['ts_operation_start'] = datetime.fromtimestamp(float(tsOperationStart[0]))
            tempOutput['ts_operation_end'] = datetime.fromtimestamp(float(tsOperationEnd[0]))
            tempOutput['ts_position_start'] = datetime.fromtimestamp(float(tsPositionStart[0]))
            tempOutput['ts_position_end'] = datetime.fromtimestamp(float(tsPositionEnd[0]))
            tempOutput['ts_acc_start'] = datetime.fromtimestamp(float(tsAccStart[0]))
            tempOutput['ts_acc_end'] = datetime.fromtimestamp(float(tsAccEnd[0]))
            Output = pd.concat([Output,tempOutput], ignore_index=True)
        Output = Output.drop_duplicates().reset_index(drop=True)
        Output.to_csv(relative_path + "\\manopt_output.csv.gz", index=False, compression='gzip')
        print("manufacturing operations metadata has been prepared")
        return Output['manopt_id']


#################################################################################################################################################### QUALITY DATA PROCESS
    def formQuality(self):
        """
        This function is used for restructuring raw data regarding measurements of quality profiles to ease the calculation of Ra and Rz values, which are characteristic figures for the interpretation of surface quality.
        The function uses txt files in data\inputs\profiles directory as input, and generates an output in data\outputs\formedProfiles directory, and finally returns an inspection id, which is generated within this function.
        The data processing includes following steps:
        - Separating all files in 2 groups
        - Renaming the columns of the group with column names
        - Inserting headers to the files of group without column names
        - Appending filenames to the datasets in order to not to loose any information within merging
        - Merging groups in themselves
        - Merging both groups
        - Converting height columns values from mm to µn
        - Exporting the file in csv format
        - Deleting unnecessary files, which are generated within data processing
        Input:              - txt files in data\inputs\profiles directory

        Output:             - merged_data.csv in data\outputs\formedProfile directory                                ... resulting tabular data of quality profiles
                            - inspection_id                                                                          ... identification number of quality measurment
        """
        current_time = datetime.fromtimestamp(time.time())
        id_format = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        inspectionId="ins_"+id_format
        relative_path_inputs = os.path.join(root_path, 'data\inputs\profiles')
        relative_path_outputs = os.path.join(root_path, 'data\outputs\\formedProfiles')
        output_folder_path_1 = os.path.join(relative_path_outputs,"1")
        output_folder_path_2 = os.path.join(relative_path_outputs,"2")
        os.mkdir(output_folder_path_1)
        os.mkdir(output_folder_path_2)

        ### List of all txt files

        file_list = []

        for filename in os.listdir(relative_path_inputs):
            if filename.endswith(".txt"):
                file_list.append(filename)

        ### Grouping files

        with_columns = []
        without_columns = []

        for i in range(len(file_list)):
            if (str(file_list[i]).split("_")[1] == "1"):
                with_columns.append(file_list[i])
            else:
                without_columns.append(file_list[i])
                ### Preprocessing of data with columns

        for filename in with_columns:
            file_path = os.path.join(relative_path_inputs, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            header = "counter;distance_mm;height_µm;valid;experiment_id\n"
            del lines[0]
            del lines[0]
            output_filename = os.path.splitext(filename)[0]
            output_file_path = os.path.join(output_folder_path_1, output_filename + ".csv")
            with open(output_file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([header.strip()])
                for line in lines:
                    csv_writer.writerow([line.strip() + ';' + output_filename])

        ### Preprocessing of data without columns

        for filename in without_columns:
            file_path = os.path.join(relative_path_inputs, filename)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            header = "distance_mm;height_µm;experiment_id\n"
            output_filename = os.path.splitext(filename)[0]
            output_file_path = os.path.join(output_folder_path_2, output_filename + ".csv")  #
            with open(output_file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow([header.strip()])
                for line in lines:
                    csv_writer.writerow([line.strip() + ';' + output_filename])

        ### Merge first group

        csv_files = [file for file in os.listdir(output_folder_path_1) if file.endswith('.csv')]
        selected_columns = ['distance_mm', 'height_µm', 'experiment_id']
        merged_data_1 = pd.DataFrame(columns=selected_columns)

        for i, csv_file in enumerate(csv_files):
            current_data = pd.read_csv(os.path.join(output_folder_path_1, csv_file), encoding='Latin', sep=";")
            current_data = current_data[selected_columns]
            merged_data_1 = pd.concat([merged_data_1, current_data], ignore_index=True)
            #merged_data_1 = merged_data_1.append(current_data, ignore_index=True)

        ### Merge second group

        csv_files_2 = [file for file in os.listdir(output_folder_path_2) if file.endswith('.csv')]
        merged_data_2 = pd.DataFrame(columns=selected_columns)

        for i, csv_file_2 in enumerate(csv_files_2):
            current_data = pd.read_csv(os.path.join(output_folder_path_2, csv_file_2), encoding='Latin', sep=";")
            current_data = current_data[selected_columns]
            merged_data_2 = pd.concat([merged_data_2, current_data], ignore_index=True)

        final_df = pd.concat([merged_data_1, merged_data_2], ignore_index=True)
        final_df['height_µm'] = final_df['height_µm'] * 1000
        final_df.to_csv(relative_path_outputs+"\merged_data.csv", index=False, encoding='Latin')

        ### Delete unnecessary files

        shutil.rmtree(output_folder_path_1)
        shutil.rmtree(output_folder_path_2)
        return inspectionId

#################################################################################################################################################### EXPORT FOLDER STRUCTURE

    def createFolderStructure(self, workpiece_id, output_dir):
        """
        This function helps to create a certain folder structure for the organized exports of data export functionality of data analysis tool.
        Inputs: - workpiece_id                              ... this ID is used for naming the parent folder
                - output_dir                                ... Directory to create folder structure
        Output: - folder structure including planning, process and quality data
        """
        output_folder = os.path.join(output_dir, workpiece_id)
        planning_folder = os.path.join(output_folder, "planningData")
        process_folder = os.path.join(output_folder, "processData")
        quality_folder = os.path.join(output_folder, "qualityData")
        try:
            os.mkdir(output_folder)
            os.mkdir(planning_folder)
            os.mkdir(process_folder)
            os.mkdir(quality_folder)
            print("Output folder structure has been created ")
            return planning_folder, process_folder, quality_folder
        except(Exception) as error:
            print(error)

#################################################################################################################################################### EXPORT FOLDER STRUCTURE
    def createPdfExport(self, findWorkpieceSince, uploadDate, queryDrillingOperations, queryMaterialRemovalSince, output_dir):
        """
        This function provides a PDF file, which gives information about results of following three queries:
        1. Instantiated workpieces since certain data with the query findWorkpieceSince
        2. Number of drilling operations with the query queryDrillingOperations
        3. Values of total material removals of every Tool ID since certain date with the query queryMaterialRemovalSince
        Inputs: - findWorkpieceSince                                ... the results of the query findWorkpieceSince
                - uploadDate                                        ... query beginning data
                - queryDrillingOperations                           ... the results of the query queryDrillingOperations
                - queryMaterialRemovalSince                         ... the results of the query queryMaterialRemovalSince
                - output_dir                                        ... the output directory to export the PDF file

        Output: - materialRemovalReport.pdf                         ... the resulting PDF file
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", size=20, style="B")
        pdf.cell(200, 10, txt="Material Removal Report", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", size=12, style="B")
        pdf.multi_cell(0, 10, txt=f"Instantiated workpieces since: {uploadDate}")
        pdf.set_font("Arial", size=12)
        col_width = pdf.w / 3.5
        row_height = pdf.font_size
        col_widths = [30, 20, 20]
        total_width = sum(col_widths)
        x_centered = (pdf.w - total_width) / 2
        for row in findWorkpieceSince:
            pdf.set_x(x_centered)
            pdf.cell(col_width, row_height * 1.5, txt=row, border=1)
            pdf.ln(row_height * 1.5)
        pdf.ln(10)

        pdf.set_font("Arial", size=12, style="B")
        pdf.multi_cell(0, 10, txt=f"The number of the drilling operations since: {uploadDate}")
        headers = list(queryDrillingOperations[0].keys())
        col_width = 80
        for header in headers:
            pdf.cell(col_width, 10, header, border=1)
        pdf.ln()
        pdf.set_font("Arial", size=12)
        for row in queryDrillingOperations:
            for header in headers:
                pdf.cell(col_width, 10, str(row[header]), border=1)
            pdf.ln()
        pdf.ln(10)

        pdf.set_font("Arial", size=12, style="B")
        pdf.multi_cell(0, 10, txt=f"Total material removal by tool for all documents with schema version 1")
        headers2 = list(queryMaterialRemovalByToolAll[0].keys())
        col_width = 80
        for header in headers2:
            pdf.cell(col_width, 10, header, border=1)
        pdf.ln()
        pdf.set_font("Arial", size=12)
        for row in queryMaterialRemovalByToolAll:
            for header in headers2:
                pdf.cell(col_width, 10, str(row[header]), border=1)
            pdf.ln()

        pdf.output(f"{output_dir}/materialRemovalReport.pdf")

#################################################################################################################################################### PLOTS

    def plotProcessData(self, output_dir, workpiece_id, df_pos, df_xacc, df_spindleload, df_spindlespeed, df_feedrate):
        f"""
        This function is used to generate a PDF file, which consists of visualizations of live manufacturing process data. The visualizations are generated through following queries:
        1. queryPositions
        2. queryAcceleration
        3. querySpindleLoad
        4. querySpindleSpeed
        5. queryFeedRate
        Inputs: - output_dir                                                              ... Directory to store resulting PDF file
                - workpiece_id                                                            ... Workpiece ID to query for
                - df_pos, df_xacc, df_spindleload, df_spindlespeed, df_feedrate           ... Dataframes collected from the queries
                
        Output: - process_workpiece_id.pdf                                                ... Resulting PDF file
        """
        pdf_filename = os.path.join(output_dir, 'process_' + workpiece_id + '.pdf')
        with PdfPages(pdf_filename) as pdf:
            ## positions
            plt.figure(figsize=(20, 10))
            plt.plot(df_pos['bucket'], df_pos['xabs_avg'], label='Xabs_avg')
            plt.plot(df_pos['bucket'], df_pos['yabs_avg'], label='Yabs_avg')
            plt.plot(df_pos['bucket'], df_pos['zabs_avg'], label='Zabs_avg')
            plt.plot(df_pos['bucket'], df_pos['cabs_avg'], label='Cabs_avg')
            plt.plot(df_pos['bucket'], df_pos['aabs_avg'], label='Aabs_avg')
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.xlabel('Bucket', fontsize=24)
            plt.ylabel('Coordinate', fontsize=24)
            plt.title('Average Positions against Timebucket', fontsize=24)
            plt.legend(fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            ## xacc

            plt.figure(figsize=(20, 10))
            plt.plot(df_xacc['bucket'], df_xacc['xacc_avg'], marker='o', linestyle='-')
            plt.xlabel('Bucket', fontsize=24)
            plt.ylabel('Average Acceleration in x direction', fontsize=24)
            plt.title('Average Acceleration in x direction against Timebucket', fontsize=24)
            plt.xticks(df_xacc.index, df_xacc['bucket'])
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            ## spindleLoad
            plt.figure(figsize=(20, 10))
            plt.plot(df_spindleload['bucket'], df_spindleload['spindleload_avg'], label='spindleload_avg')
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.xlabel('Bucket', fontsize=24)
            plt.ylabel('Average Spindle Load', fontsize=24)
            plt.title('Average Spindle Load against Timebucket', fontsize=24)
            plt.legend(fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            ## spindlespeed
            plt.figure(figsize=(20, 10))  # Adjust the figure size if needed
            plt.plot(df_spindlespeed['bucket'], df_spindlespeed['spindlespeed_avg'], label='spindlespeed_avg')
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.xlabel('Bucket', fontsize=24)
            plt.ylabel('Average Spindle Speed', fontsize=24)
            plt.title('Average Spindle Speed against Timebucket', fontsize=24)
            plt.legend(fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            ## feedrate
            plt.figure(figsize=(20, 10))  # Adjust the figure size if needed
            plt.plot(df_feedrate['bucket'], df_feedrate['feedrate_avg'], label='feedrate_avg')
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.xlabel('Bucket', fontsize=24)
            plt.ylabel('Average Feed Rate', fontsize=24)
            plt.title('Average Feed Rate against Timebucket', fontsize=24)
            plt.legend(fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

    def plotQualityData(self, output_dir, inspection_id, df_rz, df_ra):
        f"""
        This function is used to generate a PDF file, which consists of visualizations of live manufacturing process data. The visualizations are generated through following queries:
        1. queryRz
        2. queryRa
        Inputs: - output_dir                                                              ... Directory to store resulting PDF file
                - workpiece_id                                                            ... Inspection ID to query for
                - df_rz, df_ra                                                            ... Dataframes collected from the queries

        Output: - inspection_id_RaRz.pdf                                                  ... Resulting PDF file
        """
        pdf_filename = os.path.join(output_dir, inspection_id + '_RaRz.pdf')
        with PdfPages(pdf_filename) as pdf:
            ## plot Rz
            plt.figure(figsize=(20, 10))
            plt.plot(df_rz['experiment_window_id'], df_rz['rz'], marker='o', linestyle='-')
            plt.xlabel('Experiment Window ID', fontsize=24)
            plt.ylabel('Rz', fontsize=24)
            plt.title('Rz values against Experiment Window ID', fontsize=24)
            plt.xticks(df_rz.index, df_rz['experiment_window_id'])
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

            ## plot Ra
            plt.figure(figsize=(20, 10))
            plt.plot(df_ra['experiment_window_id'], df_ra['ra'], marker='o', linestyle='-')
            plt.xlabel('Experiment Window ID', fontsize=24)
            plt.ylabel('Ra', fontsize=24)
            plt.title('Ra values against Experiment Window ID', fontsize=24)
            plt.xticks(df_ra.index, df_ra['experiment_window_id'])
            plt.xticks(rotation=90, fontsize=16)
            plt.yticks(rotation=90, fontsize=16)
            plt.tight_layout()
            pdf.savefig()
            plt.close()

