import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from selenium import webdriver
from selenium.webdriver.common.alert import Alert
import random

import pygame

import config


def wait_action(text: str):
    flag = True
    while flag:
        input(text)
        flag = False


def sleep_random():
    time.sleep(random.uniform(0.5, 1.5))


class Macro:
    def __init__(self, login_id: str, login_pw: str, ticket_url: str, birth_day: str):
        self.login_id = login_id
        self.login_pw = login_pw
        self.ticket_url = ticket_url
        self.birth_day = birth_day
        self.driver = webdriver.Chrome("chromedriver")

    def program_stop_with_alarm(self):
        pygame.init()
        self.alert_sound = pygame.mixer.Sound('alert.mp3')
        self.alert_sound.play()
        time.sleep(10)
        pygame.quit()
        while True:
            pass

    def login(self):
        login_url = "https://accounts.interpark.com/authorize/ticket-pc?origin=https%3A%2F%2Fticket%2Einterpark%2Ecom%2FGate%2FTPLoginConfirmGate%2Easp&postProc=IFRAME"
        self.driver.get(login_url)
        time.sleep(1)
        id_element = self.driver.find_element(By.XPATH, '//*[@id="userId"]')
        pw_element = self.driver.find_element(By.XPATH, '//*[@id="userPwd"]')

        id = self.login_id
        pw = self.login_pw
        id_element.send_keys(id)
        pw_element.send_keys(pw)

        login_btn_element = self.driver.find_element("id", "btn_login")
        login_btn_element.click()

        ticket_url = self.ticket_url
        self.driver.get(ticket_url)
        time.sleep(1)
        wait_action("원하는 경기 클릭 이후, 보안번호를 입력해주시고 엔터를 눌러주세요")

    def check_soldout_and_get_seat_element(self):
        seat_label = "매진"
        seat_element = None
        while seat_label == "매진":
            self.driver.switch_to.window(self.driver.window_handles[1])
            target_frame = self.driver.find_element(By.XPATH, '/html/body/div[2]/iframe')
            self.driver.switch_to.frame(target_frame)
            seat_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[1]/a/span[2]')
            seat_label = seat_element.text
            print("current_seat: ", seat_label)
            if seat_label == "매진":
                sleep_random()
                self.driver.refresh()
        return seat_element

    def select_auto_seat(self, seat_element):
        seat_element.click()
        autometic_element = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[4]/a[1]/img')
        autometic_element.click()

    def get_list_frame(self):
        self.driver.switch_to.default_content()
        list_frame = self.driver.find_element(By.XPATH, '//*[@id="ifrmBookStep"]')
        return list_frame

    def select_book_seat_and_check_soldout(self, list_frame):
        self.driver.switch_to.frame(list_frame)
        list_element = Select(self.driver.find_element(By.XPATH, '//*[@id="PriceRow000"]/td[3]/select'))
        list_element.select_by_value("1")

        self.driver.switch_to.default_content()
        finishButtonElement = self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]')
        finishButtonElement.click()

        certificate_frame = self.driver.find_element(By.XPATH, '//*[@id="ifrmBookCertify"]')
        self.driver.switch_to.frame(certificate_frame)
        certificate_button = self.driver.find_element(By.XPATH, '/html/body/div/div[1]/div/table/tbody/tr/td/input')
        certificate_button.click()
        accept_button = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/a[1]/img')
        accept_button.click()

        self.driver.switch_to.default_content()
        finishButtonElement.click()

        sleep_random()

    def click_alert(self):
        da = Alert(self.driver)
        print("text: ", da.text)
        da.accept()
        sleep_random()

    def set_delivery_method(self, list_frame):
        self.driver.switch_to.frame(list_frame)
        buy_hyeonjang_element = self.driver.find_element(By.XPATH, '//*[@id="Delivery"]')
        buy_hyeonjang_element.click()
        birth_day_element = self.driver.find_element(By.XPATH,
                                                "/ html / body / form / div / div[2] / div / div[1] / table / tbody / tr[2] / td / input")
        birth_day_element.send_keys(self.birth_day)

        self.driver.switch_to.default_content()
        finishButtonElement = self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]')
        finishButtonElement.click()

    def set_payment(self, list_frame):
        self.driver.switch_to.frame(list_frame)
        kakao_pay_element = self.driver.find_element(By.XPATH,
                                                '//*[@id="Payment_22084"]/td/input')
        kakao_pay_element.click()

        self.driver.switch_to.default_content()
        finishButtonElement = self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]')
        finishButtonElement.click()

    def set_agreement(self, list_frame):
        self.driver.switch_to.frame(list_frame)
        all_agree_element = self.driver.find_element(By.XPATH, '//*[@id="checkAll"]')
        all_agree_element.click()

        self.driver.switch_to.default_content()
        finishButtonElement = self.driver.find_element(By.XPATH, '//*[@id="LargeNextBtnImage"]')
        finishButtonElement.click()

if __name__ == '__main__':
    macro = Macro(config.id,
                  config.pw,
                  config.ticket_url,
                  config.birth_day)
    macro.login()
    try:
        while True:
            seat_element = macro.check_soldout_and_get_seat_element()
            macro.select_auto_seat(seat_element)
            list_frame = macro.get_list_frame()
            macro.select_book_seat_and_check_soldout(list_frame)
            try:
                macro.click_alert()
            except:
                print("success")
                sleep_random()
                macro.set_delivery_method(list_frame)

                sleep_random()
                macro.set_payment(list_frame)

                sleep_random()
                macro.set_agreement(list_frame)

                macro.program_stop_with_alarm()
    except:
        macro.program_stop_with_alarm()
