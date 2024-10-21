# The Python standard library includes some functionality for communicating
# over the Internet.
# However, we will use a more powerful and simpler library called requests.
# This is external library that you may need to install first.
import requests

import requests
import json  # 用于解析 JSON 数据

def get_data():
    # 从 USGS 地震数据 API 获取地震信息
    response = requests.get(
        "http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
        params={
            'starttime': "2000-01-01",
            "maxlatitude": "58.723",
            "minlatitude": "50.008",
            "maxlongitude": "1.67",
            "minlongitude": "-9.756",
            "minmagnitude": "1",
            "endtime": "2018-10-11",
            "orderby": "time-asc"
        }
    )

    # 将返回的内容转为 JSON 对象
    data = response.json()
    return data

def count_earthquakes(data):
    """获取响应中的地震总数"""
    return len(data['features'])

def get_magnitude(earthquake):
    """获取单个地震事件的震级"""
    return earthquake['properties']['mag']

def get_location(earthquake):
    """获取单个地震事件的经纬度"""
    # 这里返回的是经度和纬度
    return earthquake['geometry']['coordinates'][:2]

def get_maximum(data):
    """找到数据中所有最强的地震事件，返回这些事件的震级和位置"""
    
    # 先找到最大的震级
    max_magnitude = max(get_magnitude(eq) for eq in data['features'])
    
    # 找到所有震级等于最大震级的地震事件
    max_earthquakes = [
        eq for eq in data['features'] if get_magnitude(eq) == max_magnitude
    ]
    
    # 获取这些地震的位置信息
    max_locations = [get_location(eq) for eq in max_earthquakes]
    
    return max_magnitude, max_locations



# 现在可以调用上面的函数并得到结果
data = get_data()
print(f"Loaded {count_earthquakes(data)} earthquakes.")
max_magnitude, max_location = get_maximum(data)
print(f"The strongest earthquake was at {max_location} with magnitude {max_magnitude}.")
