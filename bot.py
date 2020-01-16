from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import os
import time
import urllib.request

class my_bot:
    def __init__(self,username,password):
        self.username = username
        self.password = password

        self.driver = webdriver.Chrome("./chromedriver.exe")
        self.base = "https://www.instagram.com/"
        self.login()

    def login(self):
        self.driver.get(f'{self.base}accounts/login/')
        time.sleep(2)
        self.driver.find_element_by_name("username").send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        self.driver.find_elements_by_xpath("//div[contains(text(), 'Log In')]")[0].click()
        time.sleep(2)

    def nav_user(self, user):
        print(f"{self.base}{user}/")
        self.driver.get(f"{self.base}{user}/")

    def follow_user(self, user):
        self.nav_user(user)
        follow = self.driver.find_elements_by_xpath("//button[contains(text(),'Follow')]")[0]
        follow.click()

    def follow_lot(self,links):
        for link in links:
            self.driver.get(f"{self.base}{user}/")  
            follow = self.driver.find_elements_by_xpath("//button[contains(text(),'Follow')]")[0]
            follow.click()
            time.sleep(1)


    def infy_scroll(self):
        scroll_ps_time = 1
        self.last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_ps_time)
        self.new_height = self.driver.execute_script("return document.body.scrollHeight")

        if self.last_height == self.new_height:
            return True
        self.last_height = self.new_height
        return False

    def dwnld_imgs(self, user):
        self.nav_user(user)
        end = False
        srcs = []
        while not end:
            end = self.infy_scroll()
            srcs.extend([img.get_attribute('src') for img in self.driver.find_elements_by_class_name('FFVAD')])

        srcs = list(set(srcs))
        for idx, src in enumerate(srcs):
            self.dwnld(src,idx,user)

    def dwnld(self,src,img_filename,folder):
        folder_path = './{}'.format(folder)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        img_filename = 'image_{}.jpg'.format(img_filename)
        urllib.request.urlretrieve(src, '{}/{}'.format(folder, img_filename))
        time.sleep(0.08)

    def get_followers(self,user,count):
        self.nav_user(user)
        followers = self.driver.find_element_by_css_selector('ul li a')
        followers.click()      
        time.sleep(2)
        followersList = self.driver.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
    
        followersList.click()
        actionChain = webdriver.ActionChains(self.driver)
        while (numberOfFollowersInList < count):
            actionChain.key_down(Keys.SPACE).perform()
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)
        
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')           
            print(userLink)
            followers.append(userLink)
            if (len(followers) == count):
                break
        return followers
        
    def create_user_base(self,root,f_cnt):
        d = {}
        for person in root:
            f = self.get_followers(person,f_cnt)
            d[person] = f
        return d


if __name__ == "__main__":
    with open('details.json') as json_data_file:
        data = json.load(json_data_file)

    bot = my_bot(data['devashish']["username"],data['devashish']["pass"])
    root = ['googledsc_dtu','chirag_c.s']
    f_base = bot.create_user_base(root,100)
    print(f_base)
    path = "P:\python_projects\IG_bot\Records\RECORD.json"
    with open(path, 'w') as fp:
        json.dump(f_base, fp)





    #bot.nav_user("mohdzeeshanayyub")
    #bot.follow_user("thepracticaldev")
    #bot.dwnld_imgs("carryminati")
    #foll = bot.get_followers('googledsc_dtu',125)
    #print(foll)
    print(bot.username)
