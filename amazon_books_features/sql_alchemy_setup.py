from sqlalchemy import Column, Integer, String, create_engine, Text, Float, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Define the table to store book data
class AmazonBooksData(Base):
    __tablename__ = 'amazon_books'

    id = Column(Integer, primary_key=True)  # Primary key
    name = Column(String(255))  # Book name
    summary = Column(Text)  # Book summary
    category = Column(String(255))  # Book category
    book_type = Column(String(100))  # Type (e.g., hardcover, paperback)
    production_date = Column(String(100))  # Production/publish date
    authors = Column(String(255))  # Authors
    hard_cover_price = Column(String(50))  # Hard cover price
    paper_back_price = Column(String(50))  # Paperback price
    book_rating = Column(Float)  # Book rating
    total_user_ratings = Column(String(50))  # Total user ratings
    number_of_pages = Column(Integer)  # Number of pages
    language = Column(String(100))  # Language
    reviews = Column(Text)  # Reviews (text field to hold multiple reviews)

    __table_args__ = (
        UniqueConstraint('name', 'authors', name='unique_book_author_constraint'),
    )

# Format: 'dialect+driver://username:password@host:port/database'
engine = create_engine('mysql+pymysql://root:Jalingo2003#@127.0.0.1:3306/amazon_books', echo=True)

# Create the table in the database (if not already created)
Base.metadata.create_all(engine)

# Create a session for adding and committing data
Session = sessionmaker(bind=engine)





