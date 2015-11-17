import requests
import urllib

from bs4 import BeautifulSoup as bs4



ARCHIVE_URL = 'http://xkcd.com/archive'


# GET ARCHIVE
archive_request = requests.get(ARCHIVE_URL)

if archive_request.status_code == 200:
    archive_content = archive_request.content
    bs = bs4(archive_content, "html.parser")

    archive = {}
    
    for data in bs.find_all("div", {"id":"middleContainer"}):
        for alinks in data.find_all("a"):
            comic_num = alinks.get("href").strip("/")
            comic_date = alinks.get("title")
            comic_desc = alinks.contents[0]

            archive[comic_num] = {"date":comic_date,
                                  "desc":comic_desc}





XKCD_API1 = "http://xkcd.com/{comic_num}/info.0.json"

def get_comic_num(i):
    comic_request_url = XKCD_API1.format(comic_num = i)

    comic_request = requests.get(comic_request_url)

    if comic_request.status_code == 200:
        content = comic_request.json()

        num = content['num']
        img = content['img']
        title = content['title']
        date = "{day}-{month}-{year}".format(day=content['day'],
                                             month=content['month'],
                                             year=content['year'])

        urllib.urlretrieve(img,
                           filename="{num}_{title}_{date}".format(num=num,
                                                                  title=title,
                                                                  date=date))


def get_all_comics():
    archive_ints = map(int, archive.keys())

    num_of_comics = max(archive_ints)

    for i in xrange(1, num_of_comics):
        if i != 472:
            print "downloading comic {i}".format(i = i)
            get_comic_num(i)


get_all_comics()        
