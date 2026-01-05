from datetime import datetime, timedelta

def translate_to_kst(server_time_str: str) -> datetime:
    server_time_kst = datetime.strptime(server_time_str, '%a, %d %b %Y %H:%M:%S %Z')
    return server_time_kst + timedelta(hours=9)  # GMT -> KST (9시간 차이)


if __name__ == "__main__":
    server_time_kst = translate_to_kst('Sat, 12 Oct 2024 14:12:42 GMT')
    print("서버 시간:", server_time_kst)