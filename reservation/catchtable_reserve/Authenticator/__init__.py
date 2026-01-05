from catchtable_reserve.Authenticator.start_up import setting
from catchtable_reserve.Authenticator.naver_login import naver_login
from catchtable_reserve.Authenticator.kakao_login import kakao_login

class Authenticator:
    def __init__(self):
        self.login_url = 'https://app.catchtable.co.kr/ct/login'
        self.context = None
        self.login_page = None

    async def setting(self):
        self.context = await setting()
        return self.context

    async def naver_login(self):
        self.context, self.login_page = await naver_login(self.context, self.login_url)
        return self.context, self.login_page

    async def kakao_login(self):
        self.context, self.login_page = await kakao_login(self.context, self.login_url)
        return self.context, self.login_page