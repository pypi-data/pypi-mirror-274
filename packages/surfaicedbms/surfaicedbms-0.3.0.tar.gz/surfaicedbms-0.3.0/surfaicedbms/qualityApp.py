import os
import pandas as pd

env_name_config = 'surfaice_dbms_config'
env_name_root = 'surfaice_dbms_root'
config_path = os.getenv(env_name_config)
root_path =  os.getenv(env_name_root)

class RaRz:
    def node_calc_RaRz_static_window_size(self, window_size, inspection_id):
        """
        This function is used for calculating Ra and Rz values from processed data of quality profiles.
        The function is prepared by IFT to simulate an example calculation of related values, therefore it might not necessarily calculate exact values.
        The function uses merged_data.csv file in data\outputs\formedProfiles directory as an input,
        and generates an output of calculated values in data\outputs\rarz directory with respected inspection id,
        which will eventually stored in available PostgreSQL connection.
        The data processing includes following steps:
        - Calculation of Ra and Rz
        - Inserting inspection id to resulting dataframe
        - Exporting the file in a compressed gzip format to ease data ingestion
        - Returning resulting dataframe [CAN BE EXCLUDED]
        Input:              - merged_data.csv in data\outputs\formedProfiles                                  ... output of formQuality() method
                            - window_size                                                                     ... a parameter regarding current evaluation length (in our case 4)
                            - inspection_id                                                                   ... identification number of quality measurment

        Output:             - rarz_output.csv.gz in data\outputs\rarz directory                               ... resulting tabular data of rarz calculations as compressed csv file
                            - df_profile_out                                                                  ... resulting tabular data of rarz calculations as dataframe [CAN BE EXCLUDED]
        """
        input_path = os.path.join(root_path,'data\outputs\\formedProfiles\merged_data.csv')
        df_profile=pd.read_csv(input_path,encoding ="Latin")
        output_path = os.path.join(root_path,'data\outputs\\rarz')
        df_profile_RaRz_static_window = pd.DataFrame([], columns=df_profile.columns)

        lr = window_size
        ln = 5 * lr

        # assign windows of length ln = 5* lr (window_size)

        def get_window_id(df):
            df['window_id'] = ((df['distance_mm'] - df['distance_mm'].min()) // ln).astype(int)

            last_window = df[df['window_id'] == df['window_id'].max()]

            # drop the last window, which might be incomplete

            df = df[~(df['window_id'] == df['window_id'].max())]

            return df

        def get_RaRz_from_window(df):
            '''
                window ids are [0.0
            '''

            def get_Rz_ln(df):
                def _get_Rz_lr(subwindow):
                    subwindow['Rz_lr'] = subwindow['height_µm'].max() - subwindow['height_µm'].min()

                    return subwindow

                # each window is devided into 5 subwindows
                # final Rz is the mean over the 5 subwindow amplitudes

                df['Rz'] = df.groupby(df.index // (len(df) / 5), group_keys=False).apply(_get_Rz_lr)[
                    'Rz_lr'].unique().mean()

                return df

            def get_Ra_ln(df):
                # mean over the whole window is equal to mean over subwindows

                df['Ra'] = df['height_µm'].abs().mean()

                return df

            df = df.groupby('window_id', group_keys=False).apply(get_Rz_ln)

            df = df.groupby('window_id', group_keys=False).apply(get_Ra_ln)

            return df

        df_profile_window = df_profile.groupby('experiment_id', as_index=False).apply(get_window_id)

        df_profile_window.index = df_profile_window.index.map(lambda x: x[1])  # remove multiindex

        df_profile_out = df_profile_window.groupby('experiment_id', group_keys=False).apply(get_RaRz_from_window)

        # finally doublecheck that there is indeed only one Ra/Rz per experiment_id and window_id

        all_vals_equal = lambda x: len(x.unique()) == 1

        assert df_profile_out.groupby(['experiment_id', 'window_id']).agg({'Rz': all_vals_equal}).all().iloc[0]
        assert df_profile_out.groupby(['experiment_id', 'window_id']).agg({'Ra': all_vals_equal}).all().iloc[0]

        # modification Kap
        selected_columns = ['experiment_id', 'window_id', 'Rz', 'Ra']
        df_profile_out = df_profile_out[selected_columns]
        df_profile_out = df_profile_out.groupby(['experiment_id', 'window_id', 'Rz', 'Ra']).size().reset_index(
            name='count')

        df_profile_out = df_profile_out.drop('count', axis=1)


        df_profile_out.insert(0, 'inspection_id', inspection_id)

        # TEMPORARY STORAGE WITH GZIP #
        df_profile_out.to_csv(output_path+"\\rarz_output.csv.gz", index=False, compression='gzip')
        return df_profile_out