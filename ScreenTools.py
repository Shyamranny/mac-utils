from subprocess import call
import tempfile
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import wx
import requests 

URL = "https://translateapi.howtofixthis.com/"

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

    def set_decoded_text(self, txt):
        self.text_ctrl.SetValue(txt)

    def set_translated_text(self, txt):
        self.text_ctrl_translated.SetValue(txt)

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

    def set_decoded_text(self, txt):
        self.frame.set_decoded_text(txt)

    def set_translated_text(self, txt):
        self.frame.set_translated_text(txt)

if __name__ == '__main__':

    temp = tempfile.NamedTemporaryFile()

    try:
        call(["screencapture", "-i", temp.name])
        decoded_text = pytesseract.image_to_string(Image.open(temp.name))
        
        app = App()
        app.set_decoded_text(decoded_text)
        

        PARAMS = {
            'sourceLanguage':'en',
            'targetLanguage':'ml',
            'text':decoded_text
        } 

        r = requests.get(url = URL, params = PARAMS) 
        data = r.json() 
        
        app.set_translated_text(data['translateText'])

        app.MainLoop()

    finally:
        temp.close()


    





