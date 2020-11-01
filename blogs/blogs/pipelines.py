# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from .models import Blog, db_connect, create_table


class BlogsPipeline:

    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)



    def store_db(self, item):
        session = self.Session()
        blog = Blog()
        blog.title = item['title']
        blog.intro = item['intro']
        blog.author = item['author']
        blog.date = item['created']

        try:
            session.add(blog)
            session.commit()
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item

    def process_item(self, item, spider):
        self.store_db(item)
        print(item)
        print('************ ITEM ****************')
        print('************ ITEM ****************')
        return item
