from requests import get
from bs4 import BeautifulSoup
import re, os

url = 'https://www.baidu.com/s'

def English2Chinese(word=''):
    params = {
        'wd': word,
    }

    headers = {
        'User-Agent': 'Chrome/64.0.3282.168'
    }

    html = get(url, params=params, headers=headers, timeout=11, )
    # print(html.status_code)

    soup = BeautifulSoup(html.text, 'lxml')
    # print(soup.prettify())

    tags = soup.find_all('span')  # 找到所有span标签

    r = re.compile(r'"(op_dict.+?)">')
    classAttributeList = r.findall(str(tags))  # 通过正则匹配tags中包含字符串‘op_dict’的字符串

    taglist = soup.find_all('span', attrs={
        'class': classAttributeList
    })
    '''
    # 查看获得得需要的标签
    for tag in taglist:
        print(tag)
    '''

    # 国家
    r = re.compile(r'"op_dict3_font14 op_dict3_gap_small">(.+?)</span>')
    nation = r.findall(str(taglist))

    # 发音
    r = re.compile(r'"op_dict3_font16 op_dict3_gap_small">(.+?)</span>')
    pronunciation = r.findall(str(taglist))

    # 词性
    r = re.compile(r'"op_dict_text1 c-gap-right">(.+?)</span>')
    nature = r.findall(str(taglist))

    # 中文翻译
    r = re.compile(r'op_dict_text2">(.*?)</span>', re.S)
    translatorOfChinese = r.findall(str(taglist))

    print()
    print(word)
    print()

    # 如果搜索结果页面没有翻译会出现数组溢出错误
    try:
        print(nation[0] + ' ' + pronunciation[0] + ' ' + nation[1] + ' ' + pronunciation[1])
    except:
        print('------Sorry!The word can not be translated!-----')
        os._exit(1)

    # 多个词性
    for i in range(8):
        try:
            print(nature[i] + '  ' + translatorOfChinese[i].replace('\n','').replace(' ',''))
        except:
            break

if __name__ == '__main__':
    word = input('Input an English word:')
    English2Chinese(word=word)
