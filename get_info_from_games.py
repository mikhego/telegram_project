import time
import requests
import pandas as pd
from tqdm import tqdm
import glob, os

from src.parsing.parsing_functions import (check_data, get_games_info, find_or_create_data_file, MODULE_PATH)

file_path = os.path.join(MODULE_PATH + f'/data/raw/games_info/', 'data_info_*.csv') 
csv_files = glob.glob(file_path)


if __name__ == '__main__':
    check_data()
    data_games_list: pd.DataFrame = pd.read_csv(MODULE_PATH + '/data/raw/data_games_list.csv')
    data_info: pd.DataFrame = find_or_create_data_file(filename='/data/raw/data_info.csv', columns=['id', 'tags', 'info', 'tags_info'])
    set_games_list: set = set(data_games_list['id'].unique())
    set_games_info: set = set(data_info['id'].unique())
    diff_set: set = set_games_list.difference(set_games_info)

    if len(diff_set) > 0:
        for games_id in tqdm(diff_set):
            game_file =  MODULE_PATH + f'/data/raw/games_info/data_info_{games_id}.csv'
            if  game_file in csv_files:
                pass
            else:
                i = 0
                while i < 3:
                    try:
                        get_games_info(games_id=games_id)
                    except (SystemExit, requests.exceptions.ChunkedEncodingError) as error:
                        print('CONNECTION ERROR (have to wait)')
                        print(f'stopped_games_id: {games_id}')
                        print('\n time to sleep (30 min).. z-z-z')
                        time.sleep(2100)
                        continue
                    i += 1

        print('get_games_info COMPLETED')
        print('concat get_games_info to data_info')
        df_concat = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
        df_concat.to_csv(MODULE_PATH + '/data/raw/data_info.csv', index=False)
    else:
        print('get_games_info FULL')
