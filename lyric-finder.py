import requests
from bs4 import BeautifulSoup
import re

LYRIC_WEBSITE = "https://www.lyricsmania.com"
LYRIC_WEBSITE_SEARCH = "https://www.lyricsmania.com/search.php?"

def prettify_selection(selection):
    return selection.replace("/", "").replace(".html", "").replace("_", " ").title()

def search_songs(song_name):
    params = {"k": song_name, "x": "0", "y": "0"}

    # Gets the list of songs from the lyric website
    res = requests.get(LYRIC_WEBSITE_SEARCH, params=params)
    soup = BeautifulSoup(res.text, "html.parser")

    # Find the links of the songs
    ul = soup.find("ul", attrs={"class": "search"})
    lis = ul.find_all("li")
    as_ = [li.find("a") for li in lis]

    #Makes a selection
    selections = [{"url": a.attrs["href"], "prettified": prettify_selection(a.attrs["href"])} for a in as_]
    #Removes unnecessary links not correlating to the song
    for selection in selections:
        if re.findall(r"/search/", selection["url"]):
            del selection
    
    if selections:
    #Presents to the user | Asks for which song to choose
        for index, selection in enumerate(selections):
            print("{}) {}".format(index+1, selection["prettified"]))

        print("")

        try:
            index_chosen = int(input("Choose: "))
            song_chosen = selections[index_chosen-1]
        except:
            print("\nSomething went wrong!")
            return None

        # returns: dict {"url", "prettified"}
        return song_chosen

    print("No songs found!")
    return None

def find_lyrics(song):
    # Goes to the actual song
    song_url = LYRIC_WEBSITE + song
    res_song = requests.get(song_url)

    soup_song = BeautifulSoup(res_song.text, "html.parser")
    song_body = soup_song.find("div", attrs={"class": "lyrics-body"})

    # Gets the content
    lyrics = song_body.text

    # returns: str
    return lyrics


if __name__ == "__main__":
    print("")
    print("Lyric Finder - Luan")
    print("")
    song_chosen = input("Song: ")
    print("")
    data = search_songs(song_chosen)
    if data:
        print("")
        print("Searching...")
        print(find_lyrics(data["url"]))

