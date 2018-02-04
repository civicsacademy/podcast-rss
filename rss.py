import json
from feedgen.feed import FeedGenerator
from datetime import datetime
import pytz
import os
from mutagen.mp3 import MP3

fg = FeedGenerator()
fg.id('http://civicsacademy.co.za')
fg.title('Civics Academy - South Africa')
fg.author( {'name':'Civics Academy','email':'info@civicsacademy.co.za'} )
fg.link( href='http://www.civicsacademy.co.za/', rel='alternate' )
fg.logo('https://civicsacademy.whatcanido.org.za/logo.png')
fg.subtitle('Cultivating democracy through civic action')
fg.link( href='http://civicsacademy.co.za', rel='self' )
fg.language('en')
fg.description('Aiming to inform and to strengthen democratic values and responsible citizenship. Civics Academy covers educational content related to democracy, governance, elections, political parties, the justice system, the Constitution, economics, civil society, human rights and the environment.')

fg.load_extension('podcast')

cats = [
    {
        "cat": 'Government & Organizations',
        "sub": 'National',
    },
]
fg.podcast.itunes_category(cats)
fg.podcast.itunes_explicit('clean')

with open('podcasts.jsonlines') as podcastfile:
    for jsonline in podcastfile:
        podcast = json.loads(jsonline)
        local_path = '../' + podcast['file']
        size_bytes = os.path.getsize(local_path)
        audio = MP3(local_path)
        uri = 'https://civicsacademy.whatcanido.org.za/' + podcast['file']
        fe = fg.add_entry()
        fe.id(uri)
        u = datetime.utcnow()
        u = u.replace(tzinfo=pytz.utc)
        fe.published(u)
        fe.title(podcast['title'])
        fe.description(podcast['description'])
        fe.enclosure(uri, str(size_bytes), 'audio/mpeg')
        fe.author( {'name':'Civics Academy','email':'info@civicsacademy.co.za'} )
        fe.podcast.itunes_duration(audio.info.length)

fg.rss_str(pretty=True)
fg.rss_file('podcasts.xml')
