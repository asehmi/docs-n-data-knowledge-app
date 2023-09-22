from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

# --------------------------------------------------------------------------------

# TODO: Make this HttpException compatible
# https://stackoverflow.com/questions/64501193/fastapi-how-to-use-httpexception-in-responses
# https://plainenglish.io/blog/3-ways-to-handle-errors-in-fastapi-that-you-need-to-know-e1199e833039
# https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-5-basic-error-handling/

# Error handler
class AppError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def throw_if_nulls(df):
    if sum(df.isnull().values.ravel()) > 0:
        raise AppError(
            error = f'NULL values found in dataframe ({list(df.columns)})!!',
            status_code = 500
        )

# --------------------------------------------------------------------------------

colorama_init()

def print_red(msg):
    print(f'{Fore.RED}{msg}{Style.RESET_ALL}')
def print_blue(msg):
    print(f'{Fore.BLUE}{msg}{Style.RESET_ALL}')
def print_green(msg):
    print(f'{Fore.GREEN}{msg}{Style.RESET_ALL}')
def print_yellow(msg):
    print(f'{Fore.YELLOW}{msg}{Style.RESET_ALL}')
def print_cyan(msg):
    print(f'{Fore.CYAN}{msg}{Style.RESET_ALL}')
def print_magenta(msg):
    print(f'{Fore.MAGENTA}{msg}{Style.RESET_ALL}')

# WEB SCRAPER -----------------------------------------------------------------

# https://newspaper.readthedocs.io/en/latest/user_guide/quickstart.html
import newspaper
# https://www.crummy.com/software/BeautifulSoup/
from bs4 import BeautifulSoup
import htmldate
import dateutil
import datefinder
import random
import time

def scrape_articles(source_urls):
    article_titles = []
    article_authors = []
    article_dates = []
    article_texts = []
    article_keywords = []
    article_summaries = []
    article_urls = []

    articles_dict = \
        {'title':article_titles, 'author':article_authors, 'date':article_dates, \
          'text':article_texts, 'keywords':article_keywords, 'summary':article_summaries, \
          'url':article_urls }

    def _newspaper_scraper_helper(url):
        HEADERS = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Referer' : 'https://google.com/' }
        config = newspaper.Config()
        config.headers = HEADERS
        config.request_timeout = 10

        article = newspaper.Article(url=url, language='en')
        article.download()
        article.parse()
        article.nlp()

        article_titles.append(article.title)
        article_authors.append(article.authors)

        if article.publish_date == None:
            publish_date = alternative_get_publish_date(article)
        else:
            publish_date = parse_date_str(str(article.publish_date))
        article_dates.append(publish_date)
        
        if publish_date:
            article_text = f'Published: {publish_date.strftime("%d %B %Y")}\n\n{article.text}'
        else:
            article_text = article.text
        article_text = article_text.replace('\n\n','\n').replace('\r\n','\n')
        article_texts.append(article_text)
        
        article_keywords.append(article.keywords)
        article_summaries.append(article.summary)
        article_urls.append(article.url)

        # print(f'{article.title}\n{article.authors}\n{article.publish_date}\n{article_text[:20]}\n\
        #     {article.keywords}\n{article.summary}\n{article.url}')

        articles_dict = \
            {'title':article_titles, 'author':article_authors, 'date':article_dates, \
             'text':article_texts, 'keywords':article_keywords, 'summary':article_summaries, \
             'url':article_urls }
            
        # NOTE: Could use this dict object to return a Pandas dataframe instead!
        
        return articles_dict

    # for testing
    '''
    count = 0
    '''
    for url in source_urls:

        # for testing (can bail out early)
        '''count+=1
        if count > 5:
            break
        '''
        # Use a variable sleep betwen calls (good netizenship!)
        t = random.choice([0.1, 0.25, 0.5, 0.75, 1., 1.1, 1.25, 1.5])
        jitter = random.random()
        T = t + jitter
        time.sleep(T)

        try:
            _newspaper_scraper_helper(url)
        except Exception as e:
            print('!!Newspaper Exception!!', '\n', e)
            continue

    return articles_dict

# if newspaper can't find, then use bs4, datafinder, htmldate
def alternative_get_publish_date(article):
    # try bs4
    soup = BeautifulSoup(article.html, features="lxml")
    # class=newsdate is specific to one site I was scraping (you can change this to suit your needs)
    para = soup.find('p', attrs={'class': 'newsdate'})
    if para:
        datetime_obj = parse_date_str(para.next)
        return datetime_obj

    # try datefinder
    try:
        datefndrdt = datefinder.find_dates(article.text)
        datetime_obj = datefndrdt.__next__()
        return datetime_obj
    except:
        pass

    # try htmldate
    htmldt = htmldate.find_date(article.html, extensive_search=True, original_date=True)
    if htmldt:
        datetime_obj = parse_date_str(htmldt)
        return datetime_obj

    return None

def parse_date_str(date_str):
    if date_str:
        try:
            return dateutil.parser.parse(date_str)
        except (ValueError, OverflowError, AttributeError, TypeError):
            # nearly all parse failures are due to URL dates without a day
            # specifier, e.g. /2014/04/
            return None

# --------------------------------------------------------------------------------
# After a lot of investigation on partial formatting, I found this solution:
# https://stackoverflow.com/a/34033230
#
# NOTE: (@asehmi) It has been modified to preserve the format strings if fp's
# value is None, which is important when a prompt template is being
# incrementally built up (e.g. say templates are generated from parts 
# and they use parameter subsitutions taken from a database, and
# then they're used to build the final prompt by binding with
# the doc input, etc.) There is also a mod to deal with embedded
# JSON strings which contain braces.
#
import string
class SafeFormatter(string.Formatter):
    def vformat(self, format_string, args, kwargs):
        args_len = len(args)  # for checking IndexError
        tokens = []
        for (lit, name, spec, conv) in self.parse(format_string):
            # re-escape braces that parse() unescaped
            # NOTE: (@asehmi) Modified to deal with embedded JSON strings which contain braces
            if lit[0] in ['{','}'] or lit[-1] in ['{','}']:
                lit = lit.replace('{', '{{{{').replace('}', '}}}}')
            else:
                lit = lit.replace('{', '{{').replace('}', '}}')
            # only lit is non-None at the end of the string
            if name is None:
                tokens.append(lit)
            else:
                # but conv and spec are None if unused
                conv = '!' + conv if conv else ''
                spec = ':' + spec if spec else ''
                # name includes indexing ([blah]) and attributes (.blah)
                # so get just the first part
                fp = name.split('[')[0].split('.')[0]
                # treat as normal if fp is empty (an implicit
                # positional arg), a digit (an explicit positional
                # arg) or if it is in kwargs
                # NOTE: (@asehmi) Modified to preserve the format if fp's value is None
                if (not fp or fp.isdigit() or fp in kwargs) and kwargs[fp] is not None:
                    tokens.extend([lit, '{', name, conv, spec, '}'])
                # otherwise escape the braces
                else:
                    tokens.extend([lit, '{{', name, conv, spec, '}}'])
        format_string = ''.join(tokens)  # put the string back together
        # finally call the default formatter
        return string.Formatter.vformat(self, format_string, args, kwargs)