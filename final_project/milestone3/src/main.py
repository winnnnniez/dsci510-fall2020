import villagers_info as info
import villagers_ranking as ranking
import forum_posts as post
import os
import argparse

# web scraper / api crawler
def villagers_ranking_web_scraper():
    """gets villagers ranking from web scraping,
    returns the raw data as a list

    None -> List"""

    ranking_list = ranking.extract_ranking_list()
    return ranking_list

def villagers_info_api_crawler():
    """gets villagers' infomation from nookipedia api,
    returns the raw data as a list

    None -> List"""

    info_list = info.extract_villagers_info()
    return info_list

def forum_posts_web_scraper(page=900):
    """gets titles of forum posts from web scraping,
    returns the raw data as a string

    None -> Str"""

    # there are total 930 pages of posts in the forum
    if page > 930:
        page = 930
    title_string = post.extract_all_titles(page)
    return title_string

# get data remotely
def get_data_remotely(page=900):
    """gets three raw data from remote source,
    creates the 'data' folder if the folder does not exist,
    returns a tuple of the three datasets

    None -> Tuple (List, List, Str)"""

    characters_ranking_raw = villagers_ranking_web_scraper()
    print('get raw_characters_ranking from remote source and update to local succesfully\n')

    villagers_info_raw = villagers_info_api_crawler()
    print('get raw_villagers_info from remote source and update to local succesfully\n')

    if page >= 900:
        print('Starting to get forum_posts_raw from remote source ...')
        print('This takes 10-15 minutes! Take a break!\n')
    forum_posts_raw = forum_posts_web_scraper(page)
    print('get raw_forum_posts from remote source and update to local succesfully\n')

    return characters_ranking_raw, villagers_info_raw, forum_posts_raw

# process and model the data
def model_data(data):
    """takes a tuple containing three raw datasets,
    returns a tuple containing three dataframes that have been modeled

    Tuple (List, List, Str) -> Tuple (DataFrame, DataFrame, DataFrame)"""

    df_villagers_info = info.modeling_villagers_info(data[1])
    df_villagers_ranking = ranking.modeling_villagers_ranking(data[0], df_villagers_info)
    df_posts_count = post.modeling_forum_posts(data[2], df_villagers_ranking)

    return df_villagers_ranking, df_villagers_info, df_posts_count

# store the modeled data
def store_data(data_df):
    """takes a tuple contatining three dataframes,
    stores the data to csv files in the 'data' folder

    Tuple -> None"""

    ranking.save_to_csv(data_df[0])
    info.save_to_csv(data_df[1])
    post.save_to_csv(data_df[2])
    print("data have been updated and stored as csv files in the 'data' folder\n")
