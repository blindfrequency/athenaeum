class SimpleNumbers:
    def __init__(self,parent=None):
        from PySide2.QtMultimedia import QMediaPlayer
        self.m = QMediaPlayer()

    def numberToText(self,number=1):
        from num2words import num2words
        return num2words(number, lang='ru')

    def voiceText(self, text=''):
        from gtts import gTTS
        tts = gTTS(text=text, lang='ru')
        tts.save('/home/constcut/localFile.mp3') #TODO better file
        from PySide2.QtCore import QUrl
        self.m.setMedia(QUrl.fromLocalFile("/home/constcut/localFile.mp3"))
        self.m.setVolume(100)
        self.m.play()
