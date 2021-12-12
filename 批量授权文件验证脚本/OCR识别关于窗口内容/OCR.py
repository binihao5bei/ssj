import  pytesseract
from PIL import Image
im=Image.open('/home/ssj/Desktop/1.png')
text=pytesseract.image_to_string(im,lang='chi_sim')
print("OCR识别关于窗口内容为：{}".format(text))
print("*"*50)


licend_info="".join(text.split("\n")[8]).split(";")[0].split(":")

deactive_date="".join(text.split("\n")[8]).split(";")[2].replace("到期",'')
print("授权对象：{}".format(licend_info[1]))
print("授权到期时间：{}".format(deactive_date))