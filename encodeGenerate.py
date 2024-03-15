import cv2 as cv
import os
import face_recognition
import pickle

folderpath='/home/hacker/Desktop/pro/static/css/images'
pathlist=os.listdir(folderpath)
imglist=[]
ids=[]
for path in pathlist:
    imglist.append(cv.imread(os.path.join(folderpath,path)))

    ids.append(path.split(".")[0])

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)
        encodeList.append(encode)

    return encodeList

print("Encoding Started....")
encodeListKnown = findEncodings(imglist)
encodeListKnownWithIds = [encodeListKnown,ids]
print(encodeListKnownWithIds)
print("Encoding complete")

file = open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file)
file.close()
print("File Saved")

