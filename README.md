```
mkdir -p content
rm podcasts.jsonlines
scrapy crawl -t jsonlines -o podcasts.jsonlines podcast
```

```
python rss.py
```

```
aws s3 --profile civicsacademy sync content s3://civicsacademy.whatcanido.org.za
```