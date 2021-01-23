import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title = []
company_name = []
locations_name = []
skills = []
links =[]
salary = []
responsibilities = []
date = [] 
page_num = 0

while True:
    # 1 step use requests to fetch the url
    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=spbg&q=python&start={page_num}")

        #  2 step save page content / markup
        src = result.content
        #print(src)

        # 3 step create soup object to parse content
        soup = BeautifulSoup(src, "lxml")
        page_limit = int(soup.find("strong").text)
        
        if( page_limit > page_limit // 15 ):
            print("pages ended , terminate")
            #break

        #print(soup)

        # 4 step find the elements containing info we need 
        # -- job titles , job skills, company names, location names

        job_titles = soup.find_all("h2", {"class":"css-m604qf"}) #هنا نكتب  الصفات تبع (a) وتكون دكشنري key+value
        company_names = soup.find_all("a",{"class":"css-17s97q8"})
        locations_names = soup.find_all("span" , {"class":"css-5wys0k"})
        job_skills = soup.find_all("div",{"class":"css-y4udm8"})
        posted_new = soup.find_all("div" , {"class":"css-4c4ojb"})
        posted_old = soup.find_all("div" , {"class":"css-do6t5g"})
        posted = [*posted_new, *posted_old]


        #print(job_skills)

        # 5 step loop over returnned lists to extract needed info into other lists
        for i in range(len(job_titles)): 
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            locations_name.append(locations_names[i].text)
            skills.append(job_skills[i].text)
            date_text = posted[i].text.replace("-","").strip()
            date.append(date_text)
        
        page_num += 1
        print("page switched")

    except:
        print("error occurred")
        break

for link in links:
    result = requests.get(link)
    src =result.content
    soup = BeautifulSoup(src, "lxml")
    salaries = soup.find("div", {"class":"matching-requirement-icon-container" , "data-toggle":"tooltip" , "data-placement":"top"})
    salary.append(salaries.text.strip())
    requirements = soup.find("span", {"itemprop":"responsibilities"}).ul
    respon_text = ""
    for li in requirements.find_all("li"):
        respon_text += li.text+"| "
    respon_text = respon_text[:-2]
    responsibilities.append(respon_text)


# 6 step create csv file and fill it with jalue
file_list = [job_title, company_name , date , locations_name, skills , links , salary , responsibilities , date]
excepted = zip_longest(*file_list)
with open("F:/all programming/web scriping/jobstutorial.csv", "w") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["job title" , "company name","date", "location", "skills" , "links" ,"salary" , "responsibilities"])
    wr.writerows(excepted)


    # step is to optimize code and clean data