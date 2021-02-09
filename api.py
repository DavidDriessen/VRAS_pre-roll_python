from PyInquirer import style_from_dict, Token, prompt
import youtube_dl
import requests
import shutil
import json
import re
import os


def match_session(title):
    community_event = re.compile("^.* \\[.*]$")  # Match community_event
    seasonal = re.compile("^.*#[0-9] \\[.*]$")  # Match seasonal
    individual = re.compile("^(.*) E[P|p]? ?[0-9]+(-[0-9]+)?$")  # Match individual
    if seasonal.match(title):
        return title
    if community_event.match(title):
        return None
    if individual.match(title):
        return individual.match(title).group(1)
    else:
        print("Couldn't parse session title: '" + title + "'")


def parse_sessions(sessions):
    s = set()
    for session in sessions:
        session['title'] = match_session(session['title'])
        if session['title'] and session['title'] not in s:
            s.add(session['title'])
            yield Session(session)


def get_sessions():
    return list(parse_sessions(requests.get("https://www.vranimesociety.com/events",
                                            headers={'X-Requested-With': 'XMLHttpRequest',
                                                     'Accept': 'application/json'}).json()))


def search_series(series):
    url = "https://anilist-graphql.p.rapidapi.com/"
    payload = {"query": """query ($search: String) {
                   Media(search: $search, type: ANIME){
                   title { english romaji }
                   trailer { id site thumbnail }
                   coverImage { extraLarge large medium color }
                   bannerImage
                   }}""",
               "variables": {"search": series}}
    headers = {
        'content-type': "application/json",
        'x-rapidapi-key': "7312ba6a87mshd90faca3bd5b364p160c8bjsn42e2ef6a0aa4",
        'x-rapidapi-host': "anilist-graphql.p.rapidapi.com"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    data = response.json()['data']
    return data['Media']


class Series:
    def __init__(self, name):
        media = search_series(name)
        while not media:
            name = prompt([{
                'type': 'input',
                'name': 'series',
                'message': 'What is the correct name of the series?',
                'default': name
            }], style=style)['series']
            media = search_series(name)
        self.name = media["title"]["english"]
        self.poster = media["coverImage"]["extraLarge"]
        self.trailer = media["trailer"]

    def __repr__(self):
        return "Series(" + self.name + ")"

    def get_poster(self):
        file = "Posters/" + self.poster.split('/')[-1]
        if not os.path.isfile(file):
            r = requests.get(self.poster, stream=True)
            if r.status_code == 200:
                r.raw.decode_content = True
                with open(file, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            else:
                print("Image Couldn't be retrieved: '" + self.poster + "'")
        return file

    def get_trailer(self):
        if self.trailer and self.trailer["site"] == 'youtube':
            with youtube_dl.YoutubeDL({'outtmpl': 'Trailers/%(title)s.%(ext)s'}) as ydl:
                trailer_url = "https://www.youtube.com/watch?v=" + self.trailer["id"]
                info_dict = ydl.extract_info(trailer_url, download=False)
                file = ydl.prepare_filename(info_dict)
                if not os.path.isfile(file):
                    ydl.download([trailer_url])
                return file


class Session:
    def __init__(self, session):
        regex_series = re.compile("(?:[*][*])?(.*) E[0-9]+(?:-[0-9]+)?(?:[*][*])?")  # from description
        self.name = session['title']
        self.series = list(map(lambda s: Series(s), regex_series.findall(session['description'])))

    def __repr__(self):
        return "Session(" + self.name + ", " + str(self.series) + ")"


if __name__ == "__main__":
    style = style_from_dict({
        Token.QuestionMark: '#E91E63 bold',
        Token.Selected: '#673AB7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#2196f3 bold',
        Token.Question: '',
    })

    sessions = get_sessions()
    result = prompt([{
        'type': 'checkbox',
        'name': 'sessions',
        'message': 'What session(s) do you want to render?',
        'choices': list(map(lambda s: {'name': s.name, 'value': s}, sessions))
    }], style=style)
    print(result)
