from subprocess import call
import tempfile
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import wx
import requests 

# url for translation
URL = "https://translateapi.howtofixthis.com/"

# GUI frame to be shown to the user
class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Screen Tool')

        panel = wx.Panel(self)     
        panel.SetFocus()
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)

        my_sizer = wx.BoxSizer(wx.VERTICAL)        
        self.text_ctrl = wx.TextCtrl(panel,size = (200,100),style = wx.TE_MULTILINE) 
        self.text_ctrl_translated = wx.TextCtrl(panel,size = (200,100),style = wx.TE_MULTILINE) 
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5)
        my_sizer.Add(self.text_ctrl_translated, 0, wx.ALL | wx.EXPAND, 5)  

        panel.SetSizer(my_sizer)
        self.Show()

    # set decoded text
    def setDecodedText(self, txt):
        self.text_ctrl.SetValue(txt)

    # set translated text
    def setTranslatedText(self, txt):
        self.text_ctrl_translated.SetValue(txt)

    # key up hanlder - to close the window when user clicks escape key
    def OnKeyUP(self, event):
        keyCode = event.GetKeyCode()
        if keyCode == wx.WXK_ESCAPE:
            self.Close()
        event.Skip() 

class App(wx.App):
    """Application class."""

    def OnInit(self):
        self.frame = MyFrame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        self.frame.SetFocus()
        return True

    def setDecodedText(self, txt):
        self.frame.setDecodedText(txt)

    def setTranslatedText(self, txt):
        self.frame.setTranslatedText(txt)

if __name__ == '__main__':

    # create a temp file to store the screen shot
    temp = tempfile.NamedTemporaryFile()

    try:
        # mac command to get a screen shot and save to a file
        call(["screencapture", "-i", temp.name])

        # OCR
        decoded_text = pytesseract.image_to_string(Image.open(temp.name))
        
        # open app and set the decoded text
        app = App()
        app.setDecodedText(decoded_text)

        # params for translation query
        PARAMS = {
            'sourceLanguage':'en',
            'targetLanguage':'ml',
            'text':decoded_text
        } 

        # get translated text
        r = requests.get(url = URL, params = PARAMS) 
        data = r.json() 
        
        # set translated text to the GUI
        app.setTranslatedText(data['translateText'])

        #show the app
        app.MainLoop()

    finally:
        temp.close()
