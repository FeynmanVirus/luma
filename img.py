from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import cv2 as cv
from PIL import Image
import pytesseract
import time
import csv
import re
import os
from urllib.request import urlretrieve
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText 

def main():
    url = "https://mausam.imd.gov.in/responsive/radar.php?id=Bhuj"
    
    options = Options()
        
    options.headless = True

    driver = webdriver.Firefox(options=options)

    driver.get(url)
    time.sleep(10)

    res = driver.execute_script("var network = performance.getEntries(); return network;")
    
    msg = []
    
    for r in res:
        if r['name'].endswith('.gif'):
            if 'caz' not in r['name']:
                continue
            fd = urlretrieve(r['name'], 'image.gif')
                
            img = Image.open('image.gif')
            
            for i, frame in enumerate(iter_frames(img)):
                frame.save('image.png', **frame.info)

            im = cv.imread('image.png')

            gray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
            blur = cv.GaussianBlur(gray, (3,3), 0)
            thresh = cv.threshold(blur, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]

        # Morph open to remove noise and invert image
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
            opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations=1)
            invert = 255 - opening
            
            data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
            try:
                date = re.search('.*(\d{4}[7/]\d{2}[7/]\d{2}).*(\d{2}:\d{2}:\d{2}).*', data) 
                if "7" in date.group(1):
                    date = re.sub('7', '/', date.group(1))
                dateobj = datetime.strptime(f"{date.group(1)} {date.group(2)}", "%Y/%m/%d %H:%M:%S")   
                img = {'datetime': dateobj + timedelta(minutes=330)}
                if img in msg or img['datetime'].year == 2023:
                    continue
                msg.append(img)
            except Exception as e:
                print(e)
                

                os.remove('image.gif')
                os.remove('image.png')
    driver.quit()

    #credentials 
    #sender_email = 'example@email.com'
    #sender_password = 'get new'

    #recipient_email = 'example2.com'

    # prepare email message
    content = ""
    count = 1
    email_sent = 0
    for m in msg:
        content += f"{count}. ✅ {m['datetime'].day} {m['datetime'].time()}\n" 
        count += 1
    print(content) 
    return {'content': content, 'date': msg[0]['datetime']}

    # prepare email 
    #email = MIMEText(content)
   # email['Subject'] = f"{msg[0]['date']} UPDATE"
    #email['From'] = sender_email 
   # email['To'] = recipient_email 
    
    # login smtp
  #  with smtplib.SMTP('smtp.gmail.com', 587) as server:
        #        server.starttls()
#        server.login(sender_email, sender_password)

    #    server.sendmail(sender_email, recipient_email, email.as_string())
   # email_sent += 1 

def iter_frames(im):
    try:
        i= 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

if __name__ == "__main__":
    main()
