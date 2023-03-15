# 글자추출
#이미지 처리 모듈
#OCR 모듈 pip install pytesseract
from PIL import Image
import pytesseract as tess
Img_path = './studyPython/여기어때.png'
tess.pytesseract.tesseract_cmd = 'C:/DEV/Tools/Tesseract-OCR/tesseract.exe'

result = tess.image_to_string(Image.open(Img_path), lang='kor')
print(result)