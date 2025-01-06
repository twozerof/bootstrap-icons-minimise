import os
from bs4 import BeautifulSoup
import requests
import time

abs_path = os.path.dirname(os.path.abspath(__file__))
sitemap = "http://test.xyz/sitemap.xml" #your sitemap
to = 3 #timeout
headers = {
    "user-agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36"
}

def getPage(url):
    req = requests.get(url, headers)
    return BeautifulSoup(req.text, "lxml")

def getLinks():
    urls = []
    soup = getPage(sitemap)
    links = soup.find_all("loc")
    for link in links:
        urls.append(link.getText())
    return urls

def findIcons(urls):
    icons_list = []
    for url in urls:
        soup = getPage(url)
        tags = soup.find_all("i")
        for tag in tags:
            clss = tag.get("class")
            for cls in clss:
                if len(cls) > 2 and cls[:2] == 'bi': 
                    icons_list.append(cls)
        print(f"[+] URL {url} handled")
        time.sleep(to)
    return icons_list

def getIconsBtstrp():
    head_css = []
    with open(f"{abs_path}\\bootstrap\\bootstrap-icons.css", "r") as file:
        css = file.read().splitlines()
    bracket_count = 0
    line_count = 0
    for line in css:
        line_count += 1
        if bracket_count == 2: break
        if line.find('}') != -1: bracket_count += 1
        head_css.append(line)
    return ([item.replace(";", "").replace(" ", "") for item in css[line_count:]], [item + "\n" if item.find("*") != -1 else item.replace(" ", "") for item in head_css])

def findConformity(icons):
    iconsBtstrp = getIconsBtstrp()
    new_css = iconsBtstrp[1]
    for icon in iconsBtstrp[0]:
        for ico in icons:
            if icon.find(ico + "::") != -1:
                print(f"{icon} <---- {ico}")
                new_css.append(icon)
                icons.remove(ico)
    if len(icons) > 0: print("Not found:", *icons, "\n")
    return new_css

def writeCss(new_css):
    with open(f"{abs_path}\\result\\bootstrap-icons.min.css", "w") as f:
        for line in new_css:
            f.write(line)

def main():
    urls = getLinks()
    icons = list(dict.fromkeys(findIcons(urls)))
    writeCss(findConformity(icons))
    print("Complete!")

if __name__ == "__main__":
    main()
