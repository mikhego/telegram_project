import time
import requests
import pandas as pd

from src.parsing.parsing_functions import (check_data, get_games_info, MODULE_PATH)





      
if __name__ == '__main__':
    check_data()
    data_games_list = pd.read_csv(MODULE_PATH + '/data/raw/data_games_list.csv')

    number_games = 0
    while number_games < data_games_list['id'].nunique():
        try:
            print('\n time to parse data..')
            check_list = get_games_info(games_list=data_games_list['id'].unique())
        except (SystemExit, requests.exceptions.ChunkedEncodingError) as error:
            print('CONNECTION ERROR (have to wait)')
            pass
        temp_df = pd.read_csv(MODULE_PATH + '/data/raw/data_info.csv')
        number_games = temp_df['id'].nunique()
        print(f'get games: {number_games} of {data_games_list["id"].nunique()}')
        if number_games != data_games_list['id'].nunique():
            print('\n time to sleep (30 min).. z-z-z')
            time.sleep(1900)
        else:
            print('get_games_info COMPLETED')



