from datetime import datetime
import asyncio

async def booking(context, url: str, date: str, 인원수: int):
    booking_page = await context.new_page()
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%y%m%d")
    updated_url = f"{url}?personCount={인원수}&date={formatted_date}"
    await booking_page.goto(updated_url)
    return context, booking_page


async def click_reservation_button(context, booking_page):
    await booking_page.locator("div._1i69xxc5:has-text('예약하기')").click()
    # drawer 팝업이 열릴 때까지 대기
    await booking_page.locator(".drawer-box-body").wait_for(state='visible', timeout=10000)
    return context, booking_page

async def select_time_slot(context, booking_page, wanted_times):

    try:
        # drawer 팝업 안의 시간대 선택 영역의 클릭 가능한 버튼만 선택
        available_slots_selector = ".drawer-box-body button._18d7pgp0[style*='cursor: pointer']"
        available_time_elements = booking_page.locator(available_slots_selector)
        await available_time_elements.first.wait_for(state='visible', timeout=10000)
        available_count = await available_time_elements.count()
        print(f"Available count: {available_count}")

        available_times = {}
        target_element = None
        for i in range(available_count):
            element = available_time_elements.nth(i)
            elem_text = await element.inner_text()
            available_times[elem_text] = element
            if elem_text in wanted_times:
                target_element = element
                break

        for elem_text in available_times:
            print(f"남은 시간대: - {elem_text}")
        
        if target_element is not None:
            target_text = await target_element.inner_text()
            print(f"원하는 시간대 '{target_text}'를 클릭했습니다.")
            # 화면에 보이도록 스크롤 후 클릭
            await target_element.scroll_into_view_if_needed()
            await target_element.click()
        elif await available_time_elements.count()>0:
            first_elem = available_time_elements.first
            first_text = await first_elem.inner_text()
            # 화면에 보이도록 스크롤 후 클릭
            await first_elem.scroll_into_view_if_needed()
            await first_elem.click()
            print(f"첫 번째 가능한 시간대 '{first_text}'를 클릭했습니다.")
    except Exception as e:
        if await booking_page.get_by_text("저녁 시간대 빈자리 알림 신청 마감").is_visible():
                raise Exception("빈자리 알림 신청 마감되었습니다.")
        elif await booking_page.get_by_text("온라인 예약을 받지 않는 날이에요").is_visible():
                raise Exception("온라인 예약을 받지 않는 날입니다.")
        elif await booking_page.get_by_text("휴무일입니다.").is_visible():
                raise Exception("휴무일입니다.")
        elif await booking_page.get_by_text("예약 오픈 전이에요").is_visible():
                raise Exception("예약 오픈 전입니다.")
        elif await booking_page.get_by_text("예약 가능한 기간이 아니에요.").is_visible():
                raise Exception("예약 가능한 기간이 아닙니다.")
        elif await booking_page.get_by_text("예약이 모두 마감되었습니다.").is_visible():
                raise Exception("예약이 모두 마감되었습니다.")
        else:
            raise Exception(f"시간대 선택 중 오류 발생: {e}")

    return context, booking_page

async def choosing_table(context, booking_page):
    try:
        drawer_title = await booking_page.locator('h2.drawer-box-title').text_content()

        if drawer_title == "메뉴 선택":
            print("좌석옵션을 선택할 수 없습니다.")
            return context, booking_page
        좌석 = booking_page.locator('label:has(input[type="radio"][name="seat"]:not([disabled]))').first
        await 좌석.click()
        print("좌석 선택을 완료했습니다.")
        await  booking_page.locator('button.btn.btn-lg.btn-outline.btn-red').click()
        print("테이블 선택을 완료했습니다.")

    except Exception as e:
        raise Exception(f"테이블 요소를 찾지 못했습니다. 에러 발생: {e}")

    return context, booking_page


async def choosing_menu(context, booking_page):
    try:
        await asyncio.gather(
            booking_page.locator('h2.drawer-box-title', has_text="메뉴 선택").wait_for(state='visible'),
            booking_page.locator('.btn-group').wait_for(state='visible')
        )

        if await booking_page.locator('button.btn.btn-lg.btn-red').is_enabled():
            await booking_page.locator('button.btn.btn-lg.btn-red').click()
            print("예약을 찜했습니다.")
            return context, booking_page

        await booking_page.locator('input[type="checkbox"].form-checkbox').first.check()
        await booking_page.locator('button.btn.btn-lg.btn-red').click()
        print("예약을 찜했습니다.")

    except Exception as e:
        print(f"메뉴 선택을 찾지 못했습니다. 에러 발생: {e}")

    return context, booking_page


async def form_login(context, booking_page):
    await booking_page.wait_for_url('https://app.catchtable.co.kr/ct/reservation/form')
    try:
        await booking_page.get_by_role('button', name='친목').click()
        print('방문목적 선택')
    except Exception as e:
        print(f"방문목적 선택 중 오류 발생: {e}")
    # await booking_page.get_by_role('checkbox').check()
    # await booking_page.locator('input.c2yywn4').check()
    return context, booking_page

async def form_not_login(context, booking_page):
    try:
        visit_purpose_button = booking_page.locator("//button[text()='데이트']")
        await visit_purpose_button.wait_for(state='visible')
        await visit_purpose_button.click()
        print('방문목적 선택')
    except Exception as e:
        print(f"방문목적 선택 중 오류 발생: {e}")
    
    return context, booking_page
