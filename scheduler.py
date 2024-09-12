import time
from datetime import datetime, timezone, timedelta
import json

from fastapi import Depends
from apscheduler.schedulers.background import BackgroundScheduler
import requests

import bus

# while True:

#     print(f"[{datetime.now()}]: 버스 정보를 가져옵니다.")
#     response = requests.get("https://bus.syu.kr/api")

#     with open("./json/schedule.json", "r", encoding="utf-8") as file:
#         json_data = json.load(file)

#         json_data["data"].append(response.json())
#         print(json_data)

#     with open("./json/schedule.json", "w", encoding="utf-8") as file:
#         json.dump(json_data, file, ensure_ascii=False, indent=4)

#     time.sleep(20)

# schedule.every(10).seconds.do(job)


def scheduler():
    while True:

        # print(f"[{datetime.now()}]: 버스 정보를 가져옵니다.")
        # response = requests.get("https://bus.syu.kr/api")
        # if response.status_code != 200:
        #     print("연결 실패")
        #     continue

        # with open("./json/schedule.json", "r", encoding="utf-8") as file:
        #     json_data = json.load(file)
        #     bus_info = response.json()
        #     bus_info["server_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     json_data["data"].append(bus_info)

        #     if datetime.now() - datetime.strptime(
        #         json_data["data"][0]["server_time"], "%Y-%m-%d %H:%M:%S"
        #     ) > timedelta(hours=2):
        #         with open("./json/schedule.json", "w", encoding="utf-8") as file:
        #             json.dump(json_data, file, ensure_ascii=False, indent=4)

        #         print("\n2시간이 지나 종료합니다.\n")
        #         break

        # with open("./json/schedule.json", "w", encoding="utf-8") as file:
        #     json.dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"[{datetime.now()}]: 버스 정보를 가져옵니다.")
        bus.test_func()
        print(f"[{datetime.now()}]: 버스 정보를 가져왔습니다 40초 후 갱신.")

        time.sleep(20)


# schedule = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
# # schedule.add_job(craw_scheduler, 'interval', days=1)
# schedule.add_job(craw_scheduler, "cron", hour=0, minute=00)
# schedule.start()
# -----


# schedule = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
# # schedule.add_job(craw_scheduler, 'interval', days=1)
# schedule.add_job(scheduler, "cron", hour=23, minute=15)
# schedule.start()


if __name__ == "__main__":
    scheduler()
