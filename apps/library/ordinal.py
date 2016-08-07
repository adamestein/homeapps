def ordinal(number):
    return "%d%s" % (number, "tsnrhtdd"[(number / 10 % 10 != 1)*(number % 10 < 4)*number % 10::4])
