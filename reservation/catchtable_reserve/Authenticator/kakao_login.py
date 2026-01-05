import os

async def kakao_login(context, login_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    key_file = os.path.join(current_dir, 'kakao.key')
    with open(key_file, "r") as f:
        id = f.readline().strip()
        password = f.readline().strip()

    login_page = await context.new_page()
    await login_page.goto(login_url)
    async with context.expect_page() as new_page_info:
        await login_page.locator('button._1634eg81', has_text='카카오').click(modifiers=["Control"])
    kakao_page = await new_page_info.value
    await kakao_page.locator('#loginId--1').fill(id)
    await kakao_page.locator('#password--2').fill(password)
    await kakao_page.locator('button.btn_g.highlight.submit').click()
    await kakao_page.wait_for_event('close')
    return context, login_page