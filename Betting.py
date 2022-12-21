from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep


class OddsMoney():
    def __init__(self, username, password, url, bookmaker_bet=None, bookmaker_odds=None):
        self._username = username
        self._password = password
        self._url = url
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(
            'C:/Users/roybr/OneDrive/Desktop/Arbitrage betting/chromedriver.exe')  # Enter the correct pathname on your PC
        self.driver = webdriver.Chrome(options=options, service=Service(
            ChromeDriverManager().install()))
        pass

    def navigateOddsMonkey(self):
        self.driver.maximize_window()
        self.driver.get(self._url)
        self.driver.find_element(
            By.ID, 'MainContent_MainContent_Email').send_keys(self._username)
        self.driver.find_element(
            By.ID, 'MainContent_MainContent_Password').send_keys(self._password)
        self.driver.find_element(
            By.ID, 'MainContent_MainContent_btnLogin').click()

        try:
            sleep(2)
            self.driver.find_element(By.LINK_TEXT, 'OddsMatcher').click()

        except:
            for _ in range(2):
                self.driver.find_element(
                    By.XPATH, "//a[@id='ctl00_ctl00_MainContent_MainContent_rlvSessions_ctrl0_lbLogOut']").click()
                sleep(2)
            sleep(2)
            self.driver.find_element(By.LINK_TEXT, 'OddsMatcher').click()
        pass

    def choosingMatch(self):
        state = False
        iterator = 1

        self.driver.find_element(
            By.XPATH, "//select[@id='MainContent_MainContent_ddlSort']").click()
        self.driver.find_element(By.XPATH, "//option[@value='7']").click()
        sleep(2)

        while state == False:
            try:
                self.driver.find_element(
                    By.ID, 'ctl00_ctl00_MainContent_MainContent_rpOddsMatcher_Desktop_ctl{0:0=2d}_lbOpenCalc'.format(iterator)).click()
            except:
                self.driver.find_element(
                    By.ID, 'ctl00_ctl00_MainContent_MainContent_rpOddsMatcher_Desktop_ctl{0:0=2d}_lbOpenCalc'.format(iterator)).send_keys("\n")

            try:
                sleep(5)
                self.driver.find_element(
                    By.XPATH, "//button[normalize-space()='OK']").click()
            except:
                print('No changes')
            finally:
                sleep(2)
                self.bookmaker_bet = self.driver.find_element(
                    By.XPATH, "//span[@id='MainContent_MainContent_Modal_OMCalculator_lblBetAmount']").text
                sleep(1)
                self.bookmaker_odds = self.driver.find_element(
                    By.XPATH, "//span[@id='MainContent_MainContent_Modal_OMCalculator_lblBetOdds']").text
                sleep(1)
                self.team = self.driver.find_element(
                    By.XPATH, '//span[@id="MainContent_MainContent_Modal_OMCalculator_lblOutcome2"]').text

                try:
                    sleep(5)
                    self.driver.find_element(
                        By.XPATH, "//input[@id='MainContent_MainContent_Modal_OMCalculator_btnSmarketsPlaceBet_simple']").send_keys("\n")
                    state = True
                except:
                    self.driver.find_element(
                        By.XPATH, "//div[@class='modal-dialog modal-dialog-centered modal-lg']//span[@aria-hidden='true'][normalize-space()='×']").click()
                    state = False

                print(iterator)
                iterator += 1

        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='No, cancel']").click()
        self.driver.find_element(
            By.XPATH, "//a[@id='MainContent_MainContent_Modal_OMCalculator_btnGoToBookie']").click()
        sleep(10)
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        self.driver.find_element(By.LINK_TEXT, "LOG IN").click()
        sleep(2)
        self.driver.find_element(
            By.XPATH, "//input[@id='userId']").send_keys(self._username)
        sleep(1)
        self.driver.find_element(
            By.XPATH, "//input[@name='password']").send_keys(self._password)
        self.driver.find_element(
            By.XPATH, "//button[normalize-space()='Log in']").click()

        try:
            sleep(10)
            self.driver.find_element(
                By.XPATH, "//button[normalize-space()='Ok']").click()

        except:
            self.driver.find_element(
                By.XPATH, "//input[@id='singleStake-0']").send_keys(self.bookmaker_bet)

        pass


name = ''  # Enter your username
Pw = ''  # Enter your password
link = 'https://members.oddsmonkey.com/account/login?&ReturnURL=/dashboard.aspx&_ga=2.69341655.611537318.1671373332-941471797.1671373331'

place_bet = OddsMoney(name, Pw, link)
place_bet.navigateOddsMonkey()
place_bet.choosingMatch()
