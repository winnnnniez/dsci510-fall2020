import villagers_info as info
import villagers_ranking as ranking
import forum_posts as post
import os
import json
import argparse

# web scraper / api crawler
def villagers_ranking_web_scraper():
    """gets villagers ranking from web scraping,
    stores the data to a json file in the 'data' foleder,
    returns the raw data as a list

    None -> List"""

    ranking_list = ranking.extract_ranking_list()
    ranking.save_to_json(ranking_list)

    return ranking_list

def villagers_info_api_crawler():
    """gets villagers' infomation from nookipedia api,
    stores the data to a json file in the 'data' foleder,
    returns the raw data as a list

    None -> List"""

    info_list = info.extract_villagers_info()
    info.save_to_json(info_list)

    return info_list

def forum_posts_web_scraper(page=900):
    """gets titles of forum posts from web scraping,
    stores the data to a text file in the 'data' foleder,
    returns the raw data as a string

    None -> Str"""
    # there are total 925 pages of posts in the forum
    if page > 925:
        page = 925

    title_string = post.extract_all_titles(page)
    post.save_to_text(title_string)

    return title_string

# get data remotely
def get_data_remotely(page=900):
    """gets three raw data from remote source,
    creates the 'data' folder if the folder does not exist,
    stores the raw data to the 'data' folder
    returns a tuple of the three datasets

    None -> Tuple (List, List, Str)"""

    # create 'data' folder if not exist
    if not os.path.exists('data'):
        os.makedirs('data')
        print("the 'data' folder has been created\n")

    characters_ranking_raw = villagers_ranking_web_scraper()
    print('get raw_characters_ranking from remote source and store/update to local succesfully\n')

    villagers_info_raw = villagers_info_api_crawler()
    print('get raw_villagers_info from remote source and store/update to local succesfully\n')

    if page >= 900:
        print('Starting to get forum_posts_raw from remote source ...')
        print('This takes about 10 minutes! Take a break!\n')
    forum_posts_raw = forum_posts_web_scraper(page)
    print('get raw_forum_posts from remote source and store/update to local succesfully\n')

    return characters_ranking_raw, villagers_info_raw, forum_posts_raw

# get data locally
def get_data_locally():
    """gets three raw data from local source,
    returns a tuple containing three datasets

    None -> Tuple (List, List, Str)"""

    if not os.path.exists('data'):
        print("data do not exist, please get data from remote source first")
        exit()

    with open('data/raw_characters_ranking.json') as f1:
        characters_ranking_raw = json.load(f1)
    print('get raw_characters_ranking from local source succesfully\n')

    with open('data/raw_villagers_info.json') as f2:
        villagers_info_raw = json.load(f2)
    print('get raw_villagers_info from local source succesfully\n')

    with open('data/raw_forum_posts.txt') as f3:
        forum_posts_raw = f3.read()
    print('get raw_forum_posts from local source succesfully\n')

    return characters_ranking_raw, villagers_info_raw, forum_posts_raw

# process and model data
def modeling_data(data):
    """takes a tuple containing three raw datasets,
    returns a tuple containing three dataframes that have been modeled

    Tuple (List, List, Str) -> Tuple (DataFrame, DataFrame, DataFrame)"""

    df_villagers_info = info.modeling_villagers_info(data[1])
    print("villagers_info has been modeled\n")
    # modeling data[0] requires reference to modeled data[1]
    df_villagers_ranking = ranking.modeling_villagers_ranking(data[0], df_villagers_info)
    print("villagers_ranking has been modeled\n")
    # modeling data[2] requires reference to modeled data[0]
    df_posts_count = post.modeling_forum_posts(data[2], df_villagers_ranking)
    print("forum_posts_count has been modeled\n")

    return df_villagers_ranking, df_villagers_info, df_posts_count

# store the modeled data
def store_data(data_df):
    """takes a tuple contatining three dataframes,
    stores the data to csv files in the 'data' folder

    Tuple -> None"""

    ranking.save_to_csv(data_df[0])
    info.save_to_csv(data_df[1])
    post.save_to_csv(data_df[2])
    print("three modeled data have been stored as csv files in the 'data' folder\n")

# main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source',
                        choices=['remote', 'local'],
                        required=True,
                        type=str,
                        help="choose data source, 'remote' or 'local'")

    parser.add_argument('--grade',
                        action='store_true',
                        required=False,
                        help='grab up to 3 of each data source when invoked')

    args = parser.parse_args()
    source = args.source
    grade = args.grade

    # remote source
    if source == 'remote':
        # if grade, only scrape 3 pages
        if grade:
            raw_data = get_data_remotely(page=3)
        else:
            raw_data = get_data_remotely()
    # local source
    else:
        raw_data = get_data_locally()

    # model & store data
    modeled_data = modeling_data(raw_data)
    store_data(modeled_data)
