import os
import pandas as pd
from datetime import datetime
import time

env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
root_path =  os.getenv(env_name_root)

class EdgeApplication:

    def mock_data(self, time_offset: int = 160000):                #86400):  # seconds = 1 day
        """
        Generates fake experimental and meta data.
        Example usage:
            processID, fake_metadata, fake_rawdata = mock_data(time_offset_in_seconds)
        """

        relative_path = os.path.join(root_path, 'data\inputs\mockFiles')
        list_files = os.listdir(relative_path)
        fake_rawdata = []
        Process_ID = []

        for lf in list_files:
            files_path = os.path.join(relative_path, lf)
            files = os.listdir(files_path)
            for file in files:
                if file[-4:] == '.csv':
                    if file[:3] == 'Acc':
                        file_acc = os.path.join(files_path, file)
                        df_acc = pd.read_csv(file_acc, delimiter=',')
                        df_acc['timestamp'] = df_acc['timestamp'] + time_offset
                        fake_rawdata.append(df_acc)
                    else:
                        file_nc = os.path.join(files_path, file)
                        df_nc = pd.read_csv(file_nc, delimiter=',', header=None)
                        df_nc[0] = df_nc[0] + time_offset
                        Process_ID.append(round(df_nc.iloc[0, 0] - 120))
                        fake_rawdata.append(df_nc)
        experiment_15 = [
            ('1_5', ('1681457102.628018', '1681457142.556514'), ('1681457130.996333', '1681457135.812401'),
             ('1681457130.997339', '1681457135.811356')),
            ('2_6', ('1681457142.692529', '1681457181.452762'), ('1681457152.052484', '1681457175.788707'),
             ('1681457152.052521', '1681457175.7881029')),
            ('3_7', ('1681457181.597028', '1681457200.524968'), ('1681457187.116821', '1681457195.276909'),
             ('1681457187.117988', '1681457195.274472')),
            ('4_8', ('1681457200.669055', '1681457243.822219'), ('1681457208.037031 ', '1681457231.909257'),
             ('1681457208.037736', '1681457231.908303')),
            ('5_9', ('1681457264.33367', '1681457327.334196'), ('1681457284.517891', '1681457311.854025'),
             ('1681457284.518571', '1681457311.8518589')),
            ('5_10', ('1681457327.470413', '1681457381.631079'), ('1681457342.318353', '1681457367.406554'),
             ('1681457342.321431', '1681457367.406178')),
            ('6_11', ('1681457400.430972', '1681457465.695558'), ('1681457415.79104', '1681457446.183436'),
             ('1681457415.792035', '1681457446.1831665')),
            ('6_12', ('1681457465.839617', '1681457540.5522'), ('1681457484.519696', '1681457527.048202'),
             ('1681457484.52043', '1681457527.039943'))
        ]
        list_operation = [4, 5, 6, 7, 8, 9, 10, 11]
        fake_metadata = []  # ~ array wie "experiment_15"
        for i in range(len(experiment_15)):
            # operation = experiment_15[i][0]     # 1681450102_4   = <Process-ID>_4 ... <Process-ID>_11
            ts_start_operation = float(experiment_15[i][1][0]) + time_offset                                    # Daten aus NC Machine für die ganze Operation inkl. Wege in der Luft (Anfahrtweg)
            ts_end_operation = float(experiment_15[i][1][1]) + time_offset
            ts_start_position = float(experiment_15[i][2][0]) + time_offset                                     # Daten aus NC Machine nur im Kontakt mit dem Werkstück (Eingriff)
            ts_end_position = float(experiment_15[i][2][1]) + time_offset
            ts_start_acc = float(experiment_15[i][3][0]) + time_offset                      
            ts_end_acc = float(experiment_15[i][3][1]) + time_offset
            if experiment_15[i][0] in ['1_5', '2_6', '3_7', '4_8']:
                fake_metadata.append((str(Process_ID[0]) + '_' + str(list_operation[i]),
                                      (ts_start_operation, ts_end_operation), (ts_start_position, ts_end_position),
                                      (ts_start_acc, ts_end_acc)))
            if experiment_15[i][0] in ['5_9', '5_10']:
                fake_metadata.append((str(Process_ID[1]) + '_' + str(list_operation[i]),
                                      (ts_start_operation, ts_end_operation), (ts_start_position, ts_end_position),
                                      (ts_start_acc, ts_end_acc)))
            if experiment_15[i][0] in ['6_11', '6_12']:
                fake_metadata.append((str(Process_ID[2]) + '_' + str(list_operation[i]),
                                      (ts_start_operation, ts_end_operation), (ts_start_position, ts_end_position),
                                      (ts_start_acc, ts_end_acc)))
        current_time = datetime.fromtimestamp(time.time())
        id_format = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        processId="pro_"+id_format

        return processId, fake_metadata, fake_rawdata

