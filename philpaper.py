from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

def find_all_innermost_groups(group):
    inner_groups = group.find_all(class_='group', recursive=False)
    if not inner_groups:
        return [group]
    else:
        innermost_groups = []
        for g in inner_groups:
            innermost_groups.extend(find_all_innermost_groups(g))
        return innermost_groups

url = "https://philpapers.org/recent?latest=1&filterByAreas=off&onlineOnly=&hideAbstracts=&in_a=off&tz_offset=0&showAbstract=on&newWindow=&proOnly=on&categorizerOn=&in_w=off&langFilter=&publishedOnly=off&sqc=&showCategories=on&nosh=1&in_l=off&in_j=on&freeOnly=off&offset=31&range=90&sort=&format=html&start=100&limit=&jlist=all&ap_c1=&ap_c2="
headers = {'User-Agent': 'Mozilla/5.0'}
req = Request(url, headers=headers)
results = []

try:
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')
    soup = BeautifulSoup(webpage, 'html.parser')
    all_groups = soup.find_all(class_='group')
    innermost_groups = []
    for group in all_groups:
        innermost_groups.extend(find_all_innermost_groups(group))
except Exception as e:
    print(f"Failed to retrieve or parse the webpage: {e}")
    innermost_groups = []

for group in innermost_groups:
    temp = {}
    publish = group.select_one('a.pub_name')
    header = group.select_one('div.header_issue')
    title = group.select_one("span.articleTitle")
    authors = group.select("a.discreet")
    authors = [tag for tag in authors if tag.get('class') == ['discreet']]
    abstract = group.select_one("div.abstract")
    categories = group.select_one("div.catsCon")

    temp["publish"] = publish.text.strip() if publish else "No publisher found"
    temp["header"] = header.text.strip() if header else "No issue found"
    temp["title"] = title.text.strip() if title else "No title found"
    temp["authors"] = [author.text.strip() for author in authors] if authors else []
    temp["abstract"] = abstract.text.strip() if abstract else "No abstract found"
    temp["categories"] = categories.text.strip() if categories else "No categories found"

    results.append(temp)

print(f"Total groups processed: {len(results)}")
with open('result.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)