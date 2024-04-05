import urllib.request
import scipy.fftpack
from matplotlib import pyplot as plt


def furn(data):
    yf = scipy.fftpack.fft(data)
    an = []
    for i in range(len(yf)):
        x = abs(yf[i])
        if "e" in str(x):
            x = 0.0
        an.append(round(x))
    an[0] = 0
    return an[:len(an) // 2]


def processing(data):
    result = {}
    length = len(data)
    result["as"] = furn(data)
    result["average"] = round(sum(data) / length, 3)
    sorted_l = sorted(data)
    if length % 2 == 0:
        result["median"] = (sorted_l[length // 2 - 1] + sorted_l[length // 2]) // 2
    else:
        result["median"] = (sorted_l[length // 2])
    result["min_value"] = min(data)
    result["max_value"] = max(data)
    x = 0
    for i in data:
        x += (i-result["average"]) ** 2
    x = (x/len(data)) ** 0.5
    result["sko"] = round(x, 3)
    result["dB"] = round(result["average"] / 26, 3)
    return result


def main():
    n = input()
    esp_addr = "http://192.168.2."+n
    while True:
        page = urllib.request.urlopen("http://192.168.2.1")
        data = str(page.read())
        page = urllib.request.urlopen(esp_addr)
        data2 = str(page.read())

        if len(data) > 10:
            data = data[2:-1]
            data = list(map(int, data.split()))
            urllib.request.urlopen("http://192.168.2.1/1")
            result = processing(data)
            x = range(len(result["as"]))
            y = result["as"]
            plt.plot(x, y)
            plt.title("micro1")
            print("micro1")
            print("=" * 15)
            for i in result.keys():
                if i != "as":
                    print(f"{i}: {result[i]}")
            print("=" * 15)
            plt.show()

        if len(data2) > 10:
            data2 = data2[2:-1]
            data2 = list(map(int, data2.split()))
            urllib.request.urlopen(esp_addr+"/1")
            result2 = processing(data2)
            x = range(len(result2["as"]))
            y = result2["as"]
            plt.plot(x, y)
            plt.title("micro2")
            print("micro2")
            print("=" * 15)
            for i in result2.keys():
                if i != "as":
                    print(f"{i}: {result2[i]}")
            print("=" * 15)
            plt.show()
        n = int(input(": "))
        if n == 0:
            break
        page = urllib.request.urlopen("http://192.168.2.1/2")
        page = urllib.request.urlopen(esp_addr+"/2")


main()
