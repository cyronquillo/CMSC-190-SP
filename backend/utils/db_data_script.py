import sqlite3 as sql
import newspaper
from newspaper import Article

conn = sql.connect('../data/news/news.db')
c = conn.cursor()

def create_tables():
    c.execute('DROP TABLE reliable_news')
    c.execute('DROP TABLE satirical_news')
    c.execute('''
        CREATE TABLE reliable_news(url text, title text, newsbody text)
    ''')

    c.execute('''
        CREATE TABLE satirical_news(url text, title text, newsbody text)
    ''')

    conn.commit()

def insert_to_table(table, params):
    c.execute('INSERT INTO ' + table +' VALUES (?,?,?)',
              params)
    
    conn.commit()

def crawl():
    print("Satirical Sites:")
    for site in satiric_sites:
        print(site)
        url = http + site
        paper = newspaper.build(url, memoize_articles=False)
        article_count = 0
        for article in paper.articles:
            article_count += 1
            print('storing article', article_count)
            article_url = article.url
            article = Article(article_url)
            try:
                article.download()
                article.parse()
            except:
                continue
            title =  article.title
            newsbody = article.text.replace('\n\n', '\n')
            params = (
                url,
                title,
                newsbody
            )

            insert_to_table('satirical_news', params)

    print("Reliable Sites:")
    for site in reliable_sites:
        print(site)
        url = http + site
        paper = newspaper.build(url, memoize_articles=False)
        article_count = 0
        for article in paper.articles:
            article_count += 1
            print('storing article', article_count)
            article_url = article.url
            article = Article(article_url)
            try:
                article.download()
                article.parse()
            except:
                continue
            title = article.title
            newsbody = article.text.replace('\n\n', '\n')
            params = (
                url,
                title,
                newsbody
            )

            insert_to_table('reliable_news', params)

http = "http://"
reliable_sites = [
    'www.cnnphilippines.com',
    'newsinfo.inquirer.net',
    'www.philstar.com',
    'news.abs-cbn.com',
    'mb.com.ph'
]


#https://en.wikipedia.org/wiki/List_of_fake_news_websites
satiric_sites = [
    'adobochronicles.com',
    'filipinofreethinkers.org',
    'dutertenews.com',
    'agilanews.wordpress.com',
    'pinoytrending.altervista.org',
    'dutertetrendingnews.blogspot.com',
    'www.dutertedefender.com',
    'www.maharlikanews.com',
    'mindanation.com',
    'globalnews.favradio.fm',
    'pinoynewsblogger.blogspot.com'

]

crawl()
conn.close()

