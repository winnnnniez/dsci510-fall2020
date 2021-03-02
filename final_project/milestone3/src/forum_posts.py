import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_web_content(url):
    content = requests.get(url)
    soup = BeautifulSoup(content.content, features='html.parser')
    content.close()
    return soup

# get posts from a single page
def extract_forum_posts(n):
    """takes an integer representing page number,
    returns a string containing titles of the posts in that page

    Int -> Str"""

    url = f'https://www.belltreeforums.com/forums/new-neighbor-network.244/page-{n}'
    soup = get_web_content(url)

    titles_in_one_page = str()
    # find the main part of posts
    main = soup.find('div', {'class':'structItemContainer-group js-threadList'})
    # find titles of the posts
    try:
        for x in main.find_all('a', {'data-tp-primary':'on'}):
            titles_in_one_page += ' ' + x.text
    except AttributeError:
        titles_in_one_page += ''
    return titles_in_one_page

# get all the posts from page 1 to page n
def extract_all_titles(n):
    """takes an integer n,
    returns a string containing all titles of the posts in the first n pages

    Int -> Str"""

    all_titles = str()
    for i in range(1, n+1):
        all_titles += extract_forum_posts(i)
    return all_titles

# def save_to_text(string_content):
#     """takes a string,
#     saves it to a text file in the 'data' folder
#
#     Str -> None"""
#
#     with open('data/raw_forum_posts.txt', 'w') as text_file:
#         text_file.write(string_content)

def modeling_forum_posts(post_string, df_villagers_ranking):
    """takes a string (raw_forum_posts) and df_villagers_ranking as reference
    returns a dataframe that has been modeled

    Str, DataFrame -> DataFrame"""
    name_list = df_villagers_ranking['name'].tolist()

    # villagers_count_list contains 391 dictionaries in the format:
    #   {names of villagers(str): in how many posts the village's name has been mentioned}
    count_list = list()
    for name in name_list:
        count_dict = dict()
        count_dict['name'] = name
        # find all occurrence of each name
        count = re.findall(r'[^a-z]{}[^a-z]'.format(name.lower()), post_string.lower())
        count_dict['count'] = len(count)
        count_list.append(count_dict)

    df_posts_count = pd.DataFrame(count_list)
    return df_posts_count

def save_to_csv(df):
    """takes a dataframe,
    saves it to csv file in the 'data' folder

    DataFrame -> None"""

    df.to_csv('data/posts_count.csv', index=False)
