# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup
import urllib2, re, psycopg2, time
from GetWords import getWords

startedTime = time.time()

"""
Вытаскиваем ссылки на слова каждой буквы алфавита
"""
url = urllib2.urlopen('http://tatpoisk.net/dict/tat2rus/list')

html = url.read()

soup = BeautifulSoup(html)

aList = soup.findAll('a', href = re.compile('/dict/tat2rus/list/.+'))

host = "host='192.168.100.6' dbname='julia' user='admin' password='218855'"

conn = psycopg2.connect(host)
cursor = conn.cursor()

linksList = []
"""
Получаем список букв(для дальнейшего формирования url)
"""
for a in aList:
    linksList.append(re.search(r'(?<=href=").*(?=">)', str(a)).group(0))

for url in linksList:
    """
    Формируем url
    """
    url = 'http://tatpoisk.net/%s' % (url)
    getWords(url, cursor)
    #break

cursor.execute('COMMIT')
cursor.close()
conn.close()

print time.time() - startedTime