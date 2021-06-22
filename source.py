from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import shared
from interface import *

'''
Developed independently by Riki Borders.
Development start: 5/23/2020
Source code containing bot class and associated methods. 
Auxiliary functions included in the interface.py file,
along with front end GUI code.
'''


class CommentBot():

    def __init__(self, username, password, mode):
        '''Comment bot constructor'''

        self._username = username
        self._password = password
        self._mode = mode #Comment mode
        self._acc_index = 0 #index of current account

        #Create a headless browser & protect from selenium detection
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--ignore-certificate-errors-spki-list')
        chrome_options.add_argument('--ignore-ssl-errors')

        self._driver = webdriver.Chrome('chromedriver.exe', chrome_options = chrome_options)

        #clear cookies
        #self._driver.delete_all_cookies()

        #Check if maximized browser is enabled
        with open('config.txt', 'r') as f:
            lines = f.readlines()
            #Locate target & check if fullscreen is enabled
            for line in lines:
                if 'fullscreen' in line:
                    target = line
                    break

            if 'True' in target:
                self._driver.maximize_window()
            else:
                pass

        self._base_url = 'https://www.instagram.com'

        add_console_message('Driver started. Optns: headless, automated, no switch') #Update console

        if self._mode == 'account':
            self.login()
            self.account_comment()
        elif self._mode == 'hashtag':
            self.login()
            self.hashtag_comment()
        elif self._mode == 'feed':
            self.login()
            #Get the user's desired feed behavior
            feed_behavior = get_feed_behavior()

            if feed_behavior == 'top':
                self.top_feed_comment()
            else:
                self.normal_feed_comment()
        else:
            add_console_message('Error: Invalid mode selected.') #Update console

    def login(self):
        '''login to instagram'''
        #clear cookies
        #self._driver.delete_all_cookies()

        self._driver.get(f'{self._base_url}/accounts/login/')
        self._driver.implicitly_wait(20) #wait for page to load
        time.sleep(random.randint(2, 6))

        #input username and pass
        try:
            user_field = self._driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input')
            user_field.click()
            user_field.send_keys(self._username)
            add_console_message(f'Sent credential: [{self._username}]') #Update console

            password_field = self._driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input')
            password_field.click()
            password_field.send_keys(self._password)
            add_console_message(f'Sent credential: [{self._password}]') #Update console

        except:
            user_field = self._driver.find_element_by_name('username')
            user_field.click()
            user_field.send_keys(self._username)
            add_console_message(f'Sent credential: [{self._username}]') #Update console

            time.sleep(random.randint(2, 6))

            password_field = self._driver.find_element_by_name('password')
            password_field.click()
            password_field.send_keys(self._password)
            add_console_message(f'Sent credential: [{self._password}]') #Update console
            time.sleep(1)

        try:
            self._driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button/div').click()
            time.sleep(2)

        except Exception:
            self._driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button').click()
            time.sleep(2)

        add_console_message('Login complete.') #Update console

        #Alternative login screen handling
        try:
            self._driver.find_element_by_xpath('/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]/button').click()
        except Exception:
            pass

        #If an additional window pops up, handle it
        try:
            self._driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div/section/div/button').click()
        except Exception:
            pass

        #Accept any sort of cookies
        try:
            self._driver.find_element_by_xpath("//*[contains(text(), 'Accept')]").click()
        except Exception:
            pass

        #Close potential pop-ups
        try:
            self._driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except Exception:
            time.sleep(1)

    def swap_account(self):
        '''if the user has more than 1 account, swap accounts'''

        user = 'none'#Initialize username

        self._acc_index += 1 #update acc index

        #Search for new account
        with open('accounts.txt', 'r') as f:
            lines = f.readlines()
            #Check if index greater than acc list
            if self._acc_index >= len(lines):
                self._acc_index = 0

            target_line = lines[self._acc_index]

            user, pword = target_line[:target_line.find(':')].strip('\n'), target_line[target_line.find(':')+1:].strip('\n')

        #Logout
        self._driver.get(f'{self._base_url}/{self._username}')
        self._driver.find_element_by_class_name('wpO6b ').click()
        targ_div = self._driver.find_element_by_xpath('/html/body/div[5]/div')
        time.sleep(1)
        self._driver.find_element_by_xpath('//button[text()="Log Out"]').click()
        time.sleep(1)

        #Re-assign username and password
        self._username = user
        self._password = pword
        time.sleep(2)
        self.login()
        add_console_message('Accounts Swapped.')

        #clear cookies
        #self._driver.delete_all_cookies()

    def top_feed_comment(self):
        '''Comment on posts that appear in the users feed'''

        add_console_message('Login successful.') #Update console

        #Close potential pop-ups
        try:
            self._driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except Exception:
            time.sleep(1)

        #Get the emulation flag to determine whether or not rapid refresh mode is used
        with open('config.txt', 'r') as f:
            lines = f.readlines()

            for line in lines:
                if 'emulation_flag' in line:
                    emulate_flag = line[15:]
                    emulate_flag = emulate_flag.strip('\n')

        #Get the user's desired refresh rate (used w/ feed mode)
        sleep_time = float(get_refresh_timer())

        #Get age limiter
        refresh_time = int(get_age_limiter())

        #Get timer to swap accounts
        acc_swap_time = int(get_account_swap_timer())

        #Calculate the age
        if refresh_time >= 60:
            calculated_time = refresh_time // 60
            max_time = int(calculated_time)
            time_type = 'MINUTES'
        else:
            max_time = int(refresh_time)
            time_type = 'SECONDS'

        add_console_message('Options recieved.') #Update console
        add_console_message(f'Rapid refresh enabled. rate: [{sleep_time}]') #Update console

        swap_start_time = time.time() #Initialize account swap timer
        cmnt_count = 0

        while True:
            #Gather recent articles (posts)
            articles = self._driver.find_elements_by_tag_name('article')

            #Get previously commented links (srcs) for later comparison
            with open('sources.txt', 'r') as f:
                lines = f.readlines()
                source_file_lines = f.readlines() #Save lines for later checks

                lines = [line.strip('\n') for line in lines]
                source_file_lines = [line.strip('\n') for line in lines]

            #Get img sources to identify posts
            article_dct = {} #Associate articles with their sources

            #Fill article dict with unused posts
            for article in articles:
                try:
                    div = article.find_element_by_class_name('_97aPb ') #Get post img div
                except Exception:
                    continue
                try:
                    img = div.find_element_by_tag_name('img')
                    src = img.get_attribute('src')
                except Exception: #If the image is a video, correct the source
                    img = div.find_element_by_tag_name('video')
                    src = img.get_attribute('src')

                #If src isnt used, save it, so re-comments are not made.
                if src not in lines:
                    article_dct[article] = src

            if len(article_dct) > 0:
                #Load comments
                with open('comments.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    comments = [line.strip() for line in lines]

                for article in article_dct:

                    target_comment = random.choice(comments) #Choose a comment

                    #get post data to check if post age is lower than limit
                    try:
                        post_age = article.find_element_by_tag_name('time').text
                        age_index = post_age.find(' ')
                        post_age_num = int(post_age[:age_index])

                    except Exception: #If we cant get text, skip.
                        continue

                    #Check if a comment exists. If so, skip this post
                    try:

                        element = WebDriverWait(self._driver, 1).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "r8ZrO"))
                        )
                        add_console_message('Post too old. Skipping.')
                        continue

                    except Exception:

                        #Check if time is in minutes and post is in seconds
                        if(time_type.upper() == 'MINUTES'):
                            if 'SECONDS' in post_age.upper():

                                #preload source
                                current_src = article_dct.get(article)

                                #Send the comment to be posted
                                try: #Try/accept to protect against disabled comments
                                    form = article.find_element_by_tag_name('form')
                                    comment_field = form.find_element_by_tag_name('textarea')
                                    comment_field.click()
                                    comment_field = form.find_element_by_tag_name('textarea') #relocate (element removed from DOM)

                                    #Scroll to view comment box
                                    self._driver.execute_script("window.scrollTo(0, 140);")

                                    comment_field.send_keys(target_comment)
                                    time.sleep(5)

                                    #Click post and finalize comment
                                    post_button = form.find_element_by_xpath("//*[contains(text(), 'Post')]")
                                    time.sleep(3)
                                    post_button.click()

                                    add_console_message(f'Comment posted. [{target_comment}]') #Update console

                                    #Update commented_post list
                                    with open('commented_posts', 'a+') as f:
                                        f.seek(0)
                                        line = f.readline()

                                        if (line == ''):
                                            f.write(f'(artcl) {article}')
                                        else:
                                            f.write(f'\n(artcl) {article}')

                                except Exception:
                                    add_console_message(f'Comments disabled on post.') #Update console

                                #update source list
                                with open('sources.txt', 'a+') as f:
                                    if current_src not in source_file_lines:
                                        f.write(current_src+'\n')

                                time.sleep(random.randint(1,2))
                                if cmnt_count < 3:
                                    cmnt_count += 1
                                else:
                                    self.emulate_human_behavior_feed()
                                    self.emulate_human_behavior_feed()
                                    cmnt_count = 0
                                break

                        #Check if max time and post time are the same and post is lower than max
                        if(time_type.upper() == 'MINUTES') and (post_age_num <= max_time):
                            if 'MINUTES' in post_age.upper():

                                #preload source
                                current_src = article_dct.get(article)

                                #Send the comment to be posted
                                try: #Try/accept to protect against disabled comments
                                    form = article.find_element_by_tag_name('form')
                                    comment_field = form.find_element_by_tag_name('textarea')
                                    comment_field.click()
                                    comment_field = form.find_element_by_tag_name('textarea') #relocate (element removed from DOM)

                                    #Scroll to view comment box
                                    self._driver.execute_script("window.scrollTo(0, 140);")

                                    comment_field.send_keys(target_comment)
                                    time.sleep(3)

                                    #Click post and finalize comment
                                    post_button = form.find_element_by_xpath("//*[contains(text(), 'Post')]")
                                    time.sleep(1)
                                    post_button.click()

                                    #Update commented_post list
                                    with open('commented_posts', 'a+') as f:
                                        f.seek(0)
                                        line = f.readline()

                                        if (line == ''):
                                            f.write(f'(artcl) {article}')
                                        else:
                                            f.write(f'\n(artcl) {article}')


                                    add_console_message(f'Comment posted. [{target_comment}]') #Update console

                                except Exception:
                                    add_console_message(f'Comments disabled on post.') #Update console

                                with open('sources.txt', 'a+') as f:
                                    if current_src not in source_file_lines:
                                        f.write(current_src+'\n')

                                time.sleep(random.randint(1,2))
                                if cmnt_count < 3:
                                    cmnt_count += 1
                                else:
                                    self.emulate_human_behavior_feed()
                                    self.emulate_human_behavior_feed()
                                    cmnt_count = 0
                                break

                        #Check if both times are in seconds, and compare them
                        if(time_type.upper() == 'SECONDS') and (post_age_num <= max_time):
                            if 'SECONDS' in post_age.upper():

                                #preload source
                                current_src = article_dct.get(article)

                                #Send the comment to be posted
                                try: #Try/accept to protect against disabled comments
                                    form = article.find_element_by_tag_name('form')
                                    comment_field = form.find_element_by_tag_name('textarea')
                                    comment_field.click()

                                    comment_field = form.find_element_by_tag_name('textarea') #relocate (element removed from DOM)

                                    #Scroll to view comment box
                                    self._driver.execute_script("window.scrollTo(0, 140);")

                                    comment_field.send_keys(target_comment)
                                    time.sleep(5)

                                    #Click post and finalize comment
                                    post_button = form.find_element_by_xpath("//*[contains(text(), 'Post')]")
                                    time.sleep(3)
                                    post_button.click()

                                    #Update commented_post list
                                    with open('commented_posts', 'a+') as f:
                                        f.seek(0)
                                        line = f.readline()

                                        if (line == ''):
                                            f.write(f'(artcl) {article}')
                                        else:
                                            f.write(f'\n(artcl) {article}')


                                    add_console_message(f'Comment posted. [{target_comment}]') #Update console

                                except Exception:
                                    add_console_message(f'Comments disabled on post.') #Update console

                                with open('sources.txt', 'a+') as f:
                                    if current_src not in source_file_lines:
                                        f.write(current_src+'\n')

                                time.sleep(random.randint(1,2))
                                if cmnt_count < 3:
                                    cmnt_count += 1
                                else:
                                    self.emulate_human_behavior_feed()
                                    self.emulate_human_behavior_feed()
                                    cmnt_count = 0
                                break


            self._driver.refresh() #Refresh the page for new posts

            #Rapid refresh or emulation protocols. (flag read in as str)
            if emulate_flag == 'False':
                self.emulate_human_behavior()
            else:
                time.sleep(sleep_time)

            #Update time (swap accounts every hour and a half)
            swap_end_time = (time.time() - swap_start_time)
            if swap_end_time >= acc_swap_time:
                self.swap_account()
                swap_start_time = time.time()

    def normal_feed_comment(self):
        '''Comment on posts that appear in the users feed (indiscriminate of being first comment)'''
        add_console_message('Login successful.') #Update console

        #Close potential pop-ups
        try:
            self._driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except Exception:
            time.sleep(1)

        #Get the emulation flag to determine whether or not rapid refresh mode is used
        with open('config.txt', 'r') as f:
            lines = f.readlines()

            for line in lines:
                if 'emulation_flag' in line:
                    emulate_flag = line[15:]
                    emulate_flag = emulate_flag.strip('\n')

        #Get the user's desired refresh rate (used w/ feed mode)
        sleep_time = float(get_refresh_timer())

        #Get age limiter
        refresh_time = int(get_age_limiter())

        #Get timer to swap accounts
        acc_swap_time = int(get_account_swap_timer())

        #Calculate the age
        if refresh_time >= 60:
            calculated_time = refresh_time // 60
            max_time = int(calculated_time)
            time_type = 'MINUTES'
        else:
            max_time = int(refresh_time)
            time_type = 'SECONDS'

        add_console_message('Options recieved.') #Update console
        add_console_message(f'Rapid refresh enabled. rate: [{sleep_time}]') #Update console

        swap_start_time = time.time()

        while True:
            #Gather recent articles (posts)
            articles = self._driver.find_elements_by_tag_name('article')

            #Get previously commented links (srcs) for later comparison
            with open('sources.txt', 'r') as f:
                lines = f.readlines()
                source_file_lines = f.readlines() #Save lines for later checks

                lines = [line.strip('\n') for line in lines]
                source_file_lines = [line.strip('\n') for line in lines]

            #Get img sources to identify posts
            article_dct = {} #Associate articles with their sources

            #Fill article dict with unused posts
            for article in articles:
                div = article.find_element_by_class_name('_97aPb ') #Get post img div

                img = div.find_element_by_tag_name('img')
                src = img.get_attribute('src')

                if src == None: #If the image is a video, correct the source
                    img = div.find_element_by_tag_name('video')
                    src = img.get_attribute('src')

                #If src isnt used, save it, so re-comments are not made.
                if src not in lines:
                    article_dct[article] = src

            if len(article_dct) > 0:
                #Load comments
                with open('comments.txt', 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    comments = [line.strip() for line in lines]

                for article in article_dct:

                    target_comment = random.choice(comments) #Choose a comment

                    #get post data to check if post age is lower than limit
                    try:
                        post_age = article.find_element_by_tag_name('time').text
                        age_index = post_age.find(' ')
                        post_age_num = int(post_age[:age_index])

                    except Exception: #If we cant get text, skip.
                        continue

                    #Check if time is in minutes and post is in seconds
                    if(time_type.upper() == 'MINUTES'):
                        if 'SECONDS' in post_age.upper():

                            #preload source
                            current_src = article_dct.get(article)

                            #Send the comment to be posted
                            form = article.find_element_by_tag_name('form')
                            comment_field = form.find_element_by_tag_name('textarea')
                            comment_field.click()
                            comment_field = form.find_element_by_tag_name('textarea') #relocate (element removed from DOM)

                            comment_field.send_keys(target_comment)
                            time.sleep(1)

                            #Click post and finalize comment
                            post_button = form.find_element_by_xpath("//*[contains(text(), 'Post')]")
                            time.sleep(3)
                            post_button.click()

                            #Update commented_post list
                            with open('commented_posts', 'a+') as f:
                                f.seek(0)
                                line = f.readline()

                                if (line == ''):
                                    f.write(f'(artcl) {article}')
                                else:
                                    f.write(f'\n(artcl) {article}')


                            add_console_message(f'Comment posted. [{target_comment}]') #Update console

                            with open('sources.txt', 'a+') as f:
                                if current_src not in source_file_lines:
                                    f.write(current_src+'\n')

                            time.sleep(random.randint(1,2))

                    #Check if max time and post time are the same and post is lower than max
                    if(time_type.upper() == 'MINUTES') and (post_age_num <= max_time):
                        if 'MINUTES' in post_age.upper():

                            #preload source
                            current_src = article_dct.get(article)

                            #Send the comment to be posted
                            form = article.find_element_by_tag_name('form')
                            comment_field = form.find_element_by_tag_name('textarea')
                            comment_field.click()
                            comment_field = form.find_element_by_tag_name('textarea') #relocate (element removed from DOM)

                            comment_field.send_keys(target_comment)
                            time.sleep(1)

                            #Click post and finalize comment
                            post_button = form.find_element_by_xpath("//*[contains(text(), 'Post')]")
                            time.sleep(3)
                            post_button.click()

                            #Update commented_post list
                            with open('commented_posts', 'a+') as f:
                                f.seek(0)
                                line = f.readline()

                                if (line == ''):
                                    f.write(f'(artcl) {article}')
                                else:
                                    f.write(f'\n(artcl) {article}')

                            add_console_message(f'Comment posted. [{target_comment}]') #Update console

                            with open('sources.txt', 'a+') as f:
                                if current_src not in source_file_lines:
                                    f.write(current_src+'\n')

                            time.sleep(random.randint(1,2))

                    #Check if both times are in seconds, and compare them
                    if(time_type.upper() == 'SECONDS') and (post_age_num <= max_time):
                        if 'SECONDS' in post_age.upper():

                            #preload source
                            current_src = article_dct.get(article)

                            #Send the comment to be posted
                            form = article.find_element_by_tag_name('form')
                            comment_field = form.find_element_by_tag_name('textarea')
                            comment_field.click()

                            comment_field = form.find_element_by_tag_name('textarea') #relocate (element removed from DOM)

                            comment_field.send_keys(target_comment)
                            time.sleep(1)

                            #Click post and finalize comment
                            post_button = form.find_element_by_xpath("//*[contains(text(), 'Post')]")
                            time.sleep(3)
                            post_button.click()

                            #Update commented_post list
                            with open('commented_posts', 'a+') as f:
                                f.seek(0)
                                line = f.readline()

                                if (line == ''):
                                    f.write(f'(artcl) {article}')
                                else:
                                    f.write(f'\n(artcl) {article}')

                            add_console_message(f'Comment posted. [{target_comment}]') #Update console

                            with open('sources.txt', 'a+') as f:
                                if current_src not in source_file_lines:
                                    f.write(current_src+'\n')

                            time.sleep(random.randint(1,2))



            self._driver.refresh() #Refresh the page for new posts

            #Rapid refresh or emulation protocols. (flag read in as str)
            if emulate_flag == 'False':
                self.emulate_human_behavior_short()
            else:
                time.sleep(sleep_time)

            #Update time (swap accounts every hour and a half)
            swap_end_time = (time.time() - swap_start_time)
            if swap_end_time >= acc_swap_time:
                self.swap_account()
                swap_start_time = time.time()

    def hashtag_comment(self):
        '''Comment on posts that contain a specific hashtag'''

        add_console_message('Login successful.') #Update console
        while True:

            #Emulate behavior before commenting
            choice = random.randint(0,1)
            if(choice == 1):
                self.emulate_human_behavior_short()
            else:
                self.emulate_human_behavior()

            time.sleep(random.randint(3, 15))

            #Select a hashtag
            with open('hashtags.txt', 'r') as f:
                lines = f.readlines()
                hashtags = [line.strip('\n') for line in lines]

            hashtag = random.choice(hashtags)

            add_console_message(f'Hashtag selected: {hashtag}') #Update console

            #Navigate to the hashtag page
            self._driver.get('{}/tags/{}/'.format(self._base_url, hashtag))
            self._driver.implicitly_wait(10)
            time.sleep(random.randint(3, 15))

            for i in range(1000):
                self._driver.execute_script(f"window.scrollTo(0, {i});")

            #Create a list of acceptable posts to comment on
            posts = []
            scroll_dist = 500

            self._driver.execute_script(f"window.scrollTo(0, {scroll_dist});")
            elements = self._driver.find_elements_by_css_selector("div.EZdmt a")
            posts = [elem.get_attribute('href') for elem in elements]

            #Check if link has been visited before
            with open ('commented_posts.txt', 'r') as f:
                lines = f.readlines()
                lines = [line.strip('\n') for line in lines] #Cleanup new lines

                to_remove = []

                for link in posts: #Compare gathered links to visited file
                    if link in lines:
                        to_remove.append(link)

                for link in to_remove: #Remove duplicates
                    if link in posts:
                        posts.remove(link)

            scroll_dist += 500 #Update scroll dist for potential loops
            time.sleep(random.randint(0, 5))

            #Select a post
            try:
                target_post = random.choice(posts)
                self._driver.get(target_post)
                self._driver.implicitly_wait(20) #wait for page to load

                #Reach the comment field and make a comment
                self._driver.find_element_by_class_name('Ypffh').click()
                time.sleep(random.randint(1,5))

                with open('comments.txt', 'r', encoding='utf-8') as f: #Pick a random comment
                    lines = f.readlines()
                    comments = [line.strip() for line in lines]
                    target_comment = random.choice(comments)

                self._driver.find_element_by_class_name('Ypffh').send_keys(target_comment)
                time.sleep(random.randint(1, 5))
                post_button = self._driver.find_element_by_xpath("//*[contains(text(), 'Post')]")
                time.sleep(random.randint(2, 3))
                post_button.click()
                time.sleep(random.randint(2, 6))

                add_console_message(f'Commenting complete [{target_comment}]') #Update console

                #50% chance to like the post, then randomly wait
                chance = 1 #random.randint(0,1)
                if (chance == 1):
                    self._driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
                    time.sleep(random.randint(0, 5))
                    add_console_message('Post liked') #Update console
                else:
                    time.sleep(random.randint(0, 4))

                self.emulate_human_behavior_short()

            except Exception:
                pass


    def account_comment(self):
        '''Comment on posts made by a specific account. The bot will
            select a random post on the account page, & comment on it.
            '''

        add_console_message('Login successful.') #Update console

        #Accounts will swap after 5 posts are commented on.
        comment_count = 0

        while True:
            #Emulate behavior before commenting
            choice = random.randint(0,1)
            if(choice == 1):
                self.emulate_human_behavior_short()
            else:
                self.emulate_human_behavior()

            time.sleep(random.randint(3, 10))

            #Build account list then elect an account
            with open('target_accounts.txt', 'r') as f:
                accounts = f.readlines()
                accounts = [acc.strip('\n') for acc in accounts]

            target = random.choice(accounts)

            add_console_message(f'Account selected: {target}') #Update console

            #Try/accept incase username changed
            try:
                #Navigate to acc, then build list of posts
                self._driver.get(f'{self._base_url}/{target}')
                self._driver.implicitly_wait(20) #wait for page to load

            except Exception:
                add_console_message('Username Changed. Skipping.') #Update console
                continue

            #Check if user has no posts or is private
            try: #Check if no posts
                no_posts = self._driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[2]/article/div[1]/div/div[2]/h1').text
                add_console_message('Account has no posts. Skipping.') #Update console
                continue
            except Exception:
                pass

            try: #Check if private
                private_acc = self._driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2').text
                add_console_message('Account is private. Skipping.') #Update console
                continue
            except Exception:
                pass

            try: #Check if page not found
                no_exist = self._driver.find_element_by_xpath('/html/body/div/div[1]/div/div/h2').text
                add_console_message('Page does not exist.') #Update console
                continue
            except Exception:
                pass

            #Scroll, then grab and filter links to be only posts.
            #If all posts have been visited, keep scrolling until we find some posts
            scroll_dist = random.randint(500, 540)
            posts = []

            self._driver.execute_script(f"window.scrollTo(0, {scroll_dist});")
            elements = self._driver.find_elements_by_css_selector("div._2z6nI a")
            posts = [elem.get_attribute('href') for elem in elements]

            #Check if link has been visited before
            with open ('commented_posts.txt', 'r') as f:
                lines = f.readlines()
                lines = [line.strip('\n') for line in lines] #Cleanup new lines

                to_remove = []

                for link in posts: #Compare gathered links to visited file
                    if link in lines:
                        to_remove.append(link)

                for link in to_remove: #Remove duplicates
                    if link in posts:
                        posts.remove(link)

            scroll_dist += 500 #Update scroll dist for potential loops
            time.sleep(random.randint(1, 2))

            #Select a post
            target_post = random.choice(posts)
            self._driver.get(target_post)
            self._driver.implicitly_wait(20) #wait for page to load

            time.sleep(random.randint(1,4))

            #Reach the comment field and make a comment
            self._driver.find_element_by_class_name('Ypffh').click()
            time.sleep(random.randint(1,4))

            with open('comments.txt', 'r', encoding='utf-8') as f: #Pick a random comment
                lines = f.readlines()
                comments = [line.strip() for line in lines]
                target_comment = random.choice(comments)

            add_console_message(f'Comment selected: {target_comment}') #Update console

            self._driver.find_element_by_class_name('Ypffh').send_keys(target_comment)
            time.sleep(random.randint(1, 5))
            post_button = self._driver.find_element_by_xpath("//*[contains(text(), 'Post')]")
            post_button.click()
            time.sleep(random.randint(4, 8))

            comment_count += 1 #Update count

            with open("commented_posts.txt", "a+") as f: #add the link to the 'commented' file
                f.seek(0) #Move to file start
                line = f.readline()

                if (line == ''):
                    f.write(f'{target_post}')
                else:
                    f.write(f'\n{target_post}')

            if comment_count == 5:
                comment_count = 0
                self.swap_account()

            self.emulate_human_behavior_short()

    def emulate_human_behavior(self):
        '''Emulate human behavior for a period of time'''

        add_console_message(f'Emulating human activity... (protocol 1)') #Update console

        #Refresh main feed
        self._driver.get(self._base_url)
        self._driver.implicitly_wait(20)
        self._driver.refresh()
        time.sleep(random.randint(1,10))
        self._driver.implicitly_wait(20)

        #Close potential pop-ups
        try:
            self._driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except Exception:
            time.sleep(1)

        #Randomly scroll through feed
        for i in range(500):
            self._driver.execute_script(f"window.scrollTo(0, {i});")
            y_pos = i

        time.sleep(random.randint(0,5)) #Generate random wait time, then keep scrolling
        distance = random.randint(4000, 10000)

        for i in range(y_pos, distance):
            if(i == 5153):
                time.sleep(random.randint(0,5))
            elif(i == 8255):
                time.sleep(random.randint(0,5))

            self._driver.execute_script(f"window.scrollTo(0, {i});")
            y_pos = i #Keep storing position incase we keep scrolling

        chance = random.randint(0,1)

        if (chance == 1): #50% chance to visit and scroll thru explore page
            self._driver.get(f'{self._base_url}/explore')
            self._driver.implicitly_wait(20)

            for i in range(random.randint(2000, 20000)):
                self._driver.execute_script(f"window.scrollTo(0, {i});")

            elements = self._driver.find_elements_by_css_selector("div.v1Nh3 kIKUG  _bz0w") #View random post
            posts = [elem.get_attribute('href') for elem in elements]

            try:
                target = random.choice(posts) #Go to post and simulate viewing
                self._driver.get(target)
                self._driver.implicitly_wait(20)
                time.sleep(random.randint(1, 3))
                self._driver.execute_script("window.scrollTo(0, 850);")
                time.sleep(random.randint(2, 6))
            except Exception:
                pass

        else: #continue scrolling through feed
            distance = random.randint(y_pos+5000, y_pos+10000) #Calculate a new scroll distance
            time.sleep(random.randint(1, 3))

            for i in range(y_pos, distance): #Scroll more w/ random waits
                if(i == 9500):
                    time.sleep(random.randint(0,7))
                elif(i == 16000):
                    time.sleep(random.randint(0,8))

                self._driver.execute_script(f"window.scrollTo(0, {i});")
                y_pos = i #Keep storing position incase we keep scrolling

    def emulate_human_behavior_feed(self):
        '''Emulate human behavior for a period of time, & RETURN TO FEED PAGE'''

        add_console_message(f'Emulating human activity... (protocol 1)') #Update console

        #Refresh main feed
        self._driver.get(self._base_url)
        self._driver.implicitly_wait(20)
        self._driver.refresh()
        time.sleep(random.randint(1,10))
        self._driver.implicitly_wait(20)

        #Close potential pop-ups
        try:
            self._driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except Exception:
            time.sleep(1)

        #Randomly scroll through feed
        for i in range(500):
            self._driver.execute_script(f"window.scrollTo(0, {i});")
            y_pos = i

        time.sleep(random.randint(0,5)) #Generate random wait time, then keep scrolling
        distance = random.randint(4000, 10000)

        for i in range(y_pos, distance):
            if(i == 5153):
                time.sleep(random.randint(0,5))
            elif(i == 8255):
                time.sleep(random.randint(0,5))

            self._driver.execute_script(f"window.scrollTo(0, {i});")
            y_pos = i #Keep storing position incase we keep scrolling

        chance = random.randint(0,1)

        if (chance == 1): #50% chance to visit and scroll thru explore page
            self._driver.get(f'{self._base_url}/explore')
            self._driver.implicitly_wait(20)

            for i in range(random.randint(2000, 20000)):
                self._driver.execute_script(f"window.scrollTo(0, {i});")

            elements = self._driver.find_elements_by_css_selector("div.v1Nh3 kIKUG  _bz0w") #View random post
            posts = [elem.get_attribute('href') for elem in elements]


        else: #continue scrolling through feed
            distance = random.randint(y_pos+4000, y_pos+5000) #Calculate a new scroll distance
            time.sleep(random.randint(1, 3))

            for i in range(y_pos, distance): #Scroll more w/ random waits
                if(i == 9500):
                    time.sleep(random.randint(0,7))
                elif(i == 16000):
                    time.sleep(random.randint(0,8))

                self._driver.execute_script(f"window.scrollTo(0, {i});")
                y_pos = i #Keep storing position incase we keep scrolling

        self._driver.get(self._base_url)


    def emulate_human_behavior_short(self):
        '''emulate human behavior for a shorter amount of time'''

        add_console_message(f'Emulating human activity... (protocol 2)') #Update console

        #Refresh main feed
        self._driver.get(self._base_url)
        self._driver.implicitly_wait(20)
        self._driver.refresh()
        time.sleep(random.randint(1,10))
        self._driver.implicitly_wait(20)

        #Close potential pop-ups
        try:
            self._driver.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        except Exception:
            time.sleep(1)

        #Randomly scroll through feed
        for i in range(1500):
            self._driver.execute_script(f"window.scrollTo(0, {i});")

        #Navigate to explore page
        self._driver.get(f'{self._base_url}/explore')
        self._driver.implicitly_wait(20)
        self._driver.refresh()

        #Set random wait times
        time1 = random.randint(2000, 6000)
        time2 = random.randint(9000, 15000)
        time3 = random.randint(15000, 19999)

        for i in range(random.randint(2000, 20000)):
            self._driver.execute_script(f"window.scrollTo(0, {i});")
            if (i == time1):
                time.sleep(random.randint(1,5))
            elif(i == time2):
                time.sleep(random.randint(1,3))
            elif(i == time3):
                time.sleep(random.randint(1,7))

        elements = self._driver.find_elements_by_css_selector("div.K6yM_ a") #View random post
        posts = [elem.get_attribute('href') for elem in elements]

        try:
            target = random.choice(posts) #Go to post and simulate viewing
            self._driver.get(target)
            self._driver.implicitly_wait(20)
            time.sleep(random.randint(1, 3))
            self._driver.execute_script("window.scrollTo(0, 850);")
            time.sleep(random.randint(2, 6))

        except Exception:
            pass


if __name__ == "__main__":
    print('nill')
