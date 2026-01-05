from catchtable_reserve.reservation.booking import (
    booking,
    click_reservation_button,
    select_time_slot,
    choosing_table,
    choosing_menu,
    form_login,
    form_not_login
)

__all__ = [
    'macro',
    'booking',
    'click_reservation_button',
    'select_time_slot',
    'choosing_table',
    'choosing_menu',
    'form_login',
    'form_not_login'
]

class macro:
    def __init__(self, context):
        self.context = context
        self.booking_page = None


    async def booking_loop(self, wanted_times):
        try:
            self.context, self.booking_page = await click_reservation_button(self.context, self.booking_page)
            self.context, self.booking_page = await select_time_slot(self.context, self.booking_page, wanted_times)
            self.context, self.booking_page = await choosing_table(self.context, self.booking_page)
            self.context, self.booking_page = await choosing_menu(self.context, self.booking_page)
            self.context, self.booking_page = await form_login(self.context, self.booking_page)
        
        except Exception as e:
            print(f"예약 과정에서 오류가 발생했습니다: {e}")
            await self.booking_page.close()
            if len(self.context.pages) == 0:
                raise Exception("모든 창이 닫혔습니다. 드라이버를 종료합니다.")
        return self.context, self.booking_page

    async def booking(self, url: str, date: str, 인원수: int):
        self.context, self.booking_page = await booking(self.context, url, date, 인원수)
        return self.context, self.booking_page

    async def click_reservation_button(self):
        self.context, self.booking_page = await click_reservation_button(self.context, self.booking_page)
        return self.context, self.booking_page

    async def select_time_slot(self, wanted_times):
        self.context, self.booking_page = await select_time_slot(self.context, self.booking_page, wanted_times)
        return self.context, self.booking_page

    async def choosing_table(self):
        self.context, self.booking_page = await choosing_table(self.context, self.booking_page)
        return self.context, self.booking_page

    async def choosing_menu(self):
        self.context, self.booking_page = await choosing_menu(self.context, self.booking_page)
        return self.context, self.booking_page

    async def form_login(self):
        self.context, self.booking_page = await form_login(self.context, self.booking_page)
        return self.context, self.booking_page

    async def form_not_login(self):
        self.context, self.booking_page = await form_not_login(self.context, self.booking_page)
        return self.context, self.booking_page