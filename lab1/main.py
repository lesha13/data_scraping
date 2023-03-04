from requests import get
from bs4 import BeautifulSoup

BASE_URL = "https://www.uzhnu.edu.ua"
URL = BASE_URL + "/uk/cat/faculty"

# my user agent
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}
page = get(URL, headers=HEADERS)

# print(page.text)
page = BeautifulSoup(page.content, "html.parser")

with open("data.txt", "w", encoding='utf-8') as f:
    for fac in page.find(id="yw0").find_all("a"):
        txt = fac.text[2::]
        url = BASE_URL + fac["href"]
        print(txt)
        print(url)
        f.writelines(txt + "\n")
        f.writelines(url + "\n")

        p = BeautifulSoup(get(url, headers=HEADERS).content, "html.parser")
        # print(p.text)

        for news in p.select("#yw2 > div.items > div.anounce.compact"):
            day = news.find(class_="day").text
            month = news.find(class_="month").text
            a = news.a.text.strip()
            href = news.a["href"]
            f.write(f"\t{day} {month}:\n")
            f.write(f"\t\t{a}.\n", )
            f.write(f"\t\t{BASE_URL + href}\n\n")
