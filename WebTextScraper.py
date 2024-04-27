import requests
from bs4 import BeautifulSoup
import pandas

#read in list of URLs:
TextList = [];
progress = 0;
URL2Read = pandas.read_csv('F:\\UMN Data Science MS\\CSCI 5541\\Project\\TestSet_ReliableVsNot.csv')
for i in URL2Read['url']:
    display(i)
    res = requests.get(i)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    
    #set([t.parent.name for t in text]) #this will let you see list of text payloads in the html code.
    
    output = ''
    blacklist = [
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'button',
        'center',
        'cite',
        'div',
        'form',
        'a',
        'g',
        'img',
        'link',
        'footer',
        'h1',
        'form',
        'aside',
        'div',
        'ul',
        'time',
        'style',
        'h1',
        'body',
        'br',
        'button',
        'h1',
        'h2',
        'label',
        'li',
        'span',
        'strong',
        'svg',
        'tbody',
        'td',
        'tr',
        #'p',
        #'table',
        #'main',
        #'article',
        '[document]',
        # there may be more elements you don't want, such as "style", etc.
    ]
    
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    
    TextList.append(('unreliable',output))
    progress += 1
    print(progress/len(URL2Read['url'])*100)
    
df = pandas.DataFrame(TextList,columns = ['Label','Text']) #place text into a {label=unreliable/reliable, text=contents of article} df, then save that pandas df. 
df.to_csv('F:\\UMN Data Science MS\\CSCI 5541\\Project\\TestSet_text.csv', index=False)

#certain websites will not return a result (ex: WND). This is likely b/c they blocked your scrape attempt. To be sure, you can scrape using the single website code below. Then, check to see if the payload is "Forbidden" as the '[document]'. 
#Possible solutions to that issue are here: https://www.zenrows.com/blog/beautifulsoup-403#enhance-request-headers-for-better-acceptance

###To check an individual website...for debug purposes:

#URL = 'https://www.wnd.com/2023/07/rfk-jr-drops-vaccine-truth-bombs-fox-news-hitting-fauci-hard/'
#res = requests.get(URL)
#html_page = res.content
#soup = BeautifulSoup(html_page, 'html.parser')
#text = soup.find_all(text=True)
#set([t.parent.name for t in text])
#output = ''
#blacklist = []
#for t in text:
#    if t.parent.name not in blacklist:
#        output += '{} '.format(t)
    
        