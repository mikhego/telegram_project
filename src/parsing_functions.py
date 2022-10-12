import os
import sys
import requests
import pandas as pd
import lxml
import random

from tqdm import tqdm
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from pathlib import Path

module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

MODULE_PATH = module_path
print(MODULE_PATH)

platforms_list = ['PC', 'PS', 'PS2', 'PS3', 'PS4', 'PS5', 'Switch', 'Xbox%20One', 'Xbox%20360', 'Xbox%20Series']


def find_or_create_data_file(filename: str, columns: list)-> pd.DataFrame:
    raw_file = Path(MODULE_PATH + filename)
    if raw_file.is_file():
        print(f'{filename} EXIST. GO TO THE NEXT STEP')
        df = pd.read_csv(MODULE_PATH + filename)
        return df
    else:
        print(f'{filename} NOT EXIST. GO TO CREATE FILE')
        df = pd.DataFrame(columns=columns)
        return df



def get_count_games_from_platform(platform_name: str) -> int:
    URL_PLATFORM = f'http://www.world-art.ru/games/list.php?limit_1=00&platform={platform_name}'

    result = requests.get(URL_PLATFORM, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(result.text, "lxml")
    for item in soup.find_all('b'):
        if 'найдено' in item.text:
            count_games = int(item.text.split(': ')[-1])
            platform_name = platform_name.replace('%20', '_')        
            print(f'{platform_name}: detecting {count_games} games in DB')
    return count_games


def get_games_from_platform(platforms_list: list):
    list_games = []
    data_games_list = find_or_create_data_file(filename='/data/raw/data_games_list.csv', columns=['link', 'name', 'id', 'platform'])
    for platform_name in platforms_list:
        games_count = get_count_games_from_platform(platform_name)
        for n in tqdm(range(0, games_count, 25)):
            URL_LIST =  'http://www.world-art.ru/games/list.php?limit_1=' + str(n) + f'&platform={platform_name}'
            try:    
                result = requests.get(URL_LIST, headers={'User-Agent': UserAgent().chrome})
                soup = BeautifulSoup(result.text, "html.parser")
                games_on_page = soup.find_all('a', class_='h3')
                for game in games_on_page:
                    link = 'http://www.world-art.ru/games/' + game.get('href')
                    name = game.text.strip()
                    id_game = int(link.split('=')[1].strip())
                    if id_game not in data_games_list['id'].unique():
                        game_dict = {
                            'link': link,
                            'name': name,
                            'id': id_game,
                            'platform': platform_name.replace('%20', '_')
                                    }
                                    
                        temp_df  = pd.DataFrame([game_dict], columns=game_dict.keys())
                        data_games_list = pd.concat([data_games_list, temp_df], axis =0)
                        data_games_list.to_csv(MODULE_PATH + '/data/raw/data_games_list.csv', index=False)
                    else:
                        pass

            except requests.exceptions.ChunkedEncodingError:
                print('ConnectionError')
                pass


def check_data():
    raw_games_file = Path(MODULE_PATH + '/data/raw/data_games_list.csv')
    if raw_games_file.is_file():
        print('\n CHECK FILE: /data/raw/data_games_list.csv - OK')
        data_games_list = pd.read_csv(raw_games_file)
        count_data_games = data_games_list['id'].nunique()
        count_db_games = 0
        for platform_name in platforms_list:
            count_db_games += get_count_games_from_platform(platform_name)

        if count_data_games != count_db_games:
            print(f'\n * /data/raw/data_games_list.csv contains {count_data_games} games of {count_db_games} - WARNING')
            user_answer = input('UPDATE /data/raw/data_games_list.csv? (yes or no): ')
            while (user_answer != 'yes' and user_answer != 'no'):     
                user_answer = input('yes or no? ')
            if user_answer == 'yes':
                print('START UPDATE /data/raw/data_games_list.csv:\n')
                get_games_from_platform(platforms_list)
                print('\n UPDATE /data/raw/data_games_list.csv COMPLETED:\n')
                return check_data()

            elif user_answer == 'no': 
                print('/data/raw/data_games_list.csv NOT UPDATED\n')
        else:
            print(f'\n /data/raw/data_games_list.csv contains {count_data_games} games of {count_db_games} - OK')
    else:
        print('\n CHECK FILE: /data/raw/data_games_list.csv - ERROR')

        user_answer = input('create data_games_list? (yes or no): ')
        while (user_answer != 'yes' and user_answer != 'no'):     
            user_answer = input('yes or no? ')
        if user_answer == 'yes':
            print('START get_games_from_platform:\n')
            get_games_from_platform(platforms_list)
            print('\n /data/raw/data_games_list.csv COMPLETED:\n')
            return check_data()
        elif user_answer == 'no': 
            print('/data/raw/data_games_list.csv NOT CREATED\n')







def parsing_games_info(id):
    result = requests.get(f'http://www.world-art.ru/games/games.php?id={id}' , headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(result.text, "lxml")
    tags = []
    tags_info= []
 
    if len(soup.find_all("a", class_='newtag1')) == 0:
        tags = 'no_tags'
        tags_info = 'no_tags_info'
        try:    
            info = soup.find('p', class_ = 'review').text
        except AttributeError as error:
            info = 'no_data'
            print('STOP PARSING')
            sys.exit(1)
    else:
        for i in soup.find_all("a", class_='newtag1'):
            tags.append(i.text)
            tags_info.append(i.get('title'))
            try:    
                info = soup.find('p', class_ = 'review').text
            except AttributeError as error:
                info = 'no_data'
                print('STOP PARSING')
                sys.exit(1)

    info_dict = {
                'id': id,
                'tags' : tags,
                'info': info,
                'tags_info': tags_info
                    }

    return info_dict
    

def get_games_info(games_list: list) -> list:
    print(f'games counts: {len(games_list)}')
    data_info = find_or_create_data_file(filename='/data/raw/data_info.csv', columns=['id', 'tags', 'info', 'tags_info'])
    for id in tqdm(games_list):
        if id not in data_info['id'].unique():
            try:
                info_dict = parsing_games_info(id)

                temp_df  = pd.DataFrame([info_dict], columns=info_dict.keys())
                data_info = pd.concat([data_info, temp_df], axis =0)
                data_info.to_csv(module_path + "/data/raw/data_info.csv", index=False)

            except requests.ConnectionError:
                pass
        else:
            pass
        
    return data_info['id'].unique()

