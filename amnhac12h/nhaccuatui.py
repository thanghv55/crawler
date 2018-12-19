__author__ = 'Hoangthang'

import urllib2, urllib
from os import system
import traceback

number_of_result = 20
def get_size(link):
    try:
        resp = urllib.urlopen(link)
        return int(resp.headers.get("Content-Length"))
    except:
        #traceback.print_exc()
        return 0


def download(link, filename=""):
    if filename == "":
        filename = link.split("/")[-1]
    print get_size(link)
    print "Downloading..."
    try:
        urllib.urlretrieve(link, filename)
    except:
        print "404: Couldn't download file"
    print "Done!"


def download_using_wget(link):  # Use instead if you have wget
    system('wget -c "{}"'.format(link))


def run():
    #link = "https://www.nhaccuatui.com/bai-hat/nguoi-thuong-hoang-ton.dMteKQoTU4mw.html"
    link = "https://aredir.nixcdn.com/NhacCuaTui967/NguoiThuong-HoangTon-5582141.mp3?st=1FcLsV57gxuD4sX6V7R-1w&e=1538066611&download=true"
    print "Download nhaccuatui"
    download(link, filename="test.mp3")
    print "\nThank you for using this program !\n"

run()