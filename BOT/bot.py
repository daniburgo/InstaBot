import time, random, sys, re, json, os
from title import showTitle
from configparser import ConfigParser

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.command import Command
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager


class InstaBot(): 
    def __init__(self):        
        config = ConfigParser()
        config.read('config.ini')
        
        self.username = config['DEFAULT']['username']
        self.password = config['DEFAULT']['password']
        self.mode = config['DEFAULT']['mode']
        self.photo_links = []
        self.var1 = ["Love your", "Awesome", "Nice", "Great"]
        self.var2 = ["car", "photo", "pic"]
        self.mg = config['DEFAULT']['mg']
        self.mgCount = 0

        sys.argv.append('')
        if sys.argv[2] == "":
            self.target = config['DEFAULT']['target']
            self.user = config['LOVE']['pushUser']
            self.commentUrl = config['COMMENT']['url']
        else:
            pass

        #self.driver = webdriver.Chrome(executable_path=os.getcwd()+"/chromedriver.exe")
        self.driver = webdriver.Chrome(ChromeDriverManager().install())


    def updateData(self):
        with open('data.json', 'r') as f:
            data = json.load(f)
            data['likes'] += self.mgCount
        with open('data.json', 'w+') as f:
            json.dump(data, f)
        #print("Data updated successfully!!")


    def login(self):
        try:
            cookies = self.driver.find_element_by_css_selector("body > div.RnEpo.Yx5HN._4Yzd2 > div > div > button.aOOlW.bIiDR")
            cookies.click()
            time.sleep(1)
        except Exception:
            pass


        enter = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button"))
        ).click()
        time.sleep(0.5)
        login_user = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        login_user.send_keys(self.username)

        login_psw = self.driver.find_element_by_name("password")
        login_psw.send_keys(self.password)
        login_psw.send_keys(Keys.ENTER)


        try:
            not_now1 = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'cookies')]"))
            ).click()
        except Exception:
            pass

        try:
            not_now2 = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Ahora no')]"))
            ).click()
        except Exception:
            pass

        time.sleep(1)


    def auto_like(self):
        self.driver.get("https://www.instagram.com/explore/tags/{}/".format(self.target))

        self.login()
        time.sleep(1)

        scroll = int(self.mg)//5 +3
        while scroll > 0:       
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(1)
            scroll -= 1
        time.sleep(2)
        
        images = self.driver.find_elements_by_tag_name('a')
        images = [elem.get_attribute('href') for elem in images if '.com/p/' in elem.get_attribute('href')]
        for image in images:
            self.photo_links.append(image)
    
        print(str(len(self.photo_links)) + " photos loaded")
        self.mgCount = 0
        for image in self.photo_links:
            self.driver.get(image)
            time.sleep(1)
            try:          
                not_mg_click = self.driver.find_element_by_xpath("//*[@aria-label='Ya no me gusta' and @height='24']")
                if not_mg_click.is_displayed() == True:
                    print("Already liked")
                        
            except Exception:
                try:
                    mg_click = self.driver.find_element_by_xpath("//*[@aria-label='Me gusta' and @height='24']")
                    mg_click.click()
                    self.mgCount += 1
                    print("{} likes".format(self.mgCount))
                    if self.mgCount >= int(self.mg):
                        break
                    while self.mgCount < 10:
	                    self.driver.find_element_by_xpath("//*[@aria-label='Comentar' and @height='24']").click()
	                    comment_box = self.driver.find_element_by_css_selector('textarea.Ypffh')
	                    comment_box.clear()
	                    comment_box.send_keys("{} {}!!".format(random.choice(self.var1), random.choice(self.var2)))
	                    self.driver.find_element_by_class_name('X7cDz').submit()
                    time.sleep(1)

                except Exception as e:
                    print("Error: " + str(e))

        self.updateData()


    def loveUser(self):
        URL = f"https://instagram.com/{self.user}/"
        self.driver.get(URL)
        time.sleep(random.randint(2,5))

        self.login()
        
        posts = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span')
        text = posts.text
        print(f"\n--[{text} photos]--\n")
        if int(text) > 100:
            scroll = 20
        else:
            scroll = (int(text)//5)+2
        
        for x in range(scroll):
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(random.uniform(0.5,1))
        time.sleep(1)

        images = self.driver.find_elements_by_tag_name('a')
        images = [elem.get_attribute('href') for elem in images if '.com/p/' in elem.get_attribute('href')]
        print(f'\n--[{len(images)} photos loaded]--  (scroll={scroll})\n')
        
        mgCount = 0
        ########################################
        for image in images:
            self.photo_links.append(image)
        for image in self.photo_links:
        ######################################## 
            self.driver.get(image)
            time.sleep(1)
            try:          
                not_mg_click = self.driver.find_element_by_xpath("//*[@aria-label='Ya no me gusta' and @height='24']")
                if not_mg_click.is_displayed() == True:
                    print("Already liked")
                        
            except Exception:
                try:
                    mg_click = self.driver.find_element_by_xpath("//*[@aria-label='Me gusta' and @height='24']")
                    mg_click.click()
                    mgCount += 1
                    print(f"{mgCount} likes")

                except Exception as e:
                    print(e)
        self.updateData()

    def comment(self):
        users = []
        with open("spam.txt", "r") as f:
            for line in f.readlines():
                line = re.match(r".+", line)
                print(line)
                users.append(line.group(0))

        URL = self.commentUrl
        self.driver.get(URL)
        time.sleep(1)

        self.login()

        mentions = 0
        for user in users:
            self.driver.get(URL)
            time.sleep(0.7)

            self.driver.find_element_by_xpath("//*[@aria-label='Comentar' and @height='24']").click()
            comment_box = self.driver.find_element_by_css_selector('textarea.Ypffh')
            comment_box.clear()
            comment_box.send_keys("@"+user)
            self.driver.find_element_by_class_name('X7cDz').submit()
            time.sleep(0.7)

            mentions += 1
            if (mentions/5)%1 == 0:
                print("Please, wait to continue...")
                time.sleep(60)
            else:
                pass


    def close(self):
        print("Closing browser...")
        self.driver.quit()
        sys.exit()


def main():
    InstaBot().auto_like()
    InstaBot().close()


def action():
    InstaBot().loveUser()
    InstaBot().close()

def lottery():
    InstaBot().comment()
    InstaBot().close()
    
if __name__ == '__main__':

    print(" $$$$$$\                       $$\               $$$$$$$\             $$\     ")
    print(" \_$$  _|                      $$ |              $$  __$$\            $$ |    ")
    print("   $$ |  $$$$$$$\   $$$$$$$\ $$$$$$\    $$$$$$\  $$ |  $$ | $$$$$$\ $$$$$$\   ")
    print("   $$ |  $$  __$$\ $$  _____|\_$$  _|   \____$$\ $$$$$$$\ |$$  __$$\\_$$  _|  ")
    print("   $$ |  $$ |  $$ |\$$$$$$\    $$ |     $$$$$$$ |$$  __$$\ $$ /  $$ | $$ |    ")
    print("   $$ |  $$ |  $$ | \____$$\   $$ |$$\ $$  __$$ |$$ |  $$ |$$ |  $$ | $$ |$$\ ")
    print(" $$$$$$\ $$ |  $$ |$$$$$$$  |  \$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$  | \$$$$  |")
    print(" \______|\__|  \__|\_______/    \____/  \_______|\_______/  \______/   \____/ \n")

    sys.argv.append("")
    if sys.argv[1] == '/m':
        sys.argv.append("")
        if sys.argv[2] != "":
            InstaBot.target = sys.argv[2]
            main()
        else:
            main()

    elif sys.argv[1] == '/l':
        sys.argv.append("")
        if sys.argv[2] != "":
            InstaBot.user = sys.argv[2]
            action()
        else:
            action()
    
    elif sys.argv[1] == '/c':
        sys.argv.append("")
        if sys.argv[2] != "":
            InstaBot.commentUrl = sys.argv[2]
            lottery()
        else:
            lottery()

    else:
        if InstaBot().mode == "main":
            main()
        if InstaBot().mode == "love":
            action()
        elif InstaBot().mode == "comment":
            lottery()
        else:
            print("Invalid MODE. Loading default...")
            main()