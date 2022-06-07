#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

def crawl(addSource):
    url = "https://www.10000recipe.com/recipe/list.html?q=" + addSource
    recipe_url = "https://www.10000recipe.com"

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    recipe_titles = []
    recipe_links = []
    recipe_contents = []
    recipes = []

    res = soup.find("ul", "rcp_m_list2")
    titles = res.find_all("div", "common_sp_caption_tit line2")
    links = res.find_all("a", "common_sp_link")

    for title in titles:
        recipe_titles.append(title.get_text())

    for link in links:
        recipe_links.append(recipe_url + link["href"])

    for recipe_link in recipe_links:
        page = requests.get(recipe_link)
        soup = BeautifulSoup(page.content, "html.parser")

        res = soup.find("div", "view_step")

        res = res.find_all("div", "media-body")

        recipe = ""

        for i in res:
            recipe += i.get_text().replace("\n", "")

        recipe_contents.append(recipe)

    for i in range(len(recipe_contents)):
        recipes.append({"title" : recipe_titles[i], "link" : recipe_links[i], "recipe" : recipe_contents[i]})
    
    return recipes