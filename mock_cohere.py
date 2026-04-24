import requests
from bs4 import BeautifulSoup
from collections import deque

def scrape_data(url) -> set[str]:

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)

    html_text = response.text

    soup = BeautifulSoup(html_text, 'html.parser')

    main_content = soup.find(id="bodyContent")

    if main_content:
        tags = main_content.find_all('a')

    internal_wiki_links = set()

    if main_content:
        for tag in tags:
            link = tag.get('href')
            if link and link.startswith('/wiki/') and ':' not in link:
                internal_wiki_links.add(link)

    return internal_wiki_links

#Nodes -> url links
#Edges -> the hyperlink from url A to url B
def bfs(source_url, internal_wiki_links, keyword='Automation', base_url="https://en.wikipedia.org") -> list[str]:
    queue = deque()
    queue.append((source_url, [source_url]))

    visited = set()
    visited.add(source_url)

    while queue:
        curent_url, current_path = queue.popleft()
        if keyword in curent_url:
            return current_path
        # give full path to the current_url
        neighbor_urls_set = scrape_data(f"{base_url}{curent_url}") 
        for neighbor_url in neighbor_urls_set:
            if neighbor_url not in visited:
                updated_path = current_path.copy()
                updated_path.append(neighbor_url)
                queue.append((neighbor_url, updated_path))
                visited.add(neighbor_url)
    
    return None

if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/Web_scraping"
    internal_wiki_links = scrape_data(url)
    # print(internal_wiki_links)
    # shortest_path_links = bfs("/wiki/Web_scraping", internal_wiki_links, keyword="Web_scraping")
    # shortest_path_links = bfs("/wiki/Web_scraping", internal_wiki_links, keyword="Data_scraping")
    shortest_path_links = bfs("/wiki/Web_scraping", internal_wiki_links, keyword="Data_structure")
    print(shortest_path_links)



