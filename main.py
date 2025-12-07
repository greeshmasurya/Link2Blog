import wx
import wx.html
import threading
import markdown
import transcript
import ai
import storage
import os

class ConverterPanel(wx.ScrolledWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.SetScrollbars(20, 20, 50, 50)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        sb_inp = wx.StaticBoxSizer(wx.VERTICAL, self, "1. Input Video")
        row1 = wx.BoxSizer(wx.HORIZONTAL)
        self.url = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.url.Bind(wx.EVT_TEXT, self.OnText)
        self.btn_fetch = wx.Button(self, label="Fetch Transcript", size=(140, -1))
        self.btn_fetch.Disable()
        self.btn_fetch.Bind(wx.EVT_BUTTON, self.OnFetch)
        row1.Add(self.url, 1, wx.EXPAND | wx.RIGHT, 10)
        row1.Add(self.btn_fetch, 0)
        sb_inp.Add(row1, 0, wx.EXPAND | wx.ALL, 10)
        self.lbl_err = wx.StaticText(self, label="")
        self.lbl_err.SetForegroundColour(wx.RED)
        sb_inp.Add(self.lbl_err, 0, wx.LEFT | wx.BOTTOM, 10)
        sizer.Add(sb_inp, 0, wx.EXPAND | wx.ALL, 15)

        self.cp = wx.CollapsiblePane(self, label="2. Transcript Preview")
        self.cp.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, self.OnPane)
        pane = self.cp.GetPane()
        psizer = wx.BoxSizer(wx.VERTICAL)
        self.txt_trans = wx.TextCtrl(pane, style=wx.TE_MULTILINE|wx.TE_READONLY, size=(-1, 200))
        self.txt_trans.SetFont(wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        psizer.Add(self.txt_trans, 1, wx.EXPAND | wx.ALL, 5)
        pane.SetSizer(psizer)
        sizer.Add(self.cp, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        sb_gen = wx.StaticBoxSizer(wx.VERTICAL, self, "3. Generate Blog")
        row2 = wx.BoxSizer(wx.HORIZONTAL)
        row2.Add(wx.StaticText(self, label="Style:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.combo = wx.ComboBox(self, choices=["Professional", "Casual", "Educational", "Story Mode"], style=wx.CB_READONLY, size=(150, -1))
        self.combo.SetSelection(0)
        row2.Add(self.combo, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)
        self.btn_gen = wx.Button(self, label="Generate", size=(140, 40))
        self.btn_gen.SetFont(self.btn_gen.GetFont().Bold())
        self.btn_gen.Bind(wx.EVT_BUTTON, self.OnGen)
        self.btn_gen.Disable()
        row2.Add(self.btn_gen, 0)
        sb_gen.Add(row2, 0, wx.EXPAND | wx.ALL, 15)
        self.gauge = wx.Gauge(self, range=100, size=(-1, 8))
        self.gauge.Hide()
        sb_gen.Add(self.gauge, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)
        sizer.Add(sb_gen, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        sb_out = wx.StaticBoxSizer(wx.VERTICAL, self, "4. Final Blog Post")
        self.html = wx.html.HtmlWindow(self, size=(-1, 300))
        sb_out.Add(self.html, 1, wx.EXPAND | wx.ALL, 10)
        row3 = wx.BoxSizer(wx.HORIZONTAL)
        btn_copy = wx.Button(self, label="Copy")
        btn_copy.Bind(wx.EVT_BUTTON, self.OnCopy)
        btn_save = wx.Button(self, label="Save")
        btn_save.Bind(wx.EVT_BUTTON, self.OnSave)
        row3.Add(btn_copy, 0, wx.RIGHT, 10)
        row3.Add(btn_save, 0)
        sb_out.Add(row3, 0, wx.ALIGN_RIGHT | wx.ALL, 10)
        sizer.Add(sb_out, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        self.SetSizer(sizer)
        self.data_trans = None
        self.data_blog = None

    def OnText(self, e):
        self.btn_fetch.Enable(bool(self.url.GetValue().strip()))
        self.lbl_err.SetLabel("")

    def OnFetch(self, e):
        url = self.url.GetValue().strip()
        self.GetParent().GetParent().SetStatusText("Fetching...")
        self.btn_fetch.Disable()
        threading.Thread(target=self.RunFetch, args=(url,), daemon=True).start()

    def RunFetch(self, url):
        try:
            val = transcript.fetch_transcript(url)
            wx.CallAfter(self.EndFetch, val, None)
        except Exception as e:
            wx.CallAfter(self.EndFetch, None, str(e))

    def EndFetch(self, val, err):
        self.btn_fetch.Enable()
        if val:
            self.data_trans = val
            self.txt_trans.SetValue(val)
            self.cp.Expand()
            self.btn_gen.Enable()
            self.GetParent().GetParent().SetStatusText("Fetched.")
            self.Reflow()
        else:
            self.lbl_err.SetLabel(f"Error: {err}")
            wx.MessageBox(err, "Error", wx.OK | wx.ICON_ERROR)

    def OnGen(self, e):
        if not self.data_trans: return
        self.btn_gen.Disable()
        self.gauge.Show()
        self.gauge.Pulse()
        self.Reflow()
        threading.Thread(target=self.RunGen, args=(self.data_trans, self.combo.GetValue()), daemon=True).start()

    def RunGen(self, txt, sty):
        try:
            val = ai.generate_blog(txt, sty)
            wx.CallAfter(self.EndGen, val, None)
        except Exception as e:
            wx.CallAfter(self.EndGen, None, str(e))

    def EndGen(self, val, err):
        self.gauge.Hide()
        self.btn_gen.Enable()
        if val:
            self.data_blog = val
            h = markdown.markdown(val)
            s = "body{font-family:'Segoe UI',sans-serif;font-size:11pt;color:#333}h1{color:#2c3e50}h2{color:#34495e;border-bottom:1px solid #ddd}li{margin-bottom:5px}"
            self.html.SetPage(f"<html><style>{s}</style><body>{h}</body></html>")
            self.GetParent().GetParent().SetStatusText("Generated.")
            self.Reflow()
            if hasattr(self.GetParent().GetParent(), 'hist'): self.GetParent().GetParent().hist.RefreshList()
        else:
            wx.MessageBox(err, "Error", wx.OK | wx.ICON_ERROR)
        self.Reflow()

    def OnCopy(self, e):
        if self.data_blog and wx.TheClipboard.Open():
            wx.TheClipboard.SetData(wx.TextDataObject(self.data_blog))
            wx.TheClipboard.Close()

    def OnSave(self, e):
        if not self.data_blog: return
        with wx.FileDialog(self, "Save Blog", wildcard="Text files (*.txt)|*.txt",
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL: return
            path = dlg.GetPath()
            try:
                storage.save_blog(self.data_blog, path)
                wx.MessageBox(f"Saved to {path}", "Success")
                if hasattr(self.GetParent().GetParent(), 'hist'): self.GetParent().GetParent().hist.RefreshList()
            except Exception as e:
                wx.MessageBox(str(e), "Error")

    def OnPane(self, e):
        self.Reflow()

    def Reflow(self):
        self.Layout()
        self.FitInside()

class HistoryPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        left = wx.BoxSizer(wx.VERTICAL)
        left.Add(wx.StaticText(self, label="Files"), 0, wx.ALL, 5)
        self.lst = wx.ListBox(self)
        self.lst.Bind(wx.EVT_LISTBOX, self.OnSel)
        left.Add(self.lst, 1, wx.EXPAND | wx.ALL, 5)
        btn = wx.Button(self, label="Refresh")
        btn.Bind(wx.EVT_BUTTON, lambda e: self.RefreshList())
        left.Add(btn, 0, wx.EXPAND | wx.ALL, 5)
        sizer.Add(left, 1, wx.EXPAND | wx.ALL, 10)
        right = wx.BoxSizer(wx.VERTICAL)
        right.Add(wx.StaticText(self, label="Preview"), 0, wx.ALL, 5)
        self.view = wx.html.HtmlWindow(self)
        right.Add(self.view, 3, wx.EXPAND | wx.ALL, 5)
        sizer.Add(right, 2, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.RefreshList()

    def RefreshList(self):
        self.lst.Set(storage.get_history())

    def OnSel(self, e):
        sel = self.lst.GetStringSelection()
        if sel:
            h = markdown.markdown(storage.read_blog(sel))
            s = "body{font-family:'Segoe UI',sans-serif;font-size:11pt;color:#333}h1{color:#2c3e50}h2{color:#34495e;border-bottom:1px solid #ddd}"
            self.view.SetPage(f"<html><style>{s}</style><body>{h}</body></html>")

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="YouTube → Blog Converter", size=(1000, 700))
        
        # Windows Taskbar Icon Fix (AUMID)
        try:
            import ctypes
            myappid = 'link2blog.converter.app.1.0' 
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except:
            pass

        if os.path.exists("favi.jpg"):
            icon = wx.Icon("favi.jpg", wx.BITMAP_TYPE_JPEG)
            self.SetIcon(icon)

        nb = wx.Notebook(self)
        self.conv = ConverterPanel(nb)
        self.hist = HistoryPanel(nb)
        nb.AddPage(self.conv, "Converter")
        nb.AddPage(self.hist, "History")
        self.CreateStatusBar()
        self.SetStatusText("Ready")
        self.Centre()
        self.Show()

if __name__ == "__main__":
    app = wx.App()
    MainFrame()
    app.MainLoop()
