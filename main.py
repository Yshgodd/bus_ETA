from datetime import datetime
import os
import json
import asyncio

import requests
from fastapi import FastAPI
from pydantic import BaseModel
from haversine import haversine
from collections import defaultdict


bus_pre_stop_dict = defaultdict()

bus_pre_stop_dict["dfjaksjdfklsjdkfjal"] = "dfmaslkdm"

app = FastAPI()
# REQUEST_URL = "https://bus.syu.kr/api"

class Bus(BaseModel):
    data: list
    
    model_config = {
        "json_schema_extra": {
            "examples": [{"data": [
            {
                "1220": {
                    "lat": "37.64333205",
                    "lon": "127.10591227",
                    "time": "2024-09-02 13:10:56"
                }
            },
            {
                "71저1244": {
                    "lat": "37.64333833333333",
                    "lon": "127.10589499999999",
                    "time": "2024-09-02 13:10:56"
                }
            },
            {
                "004": {
                    "lat": "37.6186832",
                    "lon": "127.0783573",
                    "time": "2024-09-02 13:10:56"
                }
            },
            {
                "71저1221": {
                    "lat": "37.64339333333333",
                    "lon": "127.10596",
                    "time": "2024-09-02 13:10:56"
                }
            }
        ]}]
        }
        
    }
    
REQUEST_URL = "https://talk.syu.ac.kr/bus/status/list"
bus_stop = {
    "삼육대": (37.643355, 127.105891),
    "삼육대 정문": (37.639110, 127.107394),
    "태릉선수촌": (37.635569, 127.105783),
    "태릉": (37.630314, 127.098444),
    "서울여대, 육군사관학교": (37.626089, 127.094542),
    "경춘선숲길": (37.623844, 127.090912),
    "화랑대사거리": (37.621590, 127.087371),
    "화랑대역": (37.620269, 127.083752),
    # "태릉입구역": (37.617402, 127.074554),
    "태릉입구역": (37.618194,127.076766),
    "월릉교": (37.616243, 127.071402),
    "석계역": (37.615082, 127.065971),
    "봉화산역": (37.617201, 127.091748),
    "두산대림아파트": (37.618582, 127.088765),
    "담터교차로,담터고개": (37.641819,127.113341),
    "담터입구":(37.642119,127.115551),
    "힐스테이트별내역,별내자이더스타":(37.642774,127.122842),
    "별내역2번출구":(37.642375,127.126846),
    "별내상업지구" :(37.645550,127.125413),
    "별빛마을3-6단지,별내자이더스타": (37.645279,127.122546),
    "미리내마을입구": (37.642593,127.118478),
}

@app.get("/converted_bus_info")
async def get_convert_bus_info():
    print("\nSERVERTIME: ",datetime.now(),"\n")
    response = requests.get(REQUEST_URL)
    response = response.json()
    with open("./json/converted_bus.json", "r", encoding="utf-8") as file:
                converted_bus = json.load(file)
                print("\n",converted_bus,"\n")
    # bus_info = []
    for values in response["data"]:
        sorted_data = []
        bus_gps = (float(values["lat"]), float(values["lon"]))

        for k, v in bus_stop.items():
            distance = haversine(bus_gps, v, unit="m")
            sorted_data.append({"bus_stop": k, "distance": distance})
        # sorted_data.sort(key=sorted_data["distance"])
        sorted_data.sort(key=lambda x: x["distance"])
        print(sorted_data[0])
        # bus_info.append(
        #     {
        #         "id": values["id"],
        #         "from": sorted_data[0]["bus_stop"],
        #         "to": None,
        #         "progress": None,
        #     }
        # )
        if sorted_data[0]["distance"] <= 100:
            values["busstop"] = sorted_data[0]
            
        elif sorted_data[0]["distance"] > 100:
            
            if converted_bus == []:
                values["busstop"] = {"bus_stop": "삼육대", "distance": None}
                print("\n \n line 119")
            else:
                for data in converted_bus["data"]:
                    # values["busstop"] = converted_bus[0]["bus_stop"]
                    if data["id"] == values["id"]:
                        if "busstop" in data:
                            values["busstop"] = data["busstop"]
                            break
                        if "busstop" not in data:
                            # print(values)
                            print("\n busstop not in data\n")
                            values["busstop"] = {"bus_stop": "삼육대", "distance": None}
 
                        
        with open("./json/converted_bus.json", "w", encoding="utf-8") as file:
            json.dump(response, file, ensure_ascii=False,indent=4)
        # values["busstop"] = sorted_data[0]["bus_stop"]
    return response


@app.get("/bus", response_model=Bus)
async def get_bus_info():
    """
        버스 정보를 가져오는 API

            return :
                    {
                        "data": [
                            {
                                "1220": {
                                    "lat": "37.64333205",
                                    "lon": "127.10591227",
                                    "time": "2024-09-02 13:10:56"
                                }
                            },
                            {
                                "71저1244": {
                                    "lat": "37.64333833333333",
                                    "lon": "127.10589499999999",
                                    "time": "2024-09-02 13:10:56"
                                }
                            },
                            {
                                "004": {
                                    "lat": "37.6186832",
                                    "lon": "127.0783573",
                                    "time": "2024-09-02 13:10:56"
                                }
                            },
                            {
                                "71저1221": {
                                    "lat": "37.64339333333333",
                                    "lon": "127.10596",
                                    "time": "2024-09-02 13:10:56"
                                }
                            }
                        ]
                    }
    """
    
    # response = requests.get("https://bus.syu.kr/api")
    response = await asyncio.to_thread(requests.get, REQUEST_URL)
    # print(response.json())
    if response.status_code != 200:
        """ 
            연결 실패시 기존 데이터를 불러옴
        """
        with open("./json/bus.json", "r", encoding="utf-8") as file:
            return json.load(file)
        
        
    total_data = {"data": []}
    time = response.json()["time"]
    result = response.json()["data"]
    print(len(result))
    for f in result:
        json_data = {}
        json_data[f'{f["name"]}'] = {"lat": f["lat"], "lon": f["lon"], "time": time}

        print("\n step", json_data, "\n")

        total_data["data"].append(json_data)
        # print(total_data)

    with open("./json/bus.json", "w", encoding="utf-8") as file:
        json.dump(total_data, file, ensure_ascii=False)

    return total_data


if __name__ == "__main__":
    pass
