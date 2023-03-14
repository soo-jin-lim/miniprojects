#TTS (Text to Speech)
# pip install gTTS
#pip install playsound 
from gtts import gTTS
from playsound import playsound

text = '안녕하세요, 임입니다.'

tts = gTTS(text=text, lang='ko')
tts.save('./studyPython/output/hi.mp3')
print('생성완료!')
playsound('./studyPython/output/hi.mp3')
print('음성출력완료!')