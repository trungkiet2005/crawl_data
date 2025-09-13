from bs4 import BeautifulSoup

with open("response.txt", "r", encoding="utf-8") as f:
    response = f.read()

soup = BeautifulSoup(response, "html.parser")
# print(soup.prettify())

links = [a["href"] for a in soup.find_all("a", href=True)]

for link in links:
    print(link)
    text_split = link.split("/")
    print(text_split)