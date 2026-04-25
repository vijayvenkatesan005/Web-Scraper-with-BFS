import requests
from bs4 import BeautifulSoup
from collections import deque

def scrape_web_page(url):
    BASE_PATH = "https://en.wikipedia.org"

    headers = {
        'User-Agent': 'my-app/1.0.0',
        'Accept': 'text/html',
        'Content-Type': 'application/json'
    }

    response = requests.get(f"{BASE_PATH}{url}", headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    main_content = soup.find(id='bodyContent')

    tags = main_content.find_all('a')

    links = set()

    for tag in tags:
        link = tag.get('href')
        if link and link.startswith('/wiki') and ":" not in link:
            links.add(link)

    return links

def bfs(source_url, destination_url):
    queue = deque()
    queue.append((source_url, [source_url]))

    visited = set()
    visited.add(source_url)

    while queue:
        current_url, current_path = queue.popleft()
        if current_url == destination_url:
            return current_path
        neighbor_urls = scrape_web_page(current_url)
        for neighbor_url in neighbor_urls:
            if neighbor_url == destination_url:
                return current_path + [destination_url]
            if neighbor_url not in visited:
                updated_path = current_path.copy()
                updated_path.append(neighbor_url)
                queue.append((neighbor_url, updated_path))
                visited.add(neighbor_url)
    
    return None

if __name__ == "__main__":
    source_url_relative_path = "/wiki/Python_(programming_language)"
    destination_url_relative_path = "/wiki/Isaac_Newton"

    shortest_path = bfs(source_url_relative_path, destination_url_relative_path)
    print(shortest_path)








