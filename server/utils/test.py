import sqlite3 as sql
import newspaper
from newspaper import Article

conn = sql.connect('../data/news/news.db')


c = conn.cursor()


# c.execute('''
#         CREATE TABLE reliable_news(url text, title text, newsbody text)
#     ''')

url = 'http://www.cnn.com/2013/11/27/justice/tucson-arizona-captive-girls/'

article = Article(url)

article.download()
article.parse()

title = article.title
newsbody = article.text
params = (
    url,
    title,
    newsbody
)
# print(newsbody)
newsbody = newsbody.replace('\n\n', '\n')

c.execute('DROP TABLE reliable_news')
# c.execute('INSERT INTO reliable_news VALUES (?,?,?)', params)

# c.execute('SELECT newsbody FROM reliable_news')

# print(c.fetchall())


conn.commit()
conn.close()
