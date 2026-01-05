from catchtable_reserve.Authenticator import Authenticator 
from catchtable_reserve.server import Server 
from catchtable_reserve.reservation import macro 
from datetime import datetime
import asyncio

async def main():
    authenticate = Authenticator()
    await authenticate.setting()
    context, _ = await authenticate.kakao_login()
    alpha_macro = macro(context)

    await alpha_macro.booking(
        url="https://app.catchtable.co.kr/ct/shop/perehil",
        date="2026-01-14",
        인원수=2
    )
#####################################################################################
    catchtable = Server('https://app.catchtable.co.kr/')
    target_time_str = '2026-01-06 00:00:00'
    set_time = datetime.strptime(target_time_str, '%Y-%m-%d %H:%M:%S')
    print(f'설정 시간: {set_time}')
    await catchtable.open_session()
    while True:
        server_time_str, ping = await catchtable.get_server_time()
        server_time_kst = catchtable.translate_to_kst(server_time_str)
        
        print(f'현재 서버 시간 (KST): {server_time_kst}', end='\t')
        print(f'핑: {ping}')
        
        if set_time <= server_time_kst:
            print('Target time reached!')
            await catchtable.close_session()
            break
        
        await asyncio.sleep(0.1)
#####################################################################################

    tasks = [
        alpha_macro.booking_loop(
            wanted_times=['오후 6:00', '오후 6:30', '오후 7:00', '오후 7:30', '오후 8:00', '오후 8:30']
        )
    ]
    await asyncio.gather(*tasks)
    await context.tracing.stop(path='pathlog/trace.zip')
    await asyncio.sleep(50000)

if __name__ == "__main__":
    asyncio.run(main())