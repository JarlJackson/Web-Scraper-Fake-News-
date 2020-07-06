import requests
from bs4 import BeautifulSoup

maxPages = 20
z = 1
pageNum = 1

while z <= maxPages:

    print("Current Page:", pageNum)
    z += 1
    # print("Loop:", z)

    WebLink = "https://www.snopes.com/fact-check/page/{}".format(pageNum)
    CorePage = requests.get(WebLink)  # Core Page Link

    # print("Page Number:", pageNum)
    pageNum += 1

    SoupObj = BeautifulSoup(CorePage.content, "html.parser")  # Soup Object

    ArticleLinks = []

    for link in SoupObj.findAll('a', href=True):
        checkString = link.get("href")
        if "https://www.snopes.com/fact-check/" in checkString:
            ArticleLinks.append(link.get('href'))

    # print("Before Edit", ArticleLinks)

    for link in ArticleLinks:
        if link == "https://www.snopes.com/fact-check/":
            ArticleLinks.remove(link)
            # print("Removed", link)

    ArticleLinksLength = len(ArticleLinks)
    del ArticleLinks[12:ArticleLinksLength]

    print("After Edit", ArticleLinks)

    for link in ArticleLinks:
        CurrentPage = requests.get(link)
        CurrentSoupObj = BeautifulSoup(CurrentPage.content, "html.parser")

        RatingSelection = CurrentSoupObj.find_all("div", class_="rating-wrapper card")
        Rating = ""
        found = False
        for elem in RatingSelection:
            RatingDiv = elem.find_all("div", class_="media-body")
            for x in RatingDiv:
                if not found:
                    Rating = x.find("h5").get_text()
                    found = True

        ClaimSelection = CurrentSoupObj.find_all("div", class_="claim-wrapper card")
        Claim = ""

        for elem in ClaimSelection:
            ClaimDiv = elem.find_all("div", class_="claim")
            for x in ClaimDiv:
                Claim = x.find("p").get_text()

        if Rating == "False" or Rating == "Scam" or Rating == "True":
            file = open("Articles.txt", "a")
            print("Claim:")
            print(Claim)
            print("Rating:")
            print(Rating)
            print("Link:")
            print(link)
            file.write("Claim:" + "\n")
            file.write(Claim + "\n")
            file.write("Rating:" + "\n")
            file.write(Rating + "\n")
            file.write("Link:" + "\n")
            file.write(link + "\n")
            file.write("\n")
            file.close()
