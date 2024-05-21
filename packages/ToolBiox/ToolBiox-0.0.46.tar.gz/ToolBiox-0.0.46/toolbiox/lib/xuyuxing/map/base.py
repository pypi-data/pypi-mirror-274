from math import radians, sin, cos, sqrt, atan2


def float_equal(a, b, precision=2):
    return round(a, precision) == round(b, precision)


def haversine(coord1, coord2):
    R = 6371.0  # 地球半径，单位为公里

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # 将坐标转换为弧度
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # 计算距离
    distance = R * c
    return distance


def coord_DMS2DD(degrees, minutes, seconds):
    """
    DMS: Degrees, Minutes, Seconds
    DD: Decimal Degrees
    """
    return degrees + minutes / 60 + seconds / 3600


def coord_DD2DMS(decimal):
    degrees = int(decimal)
    minutes = int((decimal - degrees) * 60)
    seconds = (decimal - degrees - minutes / 60) * 3600
    return degrees, minutes, seconds
