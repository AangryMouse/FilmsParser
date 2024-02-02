import scrapy
import csv
import re

class WikiSpider(scrapy.Spider):
    name = "wiki"
    allowed_domains = ["ru.wikipedia.org"]
    start_urls = ["https://ru.wikipedia.org/w/index.php?title=Категория:Фильмы_по_алфавиту&pageuntil=65+%28фильм%29#mw-pages"]

    def __init__(self):
        csvfile = open('movies.csv', 'w', newline='')
        fieldnames = ['title', 'genres', 'directors', 'countries', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        self.writer = writer

    def parse(self, response):
        for film_link in response.css('div.mw-category-columns li a::attr(href)').getall():
            yield response.follow(film_link, callback=self.parse_films)
        if response.css('#mw-pages > a::text').getall()[-1] == 'Следующая страница':
            yield response.follow(response.css('#mw-pages > a::attr(href)').getall()[-1], callback=self.parse)

    def parse_films(self, response):
        title = response.css('th.infobox-above ::text').get()
        genres = []
        directed_by = []
        countries = []
        year = []
        for row in response.css('table.infobox tr'):
            if row.css('span::attr(data-wikidata-property-id)').get() == 'P136'\
                    or re.fullmatch(r'[Жж]анр[ы]?', str(row.css('th::text').get())):
                genres.extend(row.css('span a::text').getall())
                genres.extend(row.css('span::text').getall())
            if row.css('span::attr(data-wikidata-property-id)').get() == 'P57'\
                    or re.fullmatch(r'[Рр]ежисс[ёе]р[ы]?', str(row.css('th::text').get())):
                directed_by.extend(row.css('span a::text').getall())
                directed_by.extend(row.css('span::text').getall())
            if row.css('span::attr(data-wikidata-property-id)').get() == 'P495'\
                    or re.fullmatch(r'[Сс]тран[аы]', str(row.css('th::text').get())):
                countries.extend(row.css('span::attr(data-sort-value)').getall())
                countries.extend(row.css('span.country-name a::text').getall())
            if row.css('span::attr(data-wikidata-property-id)').get() == 'P577'\
                    or row.css('th::text').get() == "Год":
                year.extend(row.css('span::text').getall())
                year.extend(row.css('span a::text').getall())


        self.writer.writerow({
                    'title': title,
                    'genres': genres,
                    'directors': directed_by,
                    'countries': countries,
                    'year': year
                })







