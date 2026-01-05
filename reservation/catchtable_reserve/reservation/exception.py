from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

options = Options()
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)


def exception(wait):
        try:
            if driver.find_element(By.XPATH, "//span[contains(text(), '빈자리 알림 신청 마감')]"):
                print("예약 가능한 시간이 없습니다. 빈자리 알림 신청이 마감되었습니다.")
                driver.quit()
            elif driver.find_element(By.XPATH, "//p[contains(text(), '휴무일입니다.')]"):
                print("선택하신 날짜는 휴무일입니다.")
                driver.quit()
            elif driver.find_element(By.XPATH, "//p[contains(text(), '예약 오픈 전이에요')]"):
                print("선택하신 날짜는 접수 전 입니다.")
        except NoSuchElementException:
            print("요소를 찾지 못했습니다.")
