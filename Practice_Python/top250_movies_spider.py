import requests
import xlwt
from bs4 import BeautifulSoup


def get_url_list():
    for i in range(0, 250, 25):
        douban_url = "https://movie.douban.com/top250?start={0}&filter=".format(i)
        douban_list.append(douban_url)
    return douban_list


def get_html_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0'}
    response = requests.get(url=url, headers=headers)
    htmlPage = response.text
    return htmlPage


def get_info_from_page(htmlPage):
    soup = BeautifulSoup(htmlPage,"lxml")
    movies = soup.find('ol', class_='grid_view').find_all('li')
    for i in range(0, 25):
        movieName = movies[i].find('span').string
        movieScore = movies[i].find('span', class_='rating_num').string
        movieRatingNum = movies[i].find('div', class_='star').find_all('span')[-1].string.strip('人评价')
        movieQuote = movies[i].find('p', class_='quote').find('span').string if movies[i].find('p',
                                                                                               class_='quote') else 'NaN'
        result.append([movieName, movieScore, movieRatingNum, movieQuote])
    return result

def write_in_excel(result):
    book = xlwt.Workbook()
    sheet = book.add_sheet('movie_sheet')
    for row in range(0, 251):
        for col in range(0, 4):
            sheet.write(row, col, result[row][col])
    book.save('douban_top_250.xls')


if '__main__':
    douban_list = []
    result = []

    for i in get_url_list():
        htmlPage = get_html_page(i)
        result = get_info_from_page(htmlPage)
    result.insert(0, ['电影名', '评分', '评价人数', '短评'])

    write_in_excel(result)
