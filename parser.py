from bs4 import BeautifulSoup
import pandas as pd
import requests, re, os


session = requests.Session()
output = [[], [], [], [], []]
companies = ["Umbrella IT", "EPAM Systems", "СимбирСофт", "Nord Clan", "Larga", "SkillStaff", "Extyl", "Fircode",
             "YOJJI", "Reksoft", "Лайв Тайпинг", "Redlab", "SibDev", "Effective Technologies", "Sofix", "Простые решения",
             "Aero ", "JetBit", "Ипол", "Урал-Софт", "AWG", "InSales", "RNS-Soft"]
search_query = "Front-end developer"


def get_page(page_num=0):
    response = session.get(f"https://hh.ru/search/resume?clusters=true&exp_period=all_time&logic=normal&no_magic=true&order_by=relevance&ored_clusters=true&pos=full_text&text={search_query.replace(' ', '+')}&items_on_page=100&page={page_num}", headers={'User-Agent': 'Custom'})
    if response.status_code == 404:
        return None
    return response.text


def parse_person(url):
    global output, companies, session
    response = session.get(url, headers={'User-Agent': 'Custom'})
    page = response.text
    soup = BeautifulSoup(page, 'html.parser')
    location = soup.find('span', {'data-qa': 'resume-personal-address'}).text
    try:
        work_places = soup.find('div', {'data-qa': 'resume-block-experience'}).find('div', class_='resume-block-item-gap').find('div', class_='bloko-columns-row').find_all('div', class_='bloko-columns-row')
    except:
        work_places = []
    for work_place in work_places:
        blocks = work_place.find_all('div', 'bloko-column')
        company = blocks[1].find('div', class_='resume-block-container').find('div', class_='bloko-text').text
        if list(filter(lambda cmp: cmp in company, companies)):
            years = re.findall(r"(\d\d\d\d)", str(blocks[0]))
            position = blocks[1].find('div', {'data-qa': 'resume-block-experience-position'}).text
            ly = len(years)
            if ly > 1:
                years = f"{years[0]} - {years[1]}"
            elif ly == 1:
                years = str(years[0])
            output[0].append(location)
            output[1].append(company)
            output[2].append(position)
            output[3].append(years)
            output[4].append(link)
            break


links = []
page_num = 0
page = get_page()
while page:
    soup = BeautifulSoup(page, 'html.parser')
    items = soup.find_all('div', class_='resume-search-item')
    for item in items:
        link = 'https://hh.ru' + re.search(r"href=\"(.*?)\"", str(item)).group(1)
        parse_person(link)
    page_num += 1
    page = get_page(page_num)

file = pd.DataFrame({
    "Город": output[0],
    "Компания": output[1],
    "Должность": output[2],
    "Годы работы": output[3],
    "Ссылка на резюме": output[4]
})

if not os.listdir('data'):
    rn = 1
else:
    rn = int(os.listdir('data')[0][-6]) + 1
file.to_excel(f'data/result{rn}.xlsx') #script saves data in 'data' folder








