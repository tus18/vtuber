from operator import truediv
import cv2 as cv
from msvcrt import getch
import numpy as np
from PIL import Image
import os
import glob

face_cascade = cv.CascadeClassifier('./haarcascade_frontalface_default.xml')

def Get_Bounding_Box(img_path):
    img_b = cv.imread(img_path)
    if img_b is None:
        print("No Object")
        return -1
    gray = cv.cvtColor(img_b,cv.COLOR_BGR2GRAY)
    face = face_cascade.detectMultiScale(gray, 1.3, 5)
    bbox = []
    for x, y, w, h in face:
        bbox.append([x,y,x+w,y+h])
    print(face)
    #バウンディングボックス座標データを返却
    return bbox

def Cut_draw(img_path, bbox_Coordinate, img_number, select_name):
    #画像読み込み
    #RGBモードとしてやる RGBAモードだと上手く行かない
    img = Image.open(img_path).convert("RGB")
    #画像を切り取る
    #座標を格納する箱
    item_position_list = []
    #座標を一個ずつ読み取る
    for item_position in bbox_Coordinate:
        for item_coordinate in item_position:
            item_position_list.append(item_coordinate)
        #取得した座標のところだけを抜き取る
        img_crop = img.crop(item_position_list)
        img_crop.convert("RGB")
        #画像出力
        img_crop.save("./" + select_name + "/" + "/cut_image_drink{0}.jpg".format(img_number))
        #座標リストを空にする
        item_position_list.clear()

#使用する画像のパスを指定する
select_folder = input("フォルダを指定してください:./")
select_name = input("保存先を指定してください:./")
img_path = "./" +select_folder+ "/" + "/*.jpg"
    #１つずつ画像パスを読み取る
img_jpg = glob.glob(img_path)
    #画像番号
img_number = 1
    #切り取った画像を保存するフォルダーを作成
os.makedirs("./" + select_name + "/", exist_ok=True)
    #画像を１つずつ処理する
for img in img_jpg:
        #バウンディングボックスの座標データを取得&格納
    bbox_Coordinate = Get_Bounding_Box(img)
    if type(bbox_Coordinate) is not int:
            #画像の抜き取り
        Cut_draw(img, bbox_Coordinate, img_number,select_name)
        img_number += 1
