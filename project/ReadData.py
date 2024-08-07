import pandas as pd
import numpy as np
def preprocess_data(path):
        # dataset = pd.read_csv('simulated.csv')
        dataset = pd.read_csv(path)
        dataset = dataset.dropna()

        # dataset.columns
        # dataset.groupby(['Timestamp'])
        new_columns = [i for i in dataset.columns.copy()]
        for index , elem in enumerate(new_columns.copy()):
          if 'Values _Row' in elem:
            new_columns[index] = f'Unnamed: {index+1}'


        dataset.columns = new_columns
        # new_columns
        df = dataset.select_dtypes(include=['int64'])
        new_columns = [f'Sensor:{i}' for i in range(len(dataset.select_dtypes(include=['int64']).columns))]
        new_columns
        df.columns = new_columns

        df = df[:-1]


        ### separating columns by 24 (number of censors)
        start_idx = 0
        sub_dfs = list()
        for i in range(1, 5):
          end_idx = i * 24
          sub_df_columns = new_columns[start_idx:end_idx]
        #   print(sub_df_columns)
          sub_dfs.append(df[sub_df_columns])
          start_idx = end_idx 

        # sub_dfs

        splitted_data = list()
        for sub_df in sub_dfs:
          splitted_data.append(np.array_split(sub_df, int((len(df))/24)))

        # splitted_data[0][0], splitted_data[0][1]



        # Iterate over each column in the DataFrame


        # print(columns_over_2000)
        jump_list = [[],[]]
        pressure_list = [[],[]]
        for i in range(len(splitted_data[:2])):
          for idx, tile_data in enumerate(splitted_data[i]):
            # columns_over_2000 = []
            for column in tile_data.columns:
              # Convert the column to numeric, setting errors='coerce' to turn non-numeric values into NaN
              numeric_column = pd.to_numeric(tile_data[column], errors='coerce')

              # Check if any value in the column is greater than 2000
              if numeric_column.max() > 2000:
                # print(numeric_column.max())
                # print('spotted!', idx, column)
                jump_list[i].append(idx)
                pressure_list[i].append(tile_data.mean())
                # print(len(numeric_column))
                break
            
                  # columns_over_2000.append(column)
        len(jump_list[0])



        jumps = []
        def find_jumps(j_list):
          for i in range (len(j_list) - 1):
            if j_list[i+1] - j_list[i] > 1:
            
              jump_time = (j_list[i+1] - j_list[i]) * 0.3
              left_pressure = sum(pressure_list[0][i+1])/len(pressure_list[0][i+1])
              right_pressure = sum(pressure_list[1][i+1])/len(pressure_list[1][i+1])
            #   print(f'Player has been on the air for {jump_time:.2f}' ,j_list[i+1] , j_list[i])
            #   print(f' Left foot avg pressure {left_pressure:.2f}, Right foor avg pressure {right_pressure:.2f} \n')

              jump = {'jump duration':(j_list[i+1] - j_list[i]) * 0.3}
              jump['pressure'] = (left_pressure, right_pressure)
              jumps.append(jump)

          return jumps
    

        results = find_jumps(jump_list[0])
        return results
