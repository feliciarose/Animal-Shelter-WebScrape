import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

def main():

    URL = 'https://public-solutions.hillsboroughcounty.org/enterprise/wwv_flow.ajax'
    path = 'https://public-solutions.hillsboroughcounty.org/enterprise/'

    nums = ['1', '51', '101', '151', '201', '251', '301', '351', '401', '451', '501', '551', '601']

    for num in nums:
        getPage(URL, num, path)


def getPage(URL, num, path):

    raw_payload = 'p_flow_id=236&p_flow_step_id=11&p_instance=4501408421190&p_debug=&p_request=PLUGIN%3D0cAVf3gCTbw16BY_j5HyMj_JFyBcEhjQZYua8n4w0qcSj78-MdeGpvdZCoH7HXKY&p_widget_name=worksheet&p_widget_mod=ACTION&p_widget_action=PAGE&p_widget_action_mod=pgR_min_row%3D' + num + 'max_rows%3D50rows_fetched%3D50&p_widget_num_return=50&x01=624510002243935886&x02=624577032360111240&p_json=%7B%22pageItems%22%3Anull%2C%22salt%22%3A%22303801889182285054550439263054056762483%22%7D'
    
    payload = raw_payload.replace('\n', '').replace('\r', '')

    headers = {
        'authority': 'public-solutions.hillsboroughcounty.org',
        'accept': 'text/html, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': 'ORA_WWV_APP_236=ORA_WWV-L9RXFy_AqzhMssyTVTUYgPpt; nmstat=7292e1ff-8220-27a1-af3f-361517db4cad; _hjSessionUser_764005=eyJpZCI6IjYyNDMzZjQ2LTBmODItNTQxMi1iMDAxLTA5MzM1MmY3ZWJiZCIsImNyZWF0ZWQiOjE2ODk3MzM5MjQ4NDAsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_862202=eyJpZCI6ImU5MGYwZTg5LTcyNDEtNTRmMS05ZTM1LTdhM2M1YWY2N2MxMCIsImNyZWF0ZWQiOjE2ODk3MzM5MzMzMTEsImV4aXN0aW5nIjp0cnVlfQ==; _ga_QE5T04MEJ8=GS1.1.1691009472.2.0.1691009474.58.0.0; _ga=GA1.1.1466822568.1689733925; _ga_8W6YC9H2KZ=GS1.1.1691095364.9.0.1691095366.0.0.0',
        'dnt': '1',
        'origin': 'https://public-solutions.hillsboroughcounty.org',
        'referer': 'https://public-solutions.hillsboroughcounty.org/enterprise/f?p=236:11:::NO:::',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    r = requests.post(URL, data=payload, headers=headers)

    contents = r.content

    #easier reading and finding 
    soup = BeautifulSoup(contents, "html.parser")

    tree = html.fromstring(r.text)
    #print(soup)

    dataScrape(tree, soup, path)


def dataScrape(tree, soup, path,  kennel=[], gender=[], status=[], lotia=[], names=[], petLinks = [], mylinks=[], links=[], paths=[], animalID = []):

    #Full detailed pull
    details = tree.xpath('//td[contains(@class, " u-tL")]')
    unfiltered_info = []
    for detail in details:
        unfiltered_info.append(detail.text)

    info = [detail for detail in unfiltered_info if detail != None]

    #Organize full pull
    c, x, y, z = 1, 2, 3, 0
    #kennel, gender, status = [], [], []
    while x <= len(info):

        kennel.append(info[x])
        gender.append(info[y])
        status.append(info[z])
        animalID.append(info[c])
        c+=7
        x+=7
        y+=7
        z+=7
    
    print(kennel)
    print(gender)
    print(animalID)
    print(len(kennel))
    print(len(gender))
    print(len(animalID))

    #Lotia, Pulled this way because it is in ><
    lotias = tree.xpath('//td[contains(@class, " u-tR")]')
    for day in lotias:
        lotia.append(day.text)

    #Gets every individual name
    for link in soup.findAll('img'):
        names.append(link.get('title'))
    
    print(names)
    print(len(names))

    #Gets every individual link to connect to profile
    for link in soup.findAll('a'):
        href = link.get('href')
        petLinks.append(href)

        if href.startswith('f'):
            continue
        else:
            petLinks.remove(href) 

    #Add to new list with everything
    for link in petLinks:
        mylinks.append(link)

    #Remove duplicate paths
    #High time complexity fix later if this script is running too slow
    for id in mylinks:
        if id not in links:
            links.append(id)

    #Gets full paths
    paths = [path + link for link in links]

    #print(paths)

    if tree.xpath('//span[contains(@class, "a-Icon icon-irr-no-results")]'):
        buildFrame(kennel, names, animalID, gender, status, lotia, paths)
        exit()

def buildFrame(kennel, names, animalID, gender, status, lotia, paths, data = {}):

    #Dictionary: 'Kennel', 'Name', 'Gender', 'ID', 'Status', 'Lotia'
    data['Kennel'] = kennel
    data['Name'] = names
    data['ID'] = animalID
    data['Gender'] = gender
    data['Status'] = status
    data['Lotia'] = lotia
    data['Path'] = paths

    df = pd.DataFrame(data)
    print(df)

    #return df

main()