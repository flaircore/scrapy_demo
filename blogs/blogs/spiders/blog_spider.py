import scrapy

class BlogSpider(scrapy.Spider):
    name = "blogs"
    start_urls = [
        "https://www.flaircore.com/blog"
    ]

    @staticmethod
    def blog_body(item):
        body = ""
        for paragraph in item:
            body += paragraph
        return body


    def parse(self, response, **kwargs):
        for blog in response.css('div.views-row'):
            yield {
                'title': blog.css('.node header .node__title a span::text').get(),
                'intro': self.blog_body(blog.css('.field--name-body *::text').getall()),
                'author': blog.css('.field--name-uid span::text').get(),
                'created': blog.css('.field--name-created::text').get()
            }