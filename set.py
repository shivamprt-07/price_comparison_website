from flask import Flask,render_template,request
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def fetch_amazon_page_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(2)  # Allow time for the page to load
    page_source = driver.page_source
    driver.quit()
    return page_source




app = Flask(__name__)

#header for flipkart
headers_flip = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

#header for amazon
headers_amaz = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.178 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}






options = Options()
options.add_argument('--headless')
options.add_argument('--profile-directory=Default') 
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)





#to get flipkart product name for technologies
def flip_prize(product,Flag):
    url='https://www.flipkart.com/search?q=' + product + '&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY'
    driver.get(url)
    html = driver.page_source
    page = BeautifulSoup(html, features="html.parser")
    main_box= page.find_all('div',{"class":"tUxRFH"})
    box=main_box[0]
    temp=[]
    try:
        if Flag==False:
            for box in main_box:
                s="https://www.flipkart.com"
                link=box.find("a",{"class":"CGtC98"},href=True)
                l=s+link['href']
                #print(l)
                val=box.find("div",{"class":"KzDlHZ"}).text.strip()
                product_img = box.find('img',{'class':'DByuf4'}).get('src')
                #print(val)
                if product.lower() in val.lower():
                    price=box.find("div",{"class":"Nx9bqj _4b5DiR"}).text.strip()
                    temp.append([l,product_img,val,price])
                    #print(temp)
        else:
            for box in main_box:
                s="https://www.flipkart.com"
                link=box.find("a",{"class":"CGtC98"},href=True)
                #print(link['href'])
                l=s+link['href']
                title=box.find("div",{"class":"KzDlHZ"}).text.strip()
                price=box.find("div",{"class":"Nx9bqj _4b5DiR"}).text.strip()
                product_img = box.find('img',{'class':'DByuf4'}).get('src')
                temp.append([l,product_img,title,price])
                #print(temp)
    except:
        i=1
    #print(temp)
    return temp

#to get amazon product name for technologies
def amaz_price(product,Flag):
    url="https://www.amazon.in/s?k=" + product + "&crid=3GQP78C68F4YO&sprefix=t%2Caps%2C395&ref=nb_sb_ss_organic-diversity_1_1"
    response=requests.get(url,headers=headers_amaz)
    page_source = fetch_amazon_page_with_selenium(url)
    soup = BeautifulSoup(page_source, 'html.parser')
    main_box= soup.find_all('div',{"role":"listitem"})
    print(len(main_box))
    temp=[]
    print("hello")
    if Flag==False:
        for box in main_box:
            s="https://www.amazon.in"
            link=box.find("a",{"class":"a-link-normal s-line-clamp-2 s-link-style a-text-normal"},href=True)
            l=s+link['href']
            val=box.find("span",{"class":"a-link-normal s-line-clamp-2 s-link-style a-text-normal"}).text.strip()
            product_img=box.find("img",{"class":"s-image"}).get('src')
            if product.lower() in val.lower():
                pr=box.find("span",{"class":"a-price-whole"})
                price= pr.text.strip() if pr else "N/A"
                if price!="N/A":
                    temp.append([l,product_img,val,price])
                    #print(temp)
    else:
        for box in main_box:
            s="https://www.amazon.in"
            link=box.find("a",{"class":"a-link-normal s-line-clamp-2 s-link-style a-text-normal"},href=True)
            print(box)
            l=s+link['href']
            
            title=box.find("h2",{"class":"a-size-medium a-spacing-none a-color-base a-text-normal"}).text.strip()
            pr=box.find("span",{"class":"a-offscreen"})
            price= pr.text.strip() if pr else "N/A"
            product_img=box.find("img",{"class":"s-image"}).get('src')
            if price!="N/A":
                temp.append([l,product_img,title,price])
                #print(temp)
            
    
    #print(temp)
    return temp

#to get flipkart product name for others
def flip_app_price(product):
    url='https://www.flipkart.com/search?q=' + product + '&otracker=AS_Query_HistoryAutoSuggest_2_0&otracker1=AS_Query_HistoryAutoSuggest_2_0&marketplace=FLIPKART&as-show=on&as=off&as-pos=2&as-type=HISTORY'
    driver.get(url)
    html = driver.page_source
    page = BeautifulSoup(html, features="html.parser")
    main_box= page.find_all('div',{"class":"_1sdMkc LFEi7Z"})
    box=main_box[0]
    temp=[]
    try:
        for box in main_box:
            s="https://www.flipkart.com"
            link=box.find("a",{"class":"rPDeLR"},href=True)
            l=s+link['href']
            title= box.find("a",{"class":"WKTcLC"}).text.strip()
            price= box.find("div",{"class":"Nx9bqj"}).text.strip()
            product_img = box.find('img',{'class':'_53J4C-'}).get('src')
            temp.append([l,product_img,title,price])
    except:
        i=1
    return temp

#to get amazon product name for others

def amaz_app_price(product):
    url = "https://www.amazon.in/s?k=" + product + "&crid=3GQP78C68F4YO&sprefix=t%2Caps%2C395&ref=nb_sb_ss_organic-diversity_1_1"
    
    # Make the request to Amazon
    response = requests.get(url, headers=headers_amaz)
    
    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the main product listings
    main_box = soup.find_all('div', {"class": "sg-col-inner"})
    
    # If no products found, return an empty list
    if not main_box:
        print("No products found.")
        return []
    
    temp = []
    try:
        for box in main_box:
            s = "https://www.amazon.in"
            link = box.find("a", {"class": "a-link-normal s-line-clamp-2 s-link-style a-text-normal"}, href=True)
            if link:
                l = s + link['href']
                title = box.find("h2", {"class": "a-size-base-plus a-spacing-none a-color-base a-text-normal"}).text.strip()
                price = box.find("span", {"class": "a-offscreen"}).text.strip() if box.find("span", {"class": "a-offscreen"}) else "Price Not Available"
                product_img = box.find("img", {"class": "s-image"}).get('src') if box.find("img", {"class": "s-image"}) else "No Image"
                temp.append([l, product_img, title, price])
    except Exception as e:
        print(f"Error during scraping: {e}")
    
    return temp
#main function
@app.route('/')
def main():
    return render_template('index.html')


# main template for having product name 
@app.route('/getValue', methods=['POST'])
def getValue():
    words = ["under", "below", "above", "new", "phones", "mobiles", "laptops"]
    product_name = request.form['proName']
    choice = request.form['choice']
    print("hello")
    
    if choice == "tech":
        Flag = False
        for word in words:
            if word in product_name:
                Flag = True
                break
        
        flip_list = flip_prize(product_name, Flag)
        amaz_list = amaz_price(product_name, Flag)  # Corrected function name
        
        return render_template('pass.html', p=product_name, li=flip_list, li_amaz=amaz_list)
    
    else:
        flip_list = flip_app_price(product_name)
        amaz_list = amaz_app_price(product_name)  # Corrected function name
        
        return render_template('passother.html', p=product_name, li=flip_list, li_amaz=amaz_list)

        

app.run() 