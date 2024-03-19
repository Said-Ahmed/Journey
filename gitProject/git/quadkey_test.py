import math


def get_quadkey(lat, lng, zoom):
    x = int((lng + 180) / 360 * (1 << zoom))
    y = int(
        (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * (1 << zoom))
    quadkey = ''
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (x & mask) != 0:
            digit += 1
        if (y & mask) != 0:
            digit += 2
        quadkey += str(digit)
    return quadkey


def decimal_to_quad(decimal_value):
    if decimal_value == 0:
        return "0"
    quadkey = ""
    while decimal_value > 0:
        remainder = decimal_value % 4
        quadkey = str(remainder) + quadkey
        decimal_value = decimal_value // 4
    return quadkey


zoom = 23
while get_quadkey(43.47745087732927, 46.20942156652026, zoom=zoom) != get_quadkey(43.10005791032384, 47.2426249970712, zoom=zoom):
    zoom -= 1
    print(zoom)

print(get_quadkey(43.47745087732927, 46.20942156652026, zoom=7))
print(get_quadkey(43.10005791032384, 47.2426249970712, zoom=23))
print(get_quadkey(43.47745087732927, 46.20942156652026, zoom=23))
s = '123456'
print(s[:4])

# before = get_quadkey(42.9856817748056, 47.46067883577439, zoom=zoom)
# d = int(before, 4)
# print(d)
#
# print(decimal_to_quad(d) == before)
# print(type(decimal_to_quad(d)))
#
# print(int(get_quadkey(43.00895605135495, 47.44741009028134, 15), 4))
# print(int(get_quadkey(43.00664953038377, 47.4495497578743, 13), 4))