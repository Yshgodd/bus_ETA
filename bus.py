import asyncio
import json

from haversine import haversine
from pydantic import BaseModel
import requests


bus_stop = {
    "삼육대학교": (37.643355, 127.105891),
    "삼육대학교정문": (37.639110, 127.107394),
    "태릉선수촌": (37.635569, 127.105783),
    "태릉": (37.630314, 127.098444),
    "서울여대,육군사관학교행정안내소": (37.626089, 127.094542),
    "경춘선숲길,화랑대역공원": (37.623844, 127.090912),
    "화랑대사거리": (37.621590, 127.087371),
    "화랑대역2번출구": (37.620269, 127.083752),
    "태릉입구역1번출구": (37.617402, 127.074554),
    "월릉교": (37.616243, 127.071402),
    "석계역": (37.615082, 127.065971),
    "봉화산역": (37.617201, 127.091748),
    "두산대림아파트": (37.618582, 127.088765),
    "별내역2번출구": (37.642375, 127.126846),
}

# * 원본
# bus_route = {
#     1: [
#         "삼육대학교",
#         "삼육대학교정문",
#         "태릉선수촌",
#         "태릉",
#         "서울여대,육군사관학교행정안내소",
#         "경춘선숲길,화랑대역공원",
#         "화랑대사거리",
#         "두산대림아파트",
#         "봉화산역",
#         "두산대림아파트",
#         "화랑대역2번출구",
#         "화랑대사거리",
#         "경춘선숲길,화랑대역공원",
#         "서울여대,육군사관학교행정안내소",
#         "태릉",
#         "태릉선수촌",
#         "삼육대학교정문",
#         "삼육대학교",
#     ],
#     2: [
#         "삼육대학교",
#         "삼육대학교정문",
#         "태릉선수촌",
#         "태릉",
#         "서울여대,육군사관학교행정안내소",
#         "경춘선숲길,화랑대역공원",
#         "화랑대사거리",
#         "화랑대역2번출구",
#         "태릉입구역1번출구",
#         "월릉교",
#         "석계역",

#     ],
#     3: [
#         "삼육대학교",
#         "삼육대학교정문",
#         "담터교차로,담터고개",
#         "담터입구",
#         "힐스테이트별내역,별내자이더스타",
#         "별내역2번출구",
#     ],
# }

bus_route = {
    1: [
        "삼육대",
        "삼육대 정문",
        "태릉선수촌",
        "태릉",
        "서울여대, 육군사관학교",
        "경춘선숲길",
        "화랑대사거리",
        "두산대림아파트",
        "봉화산역",
        "두산대림아파트",
        "화랑대역",
        "화랑대사거리",
        "경춘선숲길",
        "서울여대, 육군사관학교",
        "태릉",
        "태릉선수촌",
        "삼육대 정문",
        "삼육대",
    ],
    2: [
        "삼육대",
        "삼육대 정문",
        "태릉선수촌",
        "태릉",
        "서울여대, 육군사관학교",
        "경춘선숲길",
        "화랑대사거리",
        "태릉입구역",
        "월릉교",
        "석계역",
        "월릉교",
        "태릉입구역",
        "화랑대사거리",
        "경춘선숲길",
        "서울여대, 육군사관학교",
        "태릉",
        "태릉선수촌",
        "삼육대 정문",
        "삼육대",
    ],
    3: [
        "삼육대학교",
        "삼육대학교정문",
        "담터교차로,담터고개",
        "담터입구",
        "힐스테이트별내역,별내자이더스타",
        "별내역2번출구",
    ],
}

init_route = {
    (1, "삼육대"): "삼육대 정문",
}
# * (status,,from):to
route_from_to = {
    # (None, "삼육대"): "삼육대 정문",
    # ("삼육대", "삼육대 정문"): "태릉선수촌",
    # ("삼육대 정문", "태릉선수촌"): "태릉",
    # ("태릉선수촌", "태릉"): "서울여대, 육군사관학교",
    # ("서울여대, 육군사관학교", "경춘선숲길"): "화랑대사거리",
    # ("경춘선숲길", "화랑대사거리"): "두산대림아파트",
    # ("화랑대사거리", "두산대림아파트"): "봉화산역",
    # ("두산대림아파트", "봉화산역"): "화랑대역",
    # ("봉화산역", "화랑대역"): "화랑대사거리",
    # ("화랑대역", "화랑대사거리"): "경춘선숲길",
    # ("화랑대사거리", "경춘선숲길"): "서울여대, 육군사관학교",
    # ("경춘선숲길", "서울여대, 육군사관학교"): "태릉",
    # ("서울여대, 육군사관학교", "태릉"): "태릉선수촌",
    # ("태릉", "태릉선수촌"): "삼육대 정문",
    # ("태릉선수촌", "삼육대 정문"): "삼육대",
    # ("삼육대 정문", "삼육대"): None,
    (1, 1, "삼육대"): "삼육대 정문",
    (1, 1, "삼육대 정문"): "태릉선수촌",
    (1, 1, "태릉선수촌"): "태릉",
    (1, 1, "태릉"): "서울여대, 육군사관학교",
    (1, 1, "서울여대, 육군사관학교"): "경춘선숲길",
    (1, 1, "경춘선숲길"): "화랑대사거리",
    (1, 1, "화랑대사거리"): "두산대림아파트",
    # *
    (1, 1, "두산대림아파트"): "봉화산역",
    (1, 1, "봉화산역"): "두산대림아파트",
    # *
    (1, 2, "두산대림아파트"): "화랑대역",
    (1, 1, "화랑대역"): "화랑대사거리",
    (1, 2, "화랑대역"): "화랑대사거리",
    (1, 2, "화랑대사거리"): "경춘선숲길",
    (1, 2, "경춘선숲길"): "서울여대, 육군사관학교",
    (1, 2, "서울여대, 육군사관학교"): "태릉",
    (1, 2, "태릉"): "태릉선수촌",
    (1, 2, "태릉선수촌"): "삼육대 정문",
    (1, 2, "삼육대 정문"): "삼육대",
    (1, 2, "삼육대"): None,
    (1, 0, "삼육대"): None,
    (2, 1, "삼육대"): "삼육대 정문",
    (2, 1, "삼육대 정문"): "태릉선수촌",
    (2, 1, "태릉선수촌"): "태릉",
    (2, 1, "태릉"): "서울여대, 육군사관학교",
    (2, 1, "서울여대, 육군사관학교"): "경춘선숲길",
    (2, 1, "경춘선숲길"): "화랑대사거리",
    (2, 1, "화랑대사거리"): "화랑대역",
    (2, 1, "화랑대역"): "태릉입구역",
    (2, 1, "태릉입구역"): "월릉교",
    (2, 1, "월릉교"): "석계역",
    (2, 1, "석계역"): "월릉교",
    (2, 2, "석계역"): "월릉교",
    (2, 2, "월릉교"): "태릉입구역",
    (2, 2, "태릉입구역"): "화랑대역",
    (2, 2, "화랑대역"): "화랑대사거리",
    (2, 2, "화랑대사거리"): "경춘선숲길",
    (2, 2, "경춘선숲길"): "서울여대, 육군사관학교",
    (2, 2, "서울여대, 육군사관학교"): "태릉",
    (2, 2, "태릉"): "태릉선수촌",
    (2, 2, "태릉선수촌"): "삼육대 정문",
    (2, 2, "삼육대 정문"): "삼육대",
    (2, 2, "삼육대"): None,
    (2, 0, "삼육대"): None,
    (3, 1, "삼육대"): "삼육대 정문",
    (3, 1, "삼육대 정문"): "담터교차로,담터고개",
    (3, 1, "담터교차로,담터고개"): "담터입구",
    (3, 1, "담터입구"): "미리내마을입구",
    (3, 1, "미리내마을입구"): "힐스테이트별내역,별내자이더스타",
    (3, 1, "힐스테이트별내역,별내자이더스타"): "별내역2번출구",
    (3, 1, "별내역2번출구"): "힐스테이트별내역,별내자이더스타",
    (3, 2, "별내역2번출구"): "힐스테이트별내역,별내자이더스타",
    (3, 2, "힐스테이트별내역,별내자이더스타"): "미리내마을입구",
    (3, 2, "미리내마을입구"): "담터입구",
    (3, 2, "담터입구"): "담터교차로,담터고개",
    (3, 2, "담터교차로,담터고개"): "삼육대 정문",
    (3, 2, "삼육대 정문"): "삼육대",
    (3, 2, "삼육대"): None,
    (3, 0, "삼육대"): None,
}
# * 한바퀴 돌면 json에서 from을 None으로 초기화


bus_status = {0: "정차", 1: "각목적지행", 2: "삼육대행"}
# REQUEST_URL = "https://talk.syu.ac.kr/bus/status/list"  # 수톡 서버
REQUEST_URL = "http://localhost:1111/converted_bus_info"


def test_func():

    # * 버스 정보 받아오기
    response = requests.get(REQUEST_URL)
    response = response.json()
    # response = {
    #     "returnCode": "200",
    #     "data": [
    #         {
    #             "id": "15231a7ce4ba789d13b722cc5c955834",
    #             "name": "1701",
    #             "lat": "37.64334317237155",
    #             "lon": "127.10595344112824",
    #             "status": "0",
    #             "routeid": 1,
    #             "updatetime": 1725328033895,
    #             "num": "01076370544",
    #             "os": "7.0",
    #             "model": "SM-G925K",
    #             "busstop": {
    #                 "bus_stop": "두산대림아파트",
    #                 "distance": 8.735517950173472,
    #             },
    #         },
    #         {
    #             "id": "b24d516bb65a5a58079f0f3526c87c57",
    #             "name": "1220",
    #             "lat": "37.61687036",
    #             "lon": "127.09374213",
    #             "status": "1",
    #             "routeid": 2,
    #             "updatetime": 1725328696273,
    #             "num": "01027710544",
    #             "os": "12",
    #             "model": "SM-A908N",
    #             "busstop": {"bus_stop": "삼육대", "distance": 8.735517950173472},
    #         },
    #     ],
    # }
    if response["data"] == []:
        return None
    # * 전 데이터랑 같으면 pass  하는 거 만들어야 될듯
    for data in response["data"]:
        if int(data["status"]):
            if data["busstop"]["bus_stop"] == "두산대림아파트":
                with open(f"./json/{data['id']}.json", "r", encoding="utf-8") as file:
                    previous_data = json.load(file)
                    print(previous_data)
                if not previous_data:
                    with open(
                        f"./json/{data['id']}.json", "w", encoding="utf-8"
                    ) as file:
                        json.dump(
                            {
                                "id": data["id"],
                                "route_id": data["routeid"],
                                "from": data["busstop"]["bus_stop"],
                                "to": None,
                                "time": None,
                                "progress": None,
                            },
                            file,
                            ensure_ascii=False,
                            indent=4,
                        )
                else:
                    if previous_data["from"] == "화랑대역":
                        to = route_from_to[
                            (data["routeid"], 1, data["busstop"]["bus_stop"])
                        ]
                    elif previous_data["from"] == "봉화산역":
                        to = route_from_to[
                            (data["routeid"], 2, data["busstop"]["bus_stop"])
                        ]

                    with open(
                        f"./json/{data['id']}.json", "w", encoding="utf-8"
                    ) as file:
                        json.dump(
                            {
                                "id": data["id"],
                                "route_id": data["routeid"],
                                "from": data["busstop"]["bus_stop"],
                                "to": to,
                                "time": None,
                                "progress": None,
                            },
                            file,
                            ensure_ascii=False,
                            indent=4,
                        )

            to = route_from_to[
                (data["routeid"], int(data["status"]), data["busstop"]["bus_stop"])
            ]

            with open(f"./json/{data['id']}.json", "w", encoding="utf-8") as file:
                json.dump(
                    {
                        "id": data["id"],
                        "route_id": data["routeid"],
                        "from": data["busstop"]["bus_stop"],
                        "to": to,
                        "time": None,
                        "progress": None,
                    },
                    file,
                    ensure_ascii=False,
                    indent=4,
                )

    # if previous_data["data"] is None:
    #     with open("./json/test.json", "w", encoding="utf-8") as file:
    #         json.dump(
    #             {"id": None,"route_id": None, "from": None, "to": None, "time": None, "progress": None},
    #             file,
    #             ensure_ascii=False,
    #             indent=4,
    #         )


# * 안쓸듯
def initialize():
    data = {
        """
            bus.json 파일에서 가져온 데이터
        """
        "data": [
            {
                "id": "1220",
                "lat": "37.64333205",
                "lon": "127.10591227",
                "time": "2024-09-02 13:23:50",
            },
            {
                "id": "0101",
                "lat": "37.617402",
                "lon": "127.074554",
                "time": "2024-09-02 13:23:50",
            },
        ]
    }
    bus_info = []
    for values in data["data"]:
        sorted_data = []
        bus_gps = (float(values["lat"]), float(values["lon"]))

        for k, v in bus_stop.items():
            distance = haversine(bus_gps, v, unit="m")
            sorted_data.append({"bus_stop": k, "distance": distance})
        # sorted_data.sort(key=sorted_data["distance"])
        sorted_data.sort(key=lambda x: x["distance"])
        print(sorted_data[0])
        bus_info.append(
            {
                "id": values["id"],
                "from": sorted_data[0]["bus_stop"],
                "to": None,
                "progress": None,
            }
        )
    print(bus_info)


class BusData(BaseModel):
    id: str
    name: str
    lat: str
    lon: str
    status: str
    routeid: int
    # updatetime: int
    # num: str
    # os: str
    # model: str
    busstop: str


class Bus(BaseModel):
    time: str
    returnCode: str
    data: list[BusData]


class SaveBusData(BusData):
    from_: str
    to: str
    progress: str


# REQUEST_URL = "https://bus.syu.kr/api" 상윤스 서버


def bus_stop_converter(bus_stop: str):
    """
    받아온 버스 정류장을 우리가 만든 정류장으로 변환
    """

    return bus_stop


def get_bus_info():
    """
    버스 정보를 가져오는 API
    {
        "time": "2024-09-03 11:34:56",
        "returnCode": "200",
        "data": [
            {
                "id": "15231a7ce4ba789d13b722cc5c955834",
                "name": "1701",
                "lat": "37.64334317237155",
                "lon": "127.10595344112824",
                "status": "0",
                "routeid": 3,
                "updatetime": 1725328033895,
                "num": "01076370544",
                "os": "7.0",
                "model": "SM-G925K",
                "busstop": "삼육대"
            },
            ]
    } # 현재 버스 정보
    """
    # * 다른 서버에서 버스 정보 가져오기
    # response = asyncio.to_thread(requests.get, REQUEST_URL)

    # response = requests.get(REQUEST_URL)
    # * 임시로 가져온 버스 정보
    response = {
        "time": "2024-09-03 11:34:56",
        "returnCode": "200",
        "data": [
            {
                "id": "15231a7ce4ba789d13b722cc5c955834",
                "name": "1701",
                "lat": "37.64334317237155",
                "lon": "127.10595344112824",
                "status": "0",
                "routeid": 3,
                "updatetime": 1725328033895,
                "num": "01076370544",
                "os": "7.0",
                "model": "SM-G925K",
                "busstop": "삼육대",
            },
        ],
    }

    # * 서버에 저장된 최신화 안된 버스의 기록..
    # with open("./json/")
    # print(response.json())
    # if response.status_code != 200:
    #     """
    #         연결 실패시 기존 데이터를 불러옴
    #     """
    #     pass

    # bus_info = Bus.model_validate(response.json())
    bus_info = Bus.model_validate(response)

    bus_info_to_save = SaveBusData()
    print(bus_info)

    if bus_info.data == []:
        return None

    for bus in bus_info.data:
        bus_info_to_save.from_ = bus.busstop
        # if bus.routeid == 1:
        bus_route[f"{bus.routeid}"].index(bus.busstop)
        # bus_info_to_save.to = busstop["봉화산역"]

        """
            #* 첫번째 방법 
            busstop이 가장 최근 지나온 정류장임 -> busstop을 기준으로 from, to를 정함
            
            status 가 1 이면 bus_route 리스트에서 busstop의 인덱스를 찾고 다음 인덱스를 to로 설정
            status 가 2 이면 bus_route 리스트에서 busstop의 인덱스를 찾고 -1번째 인덱스를 to로 설정
            bus는 response 데이터
            
            *status가 1일때 (각목적지행)
            
            bus_route[bus.routeid].index(bus.busstop) # 현재 지나온 정류장의 인덱스
            
            bus_route[bus.routeid].index(bus.busstop) + 1 # 다음 정류장의 인덱스를 to 로 설정
            
            마지막 인덱스면 바로 전 인덱스를 to로 설정
            * status가 2일때 (삼육대행)
            
            bus_route[bus.routeid].index(bus.busstop) # 현재 지나온 정류장의 인덱스
            
            bus_route[bus.routeid].index(bus.busstop) - 1 # 이전 정류장(리스트상의)의 인덱스를 to로 설정
            
            #* 두번째 방법
            
            버스의 좌표와 
            
            
            
             
        """


if __name__ == "__main__":
    # initialize()
    # get_bus_info()
    test_func()


# {
#     "삼육대학교": {"lat": 37.643355, "lon": 127.105891},
#     "삼육대학교정문": {"lat": 37.639110, "lon": 127.107394},
#     "담터교차로,담터고개": {"lat": 37.641819, "lon": 127.113341},
#     "담터입구": {"lat": 37.642119, "lon": 127.115551},
#     "힐스테이트별내역,별내자이더스타": {"lat": 37.642774, "lon": 127.122842},
#     "별내역2번출구": {"lat": 37.642375, "lon": 127.126846},
#     "별내상업지구": {"lat": 37.645550, "lon": 127.125413},
#     "별빛마을3-6단지,별내자이더스타": {"lat": 37.645279, "lon": 127.122546},
#     "미리내마을입구": {"lat": 37.642593, "lon": 127.118478},
# }

# ## 학교 -> 석계 -> 학교
# 삼육대 [37.643355,127.105891] 정류장
# 삼육대 정문 [37.639110,127.107394]
# 태릉 선수촌 [37.635569,127.105783]
# 태릉 [37.630314,127.098444]
# 서울여대,육군사관학교행정안내소 [37.626089,127.094542] 정류장
# 경춘선숲길,화랑대역공원 [37.623844,127.090912] 정류장
# 화랑대사거리 [37.621590,127.087371] 정류장
# 화랑대역2번출구 [37.620269,127.083752] 정류장
# 태릉입구역1번출구 [37.617402,127.074554] 정류장
# 월릉교 [37.616243,127.071402]
# 석계역 [37.615082,127.065971] 정류장

# ## 학교 -> 별내 -> 학교

# 삼육대 [37.643355,127.105891] 정류장
# 삼육대 정문 [37.639110,127.107394]
# 담터교차로,담터고개 [37.641819,127.113341]
# 담터입구 [37.642119,127.115551]
# 힐스테이트별내역,별내자이더스타 [37.642774,127.122842]
# 별내역2번출구 [37.642375,127.126846] 정류장
# 별내상업지구 [37.645550,127.125413]
# 별빛마을3-6단지,별내자이더스타 [37.645279,127.122546]
# 미리내마을입구 [37.642593,127.118478]
# 담터입구 [37.642119,127.115551]
# 담터교차로,담터고개 [37.641819,127.113341]
# 삼육대 정문 [37.639110,127.107394]
# 삼육대 [37.643355,127.105891] 정류장
