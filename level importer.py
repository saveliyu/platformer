from PIL import Image

im = Image.open("graphics/temp/level3.png")
pixels = im.load()  # список с пикселями
x, y = im.size  # ширина (x) и высота (y) изображения
res = []
for i in range(y):
    temp = ""
    for j in range(x):
        r, g, b, s = pixels[j, i]
        if [r, g, b] == [0, 0, 255]:
            temp += "X"
        elif [r, g, b] == [255, 150, 40]:
            temp += 'T'
        elif [r, g, b] == [100, 100, 100]:
            temp += 'L'
        elif [r, g, b] == [255, 0, 255]:
            temp += 'P'
        else:
            temp += " "
    res.append(temp)

with open('levels.py', 'w') as f:
    for line in res:
        f.write('"' + str(line) + '"' + ',\n')