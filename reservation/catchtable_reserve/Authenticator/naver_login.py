import os

async def naver_login(context, login_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(current_dir, 'naver.key')
    with open(key_file, "r") as f:
        id = f.readline().strip()
        password = f.readline().strip()

    login_page = await context.new_page()
    await login_page.goto(login_url)
    async with context.expect_page() as new_page_info:
        await login_page.locator('button._1w07br43', has_text='네이버').click(modifiers=["Control"])
    naver_page = await new_page_info.value
    await naver_page.locator('#id').fill(id)
    await naver_page.locator('#pw').fill(password)
    await naver_page.locator('div.btn_login_wrap > button.btn_login').click()
    await naver_page.wait_for_event('close')
    return context, login_page