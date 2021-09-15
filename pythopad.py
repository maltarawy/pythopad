import os
import wx
import wx.adv
import webbrowser
import wx.stc as stc
import wx.lib.dialogs
import keyword

#Main class
class Window(wx.Frame):
    def __init__(self, parent, title):
        #Filename and Directory name
        self.filename = ''
        self.dirname = ''

        #Transparent
        self.transparent = False

        #View Indentation Guides
        self.viewindentationguides = False

        #View Whitespace
        self.viewwhitespace = False

        #Always on Top
        self.alwaysontop = False

        #Line numbers enabled
        self.lineNumbersEnabled = True

        #View EOL's
        self.vieweol = False

        #Find variables
        self.pos = 0
        self.size = 0

        #Lexer
        self.lexer = "Normal Text"

        #Window
        wx.Frame.__init__(self, parent, title=title, size=(680, 600))
        self.control = stc.StyledTextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap("logo.png", wx.BITMAP_TYPE_ANY))
        self.ShowFullScreen(False)
        self.SetIcon(icon)
        self.SetupFunctions()

        self.control.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:Courier New")

        self.control.SetZoom(2)

        self.control.SetCaretLineBackground((241,246,250))
        self.control.SetCaretLineVisible(True)

        self.control.Bind(stc.EVT_STC_UPDATEUI, self.Scroll)

    def SetupFunctions(self):
        #Sets up all functions
        self.Margins()
        self.Status_Bar()
        self.FileMenu(), self.EditMenu(), self.ViewMenu(), self.HelpMenu()
        self.MenuBar()
        self.ToolBar()
        self.BindsMenu()
        self.BindsTool()

    def Margins(self):
        self.control.SetViewWhiteSpace(False)
        self.control.SetMargins(5, 0)
        self.control.SetMarginType(1, stc.STC_MARGIN_NUMBER)

    def Scroll(self, e):
        x = self.control.GetFirstVisibleLine()
        y = self.control.LinesOnScreen()
        x = x+y
        x = len(str(x))
        self.control.SetMarginWidth(1, x*16)

    def Status_Bar(self):
        #Status Bar
        self.statusbar = self.CreateStatusBar(1)
        self.StatusLineColumn(self)

    def ToolBar(self):
        self.toolbar = wx.ToolBar(self)
        self.SetToolBar(self.toolbar)
        self.newtool = self.toolbar.AddTool(wx.ID_ANY, 'New', wx.Bitmap('toolbar/new.png'))
        self.opentool = self.toolbar.AddTool(wx.ID_ANY, 'Open', wx.Bitmap('toolbar/open.png'))
        self.savetool = self.toolbar.AddTool(wx.ID_ANY, 'Save', wx.Bitmap('toolbar/save.png'))
        self.saveastool = self.toolbar.AddTool(wx.ID_ANY, 'Save As', wx.Bitmap('toolbar/save-as.png'))
        self.toolbar.AddSeparator()
        self.undotool = self.toolbar.AddTool(wx.ID_ANY, 'Undo', wx.Bitmap('toolbar/undo.png'))
        self.redotool = self.toolbar.AddTool(wx.ID_ANY, 'Redo', wx.Bitmap('toolbar/redo.png'))
        self.toolbar.AddSeparator()
        self.cuttool = self.toolbar.AddTool(wx.ID_ANY, 'Cut', wx.Bitmap('toolbar/cut.png'))
        self.copytool = self.toolbar.AddTool(wx.ID_ANY, 'Copy', wx.Bitmap('toolbar/copy.png'))
        self.pastetool = self.toolbar.AddTool(wx.ID_ANY, 'Paste', wx.Bitmap('toolbar/paste.png'))
        self.toolbar.AddSeparator()
        self.zoomintool = self.toolbar.AddTool(wx.ID_ANY, 'Zoom In', wx.Bitmap('toolbar/zoom-in.png'))
        self.zoomouttool = self.toolbar.AddTool(wx.ID_ANY, 'Zoom Out', wx.Bitmap('toolbar/zoom-out.png'))
        self.toolbar.AddSeparator()
        self.abouttool = self.toolbar.AddTool(wx.ID_ANY, 'About', wx.Bitmap('toolbar/info.png'))
        self.quittool = self.toolbar.AddTool(wx.ID_ANY, 'Quit', wx.Bitmap('toolbar/quit.png'))
        self.toolbar.Realize()

    def FileMenu(self):
        #File Menu
        self.filemenu = wx.Menu()
        self.new = self.filemenu.Append(wx.ID_NEW, "&New\tCtrl+N", "Create new document")
        self.open = self.filemenu.Append(wx.ID_OPEN, "&Open\tCtrl+O", "Open existing document")
        self.save = self.filemenu.Append(wx.ID_SAVE, "Save\tCtrl+S")
        self.save_as = self.filemenu.Append(wx.ID_SAVEAS, "Save &As\tAlt+S")
        self.readonly =  self.filemenu.Append(wx.ID_ANY, "&Read Only\tCtrl+Shift+R", "Set document to read only", wx.ITEM_CHECK)
        self.filemenu.AppendSeparator()
        self.newlinemenu = wx.Menu()
        self.windoweol = self.newlinemenu.Append(wx.ID_ANY, "&Windows (CR + LF)\tAlt+Shift+F1", "Set EOL to Windows")
        self.maceol = self.newlinemenu.Append(wx.ID_ANY, "&Mac (CR)\tAlt+Shift+F2", "Set EOL to Mac")
        self.unixeol = self.newlinemenu.Append(wx.ID_ANY, "&Unix (LF)\tAlt+Shift+F3", "Set EOL to Unix")
        self.filemenu.Append(wx.ID_ANY, "&Newline Endings", self.newlinemenu)
        self.filemenu.AppendSeparator()
        self.quit = self.filemenu.Append(wx.ID_EXIT, "&Quit\tCtrl+Q")

    def EditMenu(self):
        #Edit Menu
        self.editmenu = wx.Menu()
        self.undo = self.editmenu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z", "Undo last step")
        self.redo = self.editmenu.Append(wx.ID_REDO, "&Redo\tCtrl+Y", "Redo last step")
        self.editmenu.AppendSeparator()
        self.cut = self.editmenu.Append(wx.ID_CUT, "&Cut\tCtrl+X", "Cut selected text")
        self.copy = self.editmenu.Append(wx.ID_COPY, "&Copy\tCtrl+C", "Copy selected text")
        self.paste = self.editmenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V", "Paste copied text")
        self.delete = self.editmenu.Append(wx.ID_DELETE, "&Delete\tDel", "Delete selected text")
        self.delete_all = self.editmenu.Append(wx.ID_ANY, "&Delete All\tAlt+Del", "Delete all text in current document")
        self.duplicate = self.editmenu.Append(wx.ID_ANY, "&Duplicate\tAlt+D", "Duplicate selection")
        self.editmenu.AppendSeparator()
        self.select_all = self.editmenu.Append(wx.ID_SELECTALL, "&Select All\tCtrl+A", "Select the entire document")
        self.editmenu.AppendSeparator()
        self.linesmenu = wx.Menu()
        self.line_cut = self.linesmenu.Append(wx.ID_ANY, "&Cut Line\tCtrl+Shift+X", "Cut current line")
        self.line_copy = self.linesmenu.Append(wx.ID_ANY, "&Copy Line\tCtrl+Shift+C", "Copy current line")
        self.line_delete = self.linesmenu.Append(wx.ID_ANY, "&Delete Line\tCtrl+Shift+D", "Delete current line")
        self.line_duplicate = self.linesmenu.Append(wx.ID_ANY, "&Duplicate Line\tAlt+Shift+D", "Duplicate current line")
        self.editmenu.Append(wx.ID_ANY, "&Lines", self.linesmenu)
        self.insertmenu = wx.Menu()
        self.insertfilename = self.insertmenu.Append(wx.ID_ANY, "&Filename\tCtrl+F8", "Insert filename")
        self.insertfilepath = self.insertmenu.Append(wx.ID_ANY, "&Filepath\tAlt+F8", "Inset filepath")
        self.editmenu.Append(wx.ID_ANY, "&Insert", self.insertmenu)
        self.formatmenu = wx.Menu()
        self.indent = self.formatmenu.Append(wx.ID_ANY, "&Indent\tTab", "Indent selection")
        self.unindent = self.formatmenu.Append(wx.ID_ANY, "&Unindent\tShift+Tab", "Unindent selection")
        self.formatmenu.AppendSeparator()
        self.uppercase = self.formatmenu.Append(wx.ID_ANY, "&Uppercase\tAlt+U", "Set selection to UPPERCASE")
        self.lowercase = self.formatmenu.Append(wx.ID_ANY, "&Lowercase\tAlt+L", "Set selection to lowercase")
        self.formatmenu.AppendSeparator()
        self.wordwrap = self.formatmenu.Append(wx.ID_ANY, "&Word Wrap\tCtrl+W", "Set text to word wrapped", wx.ITEM_CHECK)
        self.editmenu.Append(wx.ID_ANY, "&Format", self.formatmenu)

    def ViewMenu(self):
        #View Menu
        self.viewmenu = wx.Menu()
        self.languagesmenu = wx.Menu()
        self.normaltext = self.languagesmenu.Append(wx.ID_ANY, "&Normal Text\tAlt+Shift+0", "Set syntax highlighting to Normal Text")
        self.languagesmenu.AppendSeparator()
        self.python = self.languagesmenu.Append(wx.ID_ANY, "&Python\tAlt+Shift+4", "Set syntax highlighting to Python")
        self.viewmenu.Append(wx.ID_ANY, "&Language", self.languagesmenu)
        self.viewmenu.AppendSeparator()
        self.togalwaysontop = self.viewmenu.Append(wx.ID_ANY, "&Always on Top\tAlt+F1", "Enable/Disable always on top", wx.ITEM_CHECK)
        self.fullscreen = self.viewmenu.Append(wx.ID_ANY, "&Fullscreen\tF11", "Fullscreen Pythopad", wx.ITEM_CHECK)
        self.viewmenu.AppendSeparator()
        self.toglinenumbers = self.viewmenu.Append(wx.ID_ANY, "Toggle &Line Numbers\tAlt+Shift+L", "Enable/Disable line numbers", wx.ITEM_CHECK)
        self.togstatusbar = self.viewmenu.Append(wx.ID_ANY, "Toggle &Status Bar\tAlt+Shift+S", "Enable/Disable status bar", wx.ITEM_CHECK)
        self.togtransparent = self.viewmenu.Append(wx.ID_ANY, "Toggle &Transparent Mode\tAlt+Shift+T", "Enable/Disable transparent mode", wx.ITEM_CHECK)
        self.togvieweol = self.viewmenu.Append(wx.ID_ANY, "Toggle &View Newline Endings\tAlt+Shift+E", "Enable/Disable view newline endings", wx.ITEM_CHECK)
        self.viewmenu.AppendSeparator()
        self.zoom_in = self.viewmenu.Append(wx.ID_ZOOM_IN, "Zoom &In\tCtrl++", "Zoom in to the applicaton")
        self.zoom_out = self.viewmenu.Append(wx.ID_ZOOM_OUT, "Zoom &Out\tCtrl+-", "Zoom out the applicaton")
        self.reset_zoom = self.viewmenu.Append(wx.ID_ANY, "Reset &Zoom\tCtrl+0", "Reset zoom level of the applicaton")
        self.viewmenu.AppendSeparator()
        self.indentationguide = self.viewmenu.Append(wx.ID_ANY, "&View Indentation Guides\tCtrl+W", "Enable/Disable indentation guide", wx.ITEM_CHECK)
        self.whitespace = self.viewmenu.Append(wx.ID_ANY, "&View Whitespace\tCtrl+Shift+W", "Enable/Disable whitespace", wx.ITEM_CHECK)

    def HelpMenu(self):
        #Help Menu
        self.helpmenu = wx.Menu()
        self.about = self.helpmenu.Append(wx.ID_ABOUT, "&About\tF1", "About Pythopad")
        self.helpmenu.AppendSeparator()
        self.homepage = self.helpmenu.Append(wx.ID_ANY, "&Pythopad Homepage\tCtrl+F2", "Pythopad's homepage")
        self.github = self.helpmenu.Append(wx.ID_ANY, "&Pythopad GitHub\tCtrl+F3", "Pythopad's GitHub")
        self.helpmenu.AppendSeparator()
        self.version = self.helpmenu.Append(wx.ID_ANY, "&Check for new version\tCtrl+F4", "Check for a new version")

    def MenuBar(self):
        #MenuBar
        self.menu = wx.MenuBar()
        self.menu.Append(self.filemenu, "&File")
        self.menu.Append(self.editmenu, "&Edit")
        self.menu.Append(self.viewmenu, "&View")
        self.menu.Append(self.helpmenu, "&Help")
        self.SetMenuBar(self.menu)

    def BindsMenu(self):
        #Binding menu functions and items
        self.Bind(wx.EVT_MENU, self.New, self.new)
        self.Bind(wx.EVT_MENU, self.Open, self.open)
        self.Bind(wx.EVT_MENU, self.Save, self.save)
        self.Bind(wx.EVT_MENU, self.SaveAs, self.save_as)
        self.Bind(wx.EVT_MENU, self.Quit, self.quit)
        self.Bind(wx.EVT_MENU, self.Undo, self.undo)
        self.Bind(wx.EVT_MENU, self.Redo, self.redo)
        self.Bind(wx.EVT_MENU, self.Cut, self.cut)
        self.Bind(wx.EVT_MENU, self.Copy, self.copy)
        self.Bind(wx.EVT_MENU, self.Paste, self.paste)
        self.Bind(wx.EVT_MENU, self.Delete, self.delete)
        self.Bind(wx.EVT_MENU, self.DeleteAll, self.delete_all)
        self.Bind(wx.EVT_MENU, self.SelectAll, self.select_all)
        self.Bind(wx.EVT_MENU, self.LineCut, self.line_cut)
        self.Bind(wx.EVT_MENU, self.LineCopy, self.line_copy)
        self.Bind(wx.EVT_MENU, self.LineDelete, self.line_delete)
        self.Bind(wx.EVT_MENU, self.LineDuplicate, self.line_duplicate)
        self.Bind(wx.EVT_MENU, self.Indent, self.indent)
        self.Bind(wx.EVT_MENU, self.Unindent, self.unindent)
        self.Bind(wx.EVT_MENU, self.Uppercase, self.uppercase)
        self.Bind(wx.EVT_MENU, self.Lowercase, self.lowercase)
        self.Bind(wx.EVT_MENU, self.InsertFilename, self.insertfilename)
        self.Bind(wx.EVT_MENU, self.InsertPath, self.insertfilepath)
        self.Bind(wx.EVT_MENU, self.NormalText, self.normaltext)
        self.Bind(wx.EVT_MENU, self.Python, self.python)
        self.Bind(wx.EVT_MENU, self.Duplicate, self.duplicate)
        self.Bind(wx.EVT_MENU, self.Fullscreen, self.fullscreen)
        self.Bind(wx.EVT_MENU, self.ZoomIn, self.zoom_in)
        self.Bind(wx.EVT_MENU, self.ZoomOut, self.zoom_out)
        self.Bind(wx.EVT_MENU, self.ResetZoom, self.reset_zoom)
        self.Bind(wx.EVT_MENU, self.TogLineNumbers, self.toglinenumbers)
        self.Bind(wx.EVT_MENU, self.TogStatusBar, self.togstatusbar)
        self.Bind(wx.EVT_MENU, self.TogTransparent, self.togtransparent)
        self.Bind(wx.EVT_MENU, self.ReadOnly, self.readonly)
        self.Bind(wx.EVT_MENU, self.ViewIndentationGuide, self.indentationguide)
        self.Bind(wx.EVT_MENU, self.ViewWhiteSpace, self.whitespace)
        self.Bind(wx.EVT_MENU, self.TogAlwaysOnTop, self.togalwaysontop)
        self.Bind(wx.EVT_MENU, self.TogViewEOL, self.togvieweol)
        self.Bind(wx.EVT_MENU, self.WindowsEOL, self.windoweol)
        self.Bind(wx.EVT_MENU, self.MacEOL, self.maceol)
        self.Bind(wx.EVT_MENU, self.UnixEOL, self.unixeol)
        self.Bind(wx.EVT_MENU, self.WordWrap, self.wordwrap)
        self.Bind(wx.EVT_MENU, self.About, self.about)
        self.Bind(wx.EVT_MENU, self.Homepage, self.homepage)
        self.Bind(wx.EVT_MENU, self.GitHub, self.github)
        self.Bind(wx.EVT_MENU, self.Version, self.version)
        self.Bind(wx.EVT_CLOSE, self.Close)
        self.control.Bind(wx.EVT_KEY_UP, self.StatusLineColumn)
        self.control.Bind(wx.EVT_LEFT_UP, self.UpdateStatusLineColumn)
        self.Bind(wx.EVT_MENU_HIGHLIGHT, self.Bypass)
        
    def BindsTool(self):
        self.Bind(wx.EVT_TOOL, self.New, self.newtool)
        self.Bind(wx.EVT_TOOL, self.Open, self.opentool)
        self.Bind(wx.EVT_TOOL, self.Save, self.savetool)
        self.Bind(wx.EVT_TOOL, self.SaveAs, self.saveastool)
        self.Bind(wx.EVT_TOOL, self.Quit, self.quittool)
        self.Bind(wx.EVT_TOOL, self.Undo, self.undotool)
        self.Bind(wx.EVT_TOOL, self.Redo, self.redotool)
        self.Bind(wx.EVT_TOOL, self.Cut, self.cuttool)
        self.Bind(wx.EVT_TOOL, self.Copy, self.copytool)
        self.Bind(wx.EVT_TOOL, self.Paste, self.pastetool)
        self.Bind(wx.EVT_MENU, self.ZoomIn, self.zoomintool)
        self.Bind(wx.EVT_MENU, self.ZoomOut, self.zoomouttool)
        self.Bind(wx.EVT_MENU, self.About, self.abouttool)
        self.Bind(wx.EVT_MENU, self.Quit, self.quittool)

    #Menu item functions
    def New(self, e):
        if self.control.IsModified():
            dlg = wx.MessageBox('Would you like to save changes to '+self.filename+'?', 'Save Changes?', wx.YES_NO | wx.CANCEL)
            if dlg == wx.YES:
                self.Save(e)
                self.control.SetValue("")
                self.SetTitle("Untitled - Pythopad")
                self.control.SetModified(False)
            if dlg == wx.NO:
                self.control.SetValue("")
                self.SetTitle("Untitled - Pythopad")
                self.control.SetModified(False)
        else:
            self.control.SetValue("")
            self.SetTitle("Untitled - Pythopad")
            self.control.SetModified(False)
        self.filename = ''
        self.dirname = ''
        self.control.StyleClearAll()

    def Open(self, e):
        if self.control.IsModified():
            dlg = wx.MessageBox('Would you like to save changes?', 'Save Changes?', wx.YES_NO | wx.CANCEL)
            if dlg == wx.YES:
                self.Save(e)
                self.OnOpen(e)
            if dlg == wx.NO:
                self.OnOpen(e)
        else:
            self.OnOpen(e)

    def OnOpen(self, e):
        try:
            dlg = wx.FileDialog(self, "Select a file", self.dirname, "", "*.*", wx.FD_OPEN)
            if(dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                self.suffix = self.filename.rsplit('.')[-1]
                if self.suffix == "py":
                    self.Python(e)
                elif self.suffix == "pyc":
                    self.Python(e)
                elif self.suffix == "pyd":
                    self.Python(e)
                elif self.suffix == "pyo":
                    self.Python(e)
                elif self.suffix == "pyw":
                    self.Python(e)
                elif self.suffix == "pyz":
                    self.Python(e)
                else:
                    self.NormalText(e)
                f = open(os.path.join(self.dirname, self.filename), 'r')
                self.control.SetValue(f.read())
                self.SetTitle(self.filename+" - "+self.dirname+" - Pythopad")
                f.close()
                self.control.SetModified(False)
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Error loading file", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            self.control.SetModified(False)
            dlg.Destroy()

    def Save(self, e):
        try:
            f = open(os.path.join(self.dirname, self.filename), 'w')
            f.write(self.control.GetValue())
            self.control.SetModified(False)
            f.close()
        except:
            try:
                dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                if (dlg.ShowModal() == wx.ID_OK):
                    self.filename = dlg.GetFilename()
                    self.dirname = dlg.GetDirectory()
                    f = open(os.path.join(self.dirname, self.filename), 'w')
                    f.write(self.control.GetValue())
                    self.SetTitle(self.filename+" - "+self.dirname+" - Pythopad")
                    f.close()
                    self.control.SetModified(False)
                dlg.Destroy()
            except:
                dlg = wx.MessageDialog(self, "Error saving file", "Error", wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()

    def SaveAs(self, e):
        try:
            dlg = wx.FileDialog(self, "Save file as", self.dirname, "Untitled", "*.*", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if (dlg.ShowModal() == wx.ID_OK):
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                f = open(os.path.join(self.dirname, self.filename), 'w')
                f.write(self.control.GetValue())
                self.SetTitle(self.filename+" - "+self.dirname+" - Pythopad")
                f.close()
                self.control.SetModified(False)
            dlg.Destroy()
        except:
            dlg = wx.MessageDialog(self, "Error saving file", "Error", wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()

    def WindowsEOL(self, e):
        self.control.SetEOLMode(wx.stc.STC_EOL_CRLF)

    def MacEOL(self, e):
        self.control.SetEOLMode(wx.stc.STC_EOL_CR)

    def UnixEOL(self, e):
        self.control.SetEOLMode(wx.stc.STC_EOL_LF)

    def Quit(self, e):
        if self.control.IsModified():
            dlg = wx.MessageBox('Would you like to save changes?','Save Changes?', wx.YES_NO | wx.CANCEL)
            if dlg == wx.YES:
                self.Save(e)
                self.Close(True)
            if dlg == wx.NO:
                self.Close(True)
        else:
            self.Close(True)

    def Undo(self, e):
        self.control.Undo()

    def Redo(self, e):
        self.control.Redo()

    def Cut(self, e):
        self.control.Cut()

    def Copy(self, e):
        self.control.Copy()

    def Paste(self, e):
        self.control.Paste()

    def Delete(self, e):
        self.control.DeleteBack()

    def DeleteAll(self, e):
        self.control.ClearAll()

    def SelectAll(self, e):
        self.control.SelectAll()

    def Fullscreen(self, e):
        self.ShowFullScreen(not self.IsFullScreen())

    def LineCut(self, e):
        self.control.LineCut()

    def LineCopy(self, e):
        self.control.LineCopy()

    def LineDelete(self, e):
        self.control.LineDelete()

    def LineDuplicate(self, e):
        self.control.LineDuplicate()

    def Indent(self, e):
        self.control.Tab()

    def Unindent(self, e):
        self.control.BackTab()

    def Uppercase(self, e):
        self.control.UpperCase()

    def Lowercase(self, e):
        self.control.LowerCase()

    def Duplicate(self, e):
        self.control.SelectionDuplicate()

    def InsertFilename(self, e):
        self.control.AddText(self.filename)

    def InsertPath(self, e):
        self.control.AddText(self.dirname)

    def ZoomIn(self, e):
        self.control.ZoomIn()

    def ZoomOut(self, e):
        self.control.ZoomOut()

    def ResetZoom(self, e):
        self.control.SetZoom(2)

    def TogLineNumbers(self, e):
        if self.lineNumbersEnabled:
            self.control.SetMarginWidth(1, 0)
            self.lineNumbersEnabled = False
        else:
            self.control.SetMarginWidth(1, 35)
            self.lineNumbersEnabled = True

    def TogStatusBar(self, e):
        if self.statusbar.IsShown():
            self.statusbar.Hide()
            self.Update()
        else:
            self.statusbar.Show()

    def TogTransparent(self, e):
        if not self.transparent:
            self.SetTransparent(200)
        else:
            self.SetTransparent(255)
        self.transparent = not self.transparent

    def ViewIndentationGuide(self, e):
        if not self.viewindentationguides:
            self.viewindentationguides = True
            self.control.SetIndentationGuides(True)
        else:
            self.viewindentationguides = False
            self.control.SetIndentationGuides(False)

    def ViewWhiteSpace(self, e):
        if not self.viewwhitespace:
            self.viewwhitespace = True
            self.control.SetViewWhiteSpace(True)
        else:
            self.viewwhitespace = False
            self.control.SetViewWhiteSpace(False)

    def TogAlwaysOnTop(self, e):
        if not self.viewindentationguides:
            self.viewindentationguides = True
            self.ToggleWindowStyle(wx.STAY_ON_TOP)
        else:
            self.viewindentationguides = False
            self.ToggleWindowStyle(wx.STAY_ON_TOP)

    def TogViewEOL(self, e):
        if not self.vieweol:
            self.vieweol = True
            self.control.SetViewEOL(True)
        else:
            self.vieweol = False
            self.control.SetViewEOL(False)

    def ReadOnly(self, e):
        self.readonly = not self.readonly
        if not self.readonly:
            self.control.SetReadOnly(True)
        else:
            self.control.SetReadOnly(False)

    def WordWrap(self, e):
        self.wordwrap = not self.wordwrap
        if not self.wordwrap:
            self.control.SetWrapMode(True)
        else:
            self.control.SetWrapMode(False)

    def About(self, e):
        info = wx.adv.AboutDialogInfo()
        info.SetName('Pythopad')
        info.SetIcon(wx.Icon('favicon.png', wx.BITMAP_TYPE_PNG))
        info.SetVersion('1.0')
        info.SetCopyright('(C) 2021 Mohamed Altarawy')
        info.SetWebSite('http://maltarawy.github.io/pythopad/')
        wx.adv.AboutBox(info)

    def Homepage(self, e):
        webbrowser.open('https://maltarawy.github.io/pythopad/')

    def GitHub(self, e):
        webbrowser.open('https://github.com/maltarawy/pythopad/')

    def Version(self, e):
        webbrowser.open('https://github.com/maltarawy/pythopad/releases')

    def StatusLineColumn(self, e):
        line = self.control.GetCurrentLine() + 1
        col = self.control.GetColumn(self.control.GetCurrentPos())
        length = self.control.GetLineCount()
        stat = "Ln: %s/%s, Col: %s" % (line, length, col)
        self.StatusBar.SetStatusText(stat, 0)

    def UpdateStatusLineColumn(self, e):
        self.StatusLineColumn(self)
        e.Skip()

    def Close(self, e):
        if self.control.IsModified():
            dlg = wx.MessageBox('Would you like to save changes?', 'Save Changes?', wx.YES_NO | wx.CANCEL)
            if dlg == wx.YES:
                self.Save(e)
                self.Destroy()
            if dlg == wx.NO:
                self.Destroy()
        else:
            self.Destroy()

    def Bypass(self, e):
        pass

    #Syntax highlighting
    def NormalText(self, e):
        self.lexer = "Normal Text"
        self.control.StyleClearAll()

    def Python(self, e):
        self.lexer = "Python"
        self.control.SetLexer(stc.STC_LEX_PYTHON)
        self.control.SetKeyWords(0, " ".join(keyword.kwlist))
        self.control.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        self.control.StyleSetSpec(wx.stc.STC_P_COMMENTLINE, 'fore:#008000')
        self.control.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000')
        self.control.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        self.control.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        self.control.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        self.control.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080')
        self.control.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#800080')
        self.control.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE, 'fore:#800080')
        self.control.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF')
        self.control.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#008080')
        self.control.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000')
        self.control.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

def main():
    app = wx.App()
    frame = Window(None, "Untitled - Pythopad")
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
