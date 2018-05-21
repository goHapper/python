import re
import pymysql
import requests
import json
from lxml import etree
from pyquery import PyQuery
from urllib.parse import urlencode

from bs4 import BeautifulSoup

#数据库链接
conn = pymysql.connect(host='127.0.0.1', user='root',
                       passwd='root', db='lianxi', charset='utf8')
cur = conn.cursor()

def get_user_page(web_url):
    url='https://movie.douban.com/people/'+web_url+'/collect'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except Exception:
        print('访问页面' + url + '出错！')
        return None
def parse_user_movie(html):#通过这个函数对循环进行控制
    movie = json.loads(html)
    result = []
    if movie and 'subjects' in movie.keys():
        for item in movie.get('subjects'):#把单个电影名和地址存入film
            film = {
                'title': item.get('title'),
                'url': item.get('url')
            }
            result.append(film)#所有电影和地址放入result
    return result
def get_one_page(start_no,u_url):
    data = {
        'start': start_no,
        'limit': 20,
        'sort': 'new_score',
        'status': 'P',
        'percent_type': ''
    }
    url = str(u_url)+'comments?' + urlencode(data)

    try:
        response = requests.get(url)
        if response.status_code == 200:
            # print(response.text)
            return response.text
    except Exception:
        print('访问页面' + url + '出错！')
        return None
def parse_user_movie1(html,name):
    doc =PyQuery(html)
    result=[]
    items=list(doc('div.item').items())
    length=len(items)
    soup = BeautifulSoup(html, 'lxml')
    num = 0
    linklist=[]
    for x in soup.find_all('span', attrs={'class': re.compile('^rating*')}):
        link1 = x.get('class')
        if link1:
            linklist.append(link1)
    for item in items:

        grid_movie = {

            'comment_user': name,
            'movie': item.find('div.info').find('ul').find('li.title').find('a').text(),
            'intro': item.find('div.info').find('ul').find('li.intro').text(),
            'date': item.find('div.info').find('ul').find('li').find('span.date').text(),
            'star': linklist[num]
        }
        num+=1
        result.append(grid_movie)
    return result
def parse_one_page(html):
    doc = PyQuery(html)
    title = doc.find('#content > h1:nth-child(1)').text()
    # print(title[:-2])
    items = list(doc('div.comment').items())
    length = len(items)
    # print(length)

    linklist = []
    soup=BeautifulSoup(html,'lxml')
    num=0
    for x in soup.find_all('a',attrs={'href':re.compile('^https://www.douban.com/people/*'),'class':''}):
        link = x.get('href')
        link1=link.split('/')[4]
        num+=1
        if link1 and num%2==0:
            linklist.append(link1)
    if length != 0:
        j = 1

        for item in items:
            commnet = {
                'id':linklist[j-1],
                'movie': title,
                'comment user': item.find('span.comment-info').find('a').text(),#PyQuery的特点，可以连续使用find
                'comment': item.find('p').text(),
                'vote': item.find('span.votes').text(),
                'comment time': item.find('span.comment-time').text()
            }
            print(commnet)





            sql_insert = """INSERT INTO doubanyingping VALUES("%d","%s","%s","%s")""" % \
                         (j,str(title)
                          ,str(pymysql.escape_string(commnet.get('comment'))),
                          str(pymysql.escape_string(commnet.get('comment user'))))
            try:
             cur.execute(sql_insert)
             j+=1
            except pymysql.err.InternalError:
                continue
            conn.commit()

                #                  用户看过电影的主页并转换成为text
            a=get_user_page(commnet.get('id'))
            aa=parse_user_movie1(a,commnet.get('comment user'))
            for item1 in aa:
                    print(item1)

                    sql_insert1 = """INSERT INTO douban_user VALUES("%s","%s","%s","%s","%s")""" % \
                             (str(commnet.get('comment user'))
                              , str(item1.get('movie'))
                              , str(item1.get('intro'))
                              , str(item1.get('date')), str(item1.get('star')[0])
                              )
                    try:
                       cur.execute(sql_insert1)
                    except pymysql.err.InternalError:
                       continue
                    conn.commit()

        return True
    else:
        print('已没有短评了！')
        return False



def get_movie_page(start_number):
    # 来自于网站网址
    data = {

        'type': 'movie',
        'tag': '热门',
        'sort': 'recommend',
        'page_limit': 20,
        'page_start': start_number
    }

    url = 'https://movie.douban.com//j/search_subjects?' + urlencode(data,'utf-8')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except Exception:
        print('请求出错！')
        return None

def get_html(web_url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.108 Safari/537.36 2345Explorer/8.5.1.15355"}
    html = requests.get(url=web_url, headers=header).text #打印源代码
    Soup = BeautifulSoup(html,'html.parser')#转换成为可操作对象
    data = str(Soup.find())
    return data

def parse_index_movie(html):#通过这个函数对循环进行控制
    movie = json.loads(html)
    result = []
    if movie and 'subjects' in movie.keys():
        for item in movie.get('subjects'):#把单个电影名和地址存入film
            film = {
                'title': item.get('title'),
                'url': item.get('url')
            }
            result.append(film)#所有电影和地址放入result
    return result


def get_info(all_movie):
    def str_strip(s):
        return s.strip()

    def re_parse(key, regex):
        ret = re.search(regex, all_movie)
        movie[key] = str_strip(ret[1]) if ret else ''
    #电影相关信息
    movie ={}
    html = etree.HTML(all_movie)
    info = html.xpath("//div[@id='info']")[0]
    movie['director'] = info.xpath("./span[1]/span[2]/a/text()")[0]
    try:
        movie['screenwriter'] = info.xpath("./span[2]/span[2]/a/text()")[0]
    except Exception:
        movie['screenwriter']=''
    try:
        movie['actors'] = '/'.join(info.xpath("./span[3]/span[2]/a/text()"))
    except:
        movie['actors']=''
    movie['type'] = '/'.join(info.xpath("./span[@property='v:genre']/text()"))
    re_parse('region', r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')
    movie['initialReleaseDate'] = '/'.join(info.xpath(".//span[@property='v:initialReleaseDate']/text()"))
    try:
        movie['runtime'] = info.xpath(".//span[@property='v:runtime']/text()")[0]
    except:
        movie['runtime']=''
    movie['rating']=html.xpath("//strong[starts-with(@class,'ll rating_num')]/text()")[0]
    stars=html.xpath("//span[starts-with(@class,'rating_per')]/text()")
    i=5
    for star in stars:
        stri='stars'+str(i)
        movie[stri]=star
        i-=1


    return movie

def main():
    j=1
    # movies=[]
    for i in range(12):
        html = get_movie_page(i*20) #爬取了当前页面信息
        for item in parse_index_movie(html):
            print(j)
            a=item.get('url')

            movie=get_info(get_html(a))
            movie['title'] = item.get('title')


            sql_insert = """INSERT INTO doubanrmdy VALUES("%d","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")""" % \
                         (j,str(pymysql.escape_string(movie.get('title'))),
                          str(pymysql.escape_string(movie.get('director'))),
                          str(pymysql.escape_string(movie.get('screenwriter'))),
                          str(pymysql.escape_string(movie.get('actors'))),
                          str(pymysql.escape_string(movie.get('type'))),
                          str(pymysql.escape_string(movie.get('region'))),
                          str(pymysql.escape_string(movie.get('initialReleaseDate'))),
                          str(pymysql.escape_string(movie.get('runtime'))),
                          float(pymysql.escape_string(movie.get('rating'))),
                          str(pymysql.escape_string(movie.get('stars5'))),
                          str(pymysql.escape_string(movie.get('stars4'))),
                          str(pymysql.escape_string(movie.get('stars3'))),
                          str(pymysql.escape_string(movie.get('stars2'))),
                          str(pymysql.escape_string(movie.get('stars1'))))

            cur.execute(sql_insert)

            j+=1
            # movies.append(movie)
            # print(movies.pop())
            conn.commit()

            flag = True
            for i in range(0,1):
             try:
                html = get_one_page(i*20,a)
                flag = parse_one_page(html)

             except Exception:
                continue

    conn.close()



if __name__ == '__main__':
   main()
