from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time

def check_exists_by_xpath(driver, xpath):
    try:
        driver.find_element("xpath",xpath)
    except NoSuchElementException:
        return False
    return True

def sync_get_element_by_xpath(driver, wait, xpath):

    try:
        wait.until(ec.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
#         print("Get element from xpath:{} Timeout".format(xpath))
        return None
    return driver.find_element("xpath",xpath)

def sync_get_elements_by_xpath(driver, wait, xpath):

    try:
        wait.until(ec.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
#         print("Get element from xpath:{} Timeout".format(xpath))
        return None
    return driver.find_elements("xpath",xpath)


def take_screenshot(url, screenshot_file_path,webdriver_delay):
    # start a new web driver headlessly to take screenshots

    #setup option for chrome profile
    chrome_options = Options()

    # chrome_options.add_argument("user-data-dir=/Users/huohsien/Library/Application Support/Google/Chrome/Default/")
    ## the following option is to solve the error if using the above cause a problem
    # chrome_options.add_argument("--remote-debugging-port=9222") 

    prefs = {'profile.default_content_setting_values.automatic_downloads': 1}
    chrome_options.add_experimental_option("prefs", prefs)

    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--start-maximized")

    #start web driver
    driver_t = webdriver.Chrome(options=chrome_options)
    driver_t.implicitly_wait(webdriver_delay)
    wait_t = WebDriverWait(driver_t, webdriver_delay)


    driver_t.get(url)
    print("start headless temp chrome driver. get {}".format(url))
    # sign in. when chrome_options user-data-dir is turned on, no need to sign in thus just need to wait for timeout

    signin_btn = sync_get_element_by_xpath(driver_t, wait_t, "//div[text()='Sign in']")
    if signin_btn is not None:
        signin_btn.click()
        print("switch to sign-in tab")

        email = sync_get_element_by_xpath(driver_t, wait_t, "//input[@id='email']")
        password = sync_get_element_by_xpath(driver_t, wait_t, "//input[@id='revealable-password']")

        if email is not None:
            email.send_keys("huohsien@gmail.com")
        if password is not None:
            password.send_keys("Huo18941256")

        signin_btn = sync_get_element_by_xpath(driver_t, wait_t, "//div[@data-testid='signin-form']//span[text()='Sign in']/..")
        
        signin_btn.click()
        print("sign in")

        # close chaptgpt help side panel

        btn = sync_get_element_by_xpath(driver_t, wait_t, "//button[@class='chakra-button css-twu8br']")
        print("try to close chat panel")
        if btn is not None:
            try:
                btn.click()
            except ElementNotInteractableException:
                print("chat panel was closed")
        print("start sleeping for 5 secs")
        time.sleep(5)

    height = driver_t.execute_script('var pageHeight = 0;function findHighestNode(nodesList) {for (var i = nodesList.length - 1; i >= 0; i--) {if (nodesList[i].scrollHeight && nodesList[i].clientHeight) {var elHeight = Math.max(nodesList[i].scrollHeight, nodesList[i].clientHeight);pageHeight = Math.max(elHeight, pageHeight);}if (nodesList[i].childNodes.length) findHighestNode(nodesList[i].childNodes);}} findHighestNode(document.documentElement.childNodes);return pageHeight;')
    width  = driver_t.execute_script('return document.documentElement.scrollWidth')
    driver_t.set_window_size(width, height)  # the trick
    print("width: {} height: {}".format(width,height))

    print("start sleeping for 2 secs")
    time.sleep(2)
    driver_t.save_screenshot(screenshot_file_path)
    driver_t.quit()

def sign_in(driver, wait):

    # when chrome_options user-data-dir is turned on, no need to sign in thus just need to wait for timeout

    signin_btn = sync_get_element_by_xpath(driver, wait, "//div[text()='Sign in']")
    if signin_btn is not None:
        signin_btn.click()

        email = sync_get_element_by_xpath(driver, wait, "//input[@id='email']")
        password = sync_get_element_by_xpath(driver, wait, "//input[@id='revealable-password']")

        if email is not None:
            email.send_keys("huohsien@gmail.com")
        if password is not None:
            password.send_keys("Huo18941256")

        signin_btn = sync_get_element_by_xpath(driver, wait, "//div[@data-testid='signin-form']//span[text()='Sign in']/..")
        if signin_btn is not None:
            signin_btn.click()
    

def close_chat_panel(driver,wait):
    # close chaptgpt help side panel
    btn = sync_get_element_by_xpath(driver, wait, "//button[@class='chakra-button css-twu8br']")
    if btn is not None:
        try:
            btn.click()
        except ElementNotInteractableException:
            print("chatgpt panel was closed")

def grab_all_youtube_links(content_html_str, download=False):

    content_soup = BeautifulSoup(content_html_str, 'html.parser')
    youtube_iframe_elms = content_soup.find_all('iframe', {'title': 'YouTube video player'})
    video_links = ''
    for idx, youtube_iframe_elm in enumerate(youtube_iframe_elms, start=1):
        video_link = youtube_iframe_elm['src']
        video_link = video_link + '#index={}_{}_{}_{}'.format(topic_name,lesson_name, part_name,idx)
        video_links = video_links + video_link + '\n\n'


    with open('all_youtube_video_links.txt','a') as fp:
        fp.writelines(video_links)