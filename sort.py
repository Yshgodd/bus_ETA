import json
import time

with open("./json/schedule.json", "r", encoding="utf-8") as file:
    json_data = json.load(file)

num_1220_data = []
num_1244_data = []
num_1_data = []
num_8517_data = []
num_004_data = []
num_1221_data = []
num_1701_data = []
for bus_data in json_data["data"]:
    for data in bus_data["data"]:
        if data["name"] == "1220":
            if num_1220_data == []:
                num_1220_data.append(data)
            else:
                for info in num_1220_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_1220_data.append(data)
        elif data["name"] == "71저1244":
            if num_1244_data == []:
                num_1244_data.append(data)
            else:
                for info in num_1244_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_1244_data.append(data)

        elif data["name"] == "1":
            if num_1_data == []:
                num_1_data.append(data)
            else:
                for info in num_1_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_1_data.append(data)

        elif data["name"] == "70라8517":
            if num_8517_data == []:
                num_8517_data.append(data)
            else:
                for info in num_8517_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_8517_data.append(data)
        elif data["name"] == "004":
            if num_004_data == []:
                num_004_data.append(data)
            else:
                for info in num_004_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_004_data.append(data)

        elif data["name"] == "71저1221":
            if num_1221_data == []:
                num_1221_data.append(data)
            else:
                for info in num_1221_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_1221_data.append(data)
        elif data["name"] == "1701":
            if num_1701_data == []:
                num_1701_data.append(data)
            else:
                for info in num_1701_data:
                    is_same = False
                    if (
                        info["busstop"] == data["busstop"]
                        and info["status"] == data["status"]
                        and info["routeid"] == data["routeid"]
                    ):
                        is_same = True
                        break
                if not is_same:
                    num_1701_data.append(data)

with open("./json/1220.json", "w", encoding="utf-8") as file:
    json.dump(num_1220_data, file, ensure_ascii=False, indent=4)

with open("./json/1244.json", "w", encoding="utf-8") as file:
    json.dump(num_1244_data, file, ensure_ascii=False, indent=4)

with open("./json/1.json", "w", encoding="utf-8") as file:
    json.dump(num_1_data, file, ensure_ascii=False, indent=4)

with open("./json/8517.json", "w", encoding="utf-8") as file:
    json.dump(num_8517_data, file, ensure_ascii=False, indent=4)

with open("./json/004.json", "w", encoding="utf-8") as file:
    json.dump(num_004_data, file, ensure_ascii=False, indent=4)

with open("./json/1221.json", "w", encoding="utf-8") as file:
    json.dump(num_1221_data, file, ensure_ascii=False, indent=4)

with open("./json/1701.json", "w", encoding="utf-8") as file:
    json.dump(num_1701_data, file, ensure_ascii=False, indent=4)
