from traceback import print_tb
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import csv

def getMallDetails(s, id):
    try:
        
        source = s.get(f"https://www.allaboutoutdoor.com/mall-media-detail.php?mid={mallId}")
        source.raise_for_status()

        soup = BeautifulSoup(source.text,'html.parser')
        dom = etree.HTML(str(soup))
        tables = dom.cssselect('table.media_detail_result_left2')
        images = dom.cssselect('ul#media')
        
        imageListItems = images[0].cssselect('li')

        dataTable = tables[0]
        rows = dataTable.cssselect('tr')

        mallTable = {
            'Id': mallId
        }

        for row in rows:
            values = row.cssselect('p')
            if(len(values) == 0): continue
            fieldName = values[0].getchildren()[0].text
            fieldValue = values[1].getchildren()
            if len(fieldValue) == 0:
                fieldValue = values[1].text.strip().replace(':', '')
            else:
                fieldValue = fieldValue[0].text.replace(':', '')
            mallTable[fieldName] = fieldValue

        mallImages = [liItem.getchildren()[0].attrib.get('src') for liItem in imageListItems]
        mallImages = [img for img in mallImages if img is not None]
        mallImages = ['https://allaboutoutdoor.com/' + img for img in mallImages]

        mallTable['images'] = mallImages
        return mallTable
    except Exception as e:
        print(e)
        return None


try:
    
    malls = [37120]
    s = requests.Session()

    loginData = {
        'email': ' ',
        'password': ' ',
        'submit-x': 87,
        'submit-y': 11,
    }
    loginHeaders = {
        'content-type': 'application/x-www-form-urlencoded',
        'referer': 'https://www.allaboutoutdoor.com/login.php'
    }
    s.post('https://www.allaboutoutdoor.com/userlogin.php', data=loginData, headers=loginHeaders)

    #mallInfoList = []
    for mallId in malls:
        mallInfo = getMallDetails(s, mallId)
        #mallInfoList.append(mallInfo)
        print(mallInfo)
        #print(mallInfoList)
        print('\n\n')
        
    
except Exception as e:
    print(e)






    




