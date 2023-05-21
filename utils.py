def compare_pixels(image_1, image_2):
    im1 = image_1.load()
    im2 = image_2.load()
    i = 0
    k=0

    x1,y1 = image_1.size
    for x in range(0,x1):
        for y in range(0,y1):
          if im1[x,y] != im2[x,y]:
            i +=1
          else:
              k+=1
    print(f"Количество разных пикселей: {i}")
    print(f"Количество одинаковых пикселей: {k}")
    #Если разница превышает 10% - картинки разные
    if i> (i+k)*0.1:
        return False
    else:
        return True
