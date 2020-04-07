from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

# Program for botting different instagram functions
# Commandline arguments sys.argv[1] is username
#                       sys.argv[2] is password

class InstaBot:
    def __init__(self): ########## __init__ ##############
        self.followingFound = False
        self.followersFound = False

        options = Options()
        options.add_argument('--incognito')
        options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

        #open instagram
        self.driver.maximize_window()
        self.driver.get("https://instagram.com")

        
    def login(self, username, password):
        self.driver.get("https://instagram.com")
        self.username = username
        self.password = password

        #input username and password
        print('Logging in')
        loginbar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')))
        loginbar.send_keys(self.username)

        passwordbar = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')))
        passwordbar.send_keys(self.password)

        #click on login
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[4]'))) \
            .click()   

        #close notification popup
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[2]'))) \
                .click() 
        except:
            print('Invalid Username and/or Password, Login not successful')
            return False
        print('Login Successful')
        return True

    def logout(self):
        #go to profile
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a'))) \
            .click()

        #hit settings
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Options"]'))) \
            .click()

        #hit logout
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div/button[9]'))) \
            .click()

    def findFollowers(self):
        print("Finding all followers")
        self.findFollow("followers")
        self.followersFound = True

    def findFollowing(self):
        print("Finding all following")
        self.findFollow("following")
        self.followingFound = True

    def findFollow(self, which): ############### findFollowing ##############
        #go to profile page
        print('\tOn profile page')
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a'))).click()
        
        #click on following box
        print('\tRunning through friendlist')
        if (which == "following"):
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/following")]'))).click()
        else:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@href, "/followers")]'))).click()

        scroll_box = self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]')))
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(2)
            ht = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight);return arguments[0].scrollHeight;""", scroll_box)
        print('\tFinished Scrolling')

        html_list = self.driver.find_element_by_xpath('/html/body/div[4]/div/div[2]/ul')
        items = html_list.find_elements_by_tag_name("a")
        if (which == "following"):
            self.following = {name.text for name in items if name.text != ''}
        else:
            self.followers = {name.text for name in items if name.text != ''}
        print('\tFriend\'s usernames saved')

        #close followinglist
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Close"]'))).click()

        print('\tNow on homescreen')
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img'))).click()

    def unfollow(self, friendUsername):
        #unlike all friend's pictures
        self.unLikeAllPics(friendUsername)

        #search friend's username
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))).send_keys(friendUsername)

        #click on friend profile
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div/div[2]/span'))).click()

        #click on following button
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/span/span[1]/button'))).click()

        #unfollow
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div/div[3]/button[1]'))).click()

        print('\tNow on homescreen')
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img'))).click()


    def likeAllFriendsAllPics(self): ####### likeAllFriendsAllPics ############
        if not self.followingFound:
            self.findFollowing()

        for username in self.following:
            self.likeAllPics(username)


    def likeAllPics(self, friendUsername):
        print('Starting to like all of ' + friendUsername + '\'s pictures')
        self.__changeAllPics(friendUsername, "like")
        print()

    def unLikeAllPics(self, friendUsername):
        print('Starting to dislike all of ' + friendUsername + '\'s pictures')
        self.__changeAllPics(friendUsername, "dislike")
        print()

    def __changeAllPics(self, friendUsername, switch): ######## likeAllPics ##############
        #search friend's username
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input'))).send_keys(friendUsername)

        #click on friend profile
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[2]/div[2]/div/a[1]/div/div[2]/span'))).click()

        check = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/div/header/section/div[1]/h2')))
        noPictures = len(self.driver.find_elements_by_xpath('//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div[2]/h1')) > 0
        if (noPictures):
            print('\tFriend has no pictures')
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img').click()
            return

        #open first picture
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class=" _2z6nI"]/article/div/div/div/div/a'))).click()

        i = 1 #picture number counter

        # button = self.driver.find_element_by_xpath('//button[@class="wp06b "]')
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Comment"]')))
        liked = len(self.driver.find_elements_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Unlike"]')) > 0
        disliked = len(self.driver.find_elements_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Like"]')) > 0

        if (disliked and switch == "like"):
            self.driver.find_element_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Like"]').click()
        elif (liked and switch == "dislike"):
            self.driver.find_element_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Unlike"]').click()
        i+=1
    
        #go to next picture
        try:
            current = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a').click()
        except:
            print('\tUser has only one picture\n')
            self.driver.find_element_by_xpath('/html/body/div[4]/div[3]').click()
            self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img').click()
            return

        while(True):
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Comment"]')))
            liked = len(self.driver.find_elements_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Unlike"]')) > 0
            disliked = len(self.driver.find_elements_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Like"]')) > 0
            if (disliked and switch == "like"):
                self.driver.find_element_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Like"]').click()
            elif (liked and switch == "dislike"):
                self.driver.find_element_by_xpath('//button[@class="wpO6b "]/*[name()="svg"][@aria-label="Unlike"]').click()
            i+=1

            try:
                self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div/a[2]').click()
                sleep(2)
            except:
                print('\tFinished all friends\'s ' + str(i) + ' pictures\n')
                self.driver.find_element_by_xpath('/html/body/div[4]/div[3]').click()

                print('\tNow on homescreen')
                self.driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[1]/a/div/div/img').click()
                return

    def watchAllStories(self):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="react-root"]/section/main/section/div[3]/div[2]/div[1]/a/div'))) \
            .click()
        while True:
            if (self.driver.find_element_by_xpath('/html/head/title').text != "Stories • Instagram"):
                break
            self.driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_RIGHT)


print("\nWelcome to the Instagram Botting program!\n")
myBot = InstaBot()

print("\nPlease login and navigate to the homepage of Instagram")
input("Close notification popup and then press any key when done\n")

done = False
while not done:
    print("\n\nMenu:")
    print("1: Like every picture from every friend")
    print("2: Find out who you follow that doesn't follow you back")
    print("3: Drop a friend (Dislike all pictures, then unfollow)")
    print("4: Skip through all stories")
    print("5: Like all of one friend's pictures")
    print("6: Logout")

    cin = input("Enter option: ")
    if (cin == "1"):
        myBot.likeAllFriendsAllPics()
    elif (cin == "2"):
        data = {}
        myBot.findFollowing()
        myBot.findFollowers()
        data = myBot.following - myBot.followers
        for name in sorted(data):
            print (name)
    elif (cin == "3"):
        friend = input("What is the username of the friend you want to drop?: ")
        myBot.unfollow(friend)
    elif (cin == "4"):
        myBot.watchAllStories()
    elif (cin == "5"):
        friend = input("What is the username?: ")
        myBot.likeAllPics(friend)
    else: #5
        myBot.logout()
        done = True
    

    


