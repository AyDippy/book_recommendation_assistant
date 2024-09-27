# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from amazon_books_features.sql_alchemy_setup import AmazonBooksData, Session
from sqlalchemy.exc import IntegrityError

class MySQLStorePipeline:
    def process_item(self, item, spider):
        # Open a session
        session_instance = Session()
        try:
            # Check if the book with the same name and authors already exists in the database
            existing_book = session_instance.query(AmazonBooksData).filter_by(
                name=item.get('BookName'),
                authors=item.get('Authors')
            ).first()

            # If the book doesn't exist, create a new row
            if not existing_book:
                book_data = AmazonBooksData(
                    name=item.get('BookName'),
                    summary=item.get('Summary'),
                    category=item.get('Category'),
                    book_type=item.get('BookType'),
                    production_date=item.get('ProductionDate'),
                    authors=item.get('Authors'),
                    hard_cover_price=item.get('HardCoverPrice'),
                    paper_back_price=item.get('PaperBackPrice'),
                    book_rating=float(item.get('BookRating') or 0),  # Handle missing ratings
                    total_user_ratings=item.get('TotalUserRatings'),
                    number_of_pages=int(item.get('NumberOfPages') or 0),  # Handle missing page numbers
                    language=item.get('Language'),
                    reviews=', '.join(item.get('Reviews'))  # Join reviews into a single string
                )
                # Add the data to the session
                session_instance.add(book_data)
                # Commit the transaction
                session_instance.commit()

            else:
                spider.logger.info(f"Duplicate item found: {item.get('BookName')} by {item.get('Authors')}. Skipping.")

        except IntegrityError as e:
            # Handle unique constraint violation
            session_instance.rollback()
            spider.logger.error(f"Integrity error: {e}")
        except Exception as e:
            # Rollback in case of an error
            session_instance.rollback()
            spider.logger.error(f"Error storing item: {e}")
        finally:
            # Close the session
            session_instance.close()

        return item
