from catchtable_reserve.Authenticator import Authenticator
from catchtable_reserve.reservation.booking import booking

# 각 스레드에서 예약 작업을 실행하는 함수
def multi_control(url, date, 인원수):
    authenticator = Authenticator()  # 로그인 과정을 각 스레드에서 별도로 진행
    driver, wait = authenticator.login()  # 각 스레드에서 새롭게 로그인 세션 생성

    # 예약 진행
    booking(driver, wait, url=url, date=date, 인원수=인원수)

    driver.quit()  # 예약 완료 후 브라우저 닫기


