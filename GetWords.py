# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from tat2url import tat2url
import urllib2, re, codecs

"""
Функция получает список слов по ссылке, потом формирует url перевода слова
и парсит данные по переводу слова.
Готовые данные пишутся в БД.
"""
def getWords(url, cursor = None):
    if not cursor:
        return 0

    #output = codecs.open('./words/' + re.search('.{2}$', url).group(0) + '.txt', 'w', 'utf-8')

    url = urllib2.urlopen(url)

    html = url.read()

    soup = BeautifulSoup(html)

    """
    Находим div со списком слов и по url получаем страницу с переводом слова.
    """
    result = soup.find('div', {'class' : 'words_list'})

    for a in list(result.findAll('a')):
        word = re.search('(?<=-\s).*$', a['title'].encode('utf-8')).group(0)
        """
        Получаем страницу с переводом слова
        """
        url = urllib2.urlopen('http://tatpoisk.net/dict/tat2rus/' + urllib2.quote(word))

        html = url.read()

        soup = BeautifulSoup(html)

        """
        Собственно вытаскиваем сам перевод слова из "мусора"
        """
        try:
            result = soup.find('p', {'class': 'search_results'}).contents[-1]
            cursor.execute("INSERT INTO t_dictionary (t_word, translate) VALUES ('%s', '%s')" % (word, result.encode('utf-8')))
        except:
            print word