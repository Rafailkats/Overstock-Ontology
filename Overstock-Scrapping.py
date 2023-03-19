from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from csv import writer
import time,random,re,os,json

s=Service("c:/Users/rafail/Desktop/chromedriver")
driver = webdriver.Chrome(service=s)
col=['ID', 'Title', 'Price','Brand','Rating','Reviews','Material','Color'
                                  ,'AssemblyNeeded','MadeIn','Warranty Days','Image','Category/Class']
answ=os.path.exists('Overstock-Dataset.csv')
with open('Overstock-Dataset.csv', "a" if answ else "w") as creating_new_csv_file: 
    csv_writer = writer(creating_new_csv_file)
    if answ==False:
       csv_writer.writerow(col)
for i in range(3):
   url='https://www.overstock.com/Home-Garden/Living-Room-Chairs/Accent-Chairs,/chair-type,/2737/subcat.html' + '?page=' + str(i+1)
   driver.get(url)
   content=driver.page_source
   soup=BeautifulSoup(content,"html.parser")
   content=soup.find("script",{"type":"application/ld+json"})
   json_object = json.loads(content.contents[0])
   temp=json_object[1]['itemListElement']
   for x in temp:
      #delay
      rand=random.randint(3,6)
      time.sleep(rand)
      driver.get(x['url'])
      content=driver.page_source
      soup=BeautifulSoup(content,"html.parser")
      #title
      temp=soup.find('div',attrs={'class':'product-title'})
      if temp==None:
          continue
      title=temp.text
       #id
      id_temp=soup.find('div',attrs={'class':'item-number'}).text.strip()
      id_=id_temp[6:len(id_temp)]
      #price
      if soup.find('span',attrs={'class':'dollars'})==None:
          continue
      else:
          dollars=soup.find('span',attrs={'class':'dollars'}).text
          cents=soup.find('span',attrs={'class':'cents'}).text
          price=dollars + '.' + cents + ' EUR'
      #rating
      rating=soup.find('div',attrs={'class':'background-star-container add-to-cart-rating-stars'})
      rating=rating["data-rating"]
      #reviews
      reviews=soup.find('p',attrs={'class':'product-info-review-count'}).text.replace('Reviews','').strip()
      if reviews=="Review this item":
          reviews=0
      #image
      ima=soup.find("div", {"class":"hero-zoom-container"})
      try:
             ima=ima.find('img')
             ima=ima.get('src')
      except AttributeError:
              continue
      #brand
      brand=soup.find("span",{"id":"brand-name"})
      if brand==None:
          brand="No Info"
      else:
          brand=brand.find('a').text.strip()
      #Color
      color=soup.find("td", string='Color')
      if color==None:
        color="No Info"
      else:
        color=color.find_next().text.strip()
        color=color.replace(" ","")
        color=os.linesep.join([s for s in color.splitlines() if s])
      #Material
      material=soup.find("td", string='Material')
      if material==None:
          material="No Info"
      else:
          material=material.find_next().text.strip()
          material=material.replace(" ","")
          material=os.linesep.join([s for s in material.splitlines() if s])
      #Assembly
      asse=soup.find("td", string='Assembly')
      if asse==None:
        asse='No'
      else:
        asse=asse.find_next().text.strip()
        if "not" in asse or "Assembled" in asse:
           asse="No"
        else:
           asse="Yes"
      #Made in
      madeIn=soup.find("td", string='Country of Origin')
      if madeIn==None:
             madeIn = 'No Info'
      else:
             madeIn=madeIn.find_next().text.strip()
      #Warranty
      warranty=soup.find("td", string='Warranty')
      if warranty==None:
         warranty=0
      else:
         warranty=warranty.find_next().text
         try:
            if re.search(r'\d+', warranty)==None:
                warranty = 0
            else:
                temp=int(re.search(r'\d+', warranty).group())
                if 'year' in warranty:
                    warranty=temp*365
                else:
                    warranty=temp
         except TypeError:
                continue
      #Category- Class
      cat='Overstock/HomeItem/Furniture/Chair/AccentChair'
      entry=[id_,title,price,brand,rating,reviews,material,color,asse,madeIn,warranty,ima,cat]
      with open('Overstock-Dataset.csv', 'a+',newline='') as write_obj:
        csv_writer = writer(write_obj)
        try:
           csv_writer.writerow(entry)
        except UnicodeEncodeError:
            print("Error!!!")
            continue
driver.close()