from typing import Iterable
import scrapy
from scrapy import Request
from urllib.parse import urlencode, urljoin



API_KEY = '3d84a0fc-d307-402f-82ea-46d8eeb94976'

def get_proxy_url(url):
    payload = {'api_key': API_KEY, 'url': url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class AmazonBooksSpider(scrapy.Spider):
    name = "amazon_books"
    allowed_domains = ["www.amazon.com", "proxy.scrapeops.io"]

    def start_requests(self):
        base_url = f"https://www.amazon.com/s?"
        # Parameters that will remain constant
        common_params = {
            'k': 'books amazon',
            'page': '1',
            'i': 'stripbooks',
            'rh': 'n:283155,p_76:1250218011,p_n_feature_browse-bin:2656020011',
            'dc': '',
            'crid': 'BHW29Z8MHECZ',
            'sprefix': 'books amazon,aps,1300'
        }

        # List of changing parameters
        category_parameters = ['1', '2', '3', '4', '4366', '5', '6', '173507', '10', '9', '86', '10777', '17', '173514', '18', '22', '23', '75', '25', '28', '27']

        # Iterate through each changing parameter
        for category in category_parameters:
            # Update the parameter
            params = common_params.copy()
            params['rh'] = f'n:283155,n:{category},p_76:1250218011,p_n_feature_browse-bin:2656020011'

            # Construct the URL
            query_string = urlencode(params, doseq=True)
            amazon_search_url = f"{base_url}{query_string}"

            yield scrapy.Request(url=amazon_search_url, callback=self.discover_books_url, meta={'page':1, 'category': category})

            # Now request additional pages for this category (from page 2 to last page, e.g., 10)
            for i in range(2, 11):  # Assuming scraping up to 10 pages
                amazon_search_url = f"{base_url}{query_string}&page={i}"
                yield scrapy.Request(url=amazon_search_url, callback=self.discover_books_url,
                                     meta={'page': i, 'category': category})

    def discover_books_url(self, response):
        page = response.meta['page']
        category = response.meta['category']
        search_books = response.css('div.a-section.a-spacing-none.puis-padding-right-small.s-title-instructions-style')
        for book in search_books:
            book_links = book.css('h2>a::attr(href)').get()
            baseUrl = "https://amazon.com"
            book_url = urljoin(baseUrl, book_links)
            yield scrapy.Request(url =get_proxy_url(book_url), callback=self.parse, meta={'page': page, 'category': category})
        #Scrapping 10 pages per book category
        # if page == 1:
        #     for i in range(2,10):
        #         params = {
        #             'k': 'books amazon',
        #             'page': str(i),
        #             'i': 'stripbooks',
        #             'rh': 'n:283155,p_76:1250218011,p_n_feature_browse-bin:2656020011',
        #             'dc': '',
        #             'crid': 'BHW29Z8MHECZ',
        #             'sprefix': 'books amazon,aps,1300'
        #         }
        #         new_params = params.copy()
        #         new_params['rh'] = f'n:283155,n:{category},p_76:1250218011,p_n_feature_browse-bin:2656020011'
        #
        #         # Construct the URL
        #         query_string = urlencode(new_params, doseq=True)
        #         amazon_search_url = f"https://www.amazon.com/s?{query_string}"
        #         yield scrapy.Request(url=amazon_search_url, callback=self.discover_books_url, meta={'page':i, 'category': category})

    def parse(self, response):
        # Extract the book information using the correct methods
        name = response.css('div.a-section.a-spacing-none span.a-size-large.celwidget::text').get().strip()
        book_type = response.css('div.a-section.a-spacing-none span.a-size-medium.a-color-secondary.celwidget::text').get().split('–')[0].strip()
        production_date = response.css('div.a-section.a-spacing-none span.a-size-medium.a-color-secondary.celwidget::text').get().split('–')[1].split(',')
        if len(production_date) > 2:
            date = response.css('div.a-section.a-spacing-none span.a-size-medium.a-color-secondary.celwidget::text').get().split('\u2013')[1].split(',')
            production_date = ', '.join([date[1],date[2]]).strip()
        else:
            production_date = response.css('div.a-section.a-spacing-none span.a-size-medium.a-color-secondary.celwidget::text').get().split('–')[1].strip()


        if len(response.css('span.author.notFaded a.a-link-normal::text').getall()) > 1:
            authors = ', '.join(response.css('span.author.notFaded a.a-link-normal::text').getall())
        else:
            authors = response.css('span.author.notFaded a.a-link-normal::text').getall()[0]

        hard_cover_price = response.css('span.slot-price span.a-size-base.a-color-price.a-color-price::text').get().strip()
        paper_back_price = response.xpath('//span[@aria-label and contains(@class, "a-size-base") and contains(@class, "a-color-secondary")]/@aria-label').get()
        book_rating = response.css('span.a-declarative span.a-size-base.a-color-base::text').get()
        total_ratings = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get()

        # Check if the total_ratings element was found
        if total_ratings:
            total_ratings = total_ratings.split(' ')[0]
        else:
            total_ratings = '0'  # Default value if the rating is not found

        no_of_pages = response.xpath('//div[@class="a-section a-spacing-none a-text-center rpi-attribute-value"]/span/text()').getall()[0].split(' ')[0]
        language = response.xpath('//div[@class="a-section a-spacing-none a-text-center rpi-attribute-value"]/span/text()').getall()[1]
        reviews =  response.css('div.a-expander-content.reviewText.review-text-content.a-expander-partial-collapse-content span::text').getall()
        category = response.css('ul.a-unordered-list.a-horizontal.a-size-small span.a-list-item a.a-link-normal.a-color-tertiary::text').getall()[1].strip()
        summary = response.css('div.a-expander-collapsed-height.a-row.a-expander-container.a-spacing-base.a-expander-partial-collapse-container span.a-text-bold::text').get()


        # Yield the book information
        yield {
            'BookName': name,
            'Summary': summary,
            'Category': category,
            'BookType': book_type,
            'ProductionDate': production_date,
            'Authors': authors,
            'HardCoverPrice': hard_cover_price,
            'PaperBackPrice': paper_back_price,
            'BookRating': book_rating,
            'TotalUserRatings': total_ratings,
            'NumberOfPages': no_of_pages,
            'Language': language,
            'Reviews': reviews
        }
