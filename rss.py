import json
from feedgen.feed import FeedGenerator


fg = FeedGenerator()
fg.id('http://civicsacademy.co.za')
fg.title('Civics Academy - South Africa')
fg.author( {'name':'Civics Academy','email':'info@civicsacademy.co.za'} )
fg.link( href='http://www.civicsacademy.co.za/', rel='alternate' )
fg.logo('http://civicsacademy.github.io/logo.png')
fg.subtitle('Cultivating democracy through civic action')
fg.link( href='http://civicsacademy.co.za', rel='self' )
fg.language('en')

fg.load_extension('podcast')

cats = [
    {
        "cat": 'Government & Organizations',
        "sub": 'National',
    },
    {
        "cat": 'News & Politics',
    },
    {
        "cat": 'Government & Organizations',
        "sub": 'Local',
    },
]
fg.podcast.itunes_category(cats)
fg.podcast.itunes_explicit('clean')

with open('podcasts.jsonlines') as podcastfile:
    for jsonline in podcastfile:
        podcast = json.loads(jsonline)
        uri = 'http://civicsacademy.github.io/' + podcast['file']
        fe = fg.add_entry()
        fe.id(uri)
        fe.title(podcast['title'])
        fe.description(podcast['description'])
        fe.enclosure(uri, 0, 'audio/mpeg')

fg.rss_str(pretty=True)
fg.rss_file('podcasts.xml')
