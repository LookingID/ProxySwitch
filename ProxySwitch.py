#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Proxy Switch

author: rainwon
last modified: Dec. 2013
'''

import wx
from ProxyUtil import getProxyList, setProxyReg, modifyProxyList

class frmProxySwitch(wx.Frame):
    def __init__(self, parent, id):
        self.defaultX_R = 50
        self.defaultX_T = 150
        self.defaultY = 20
        wx.Frame.__init__(self, parent, id, 'Proxy Switch', 
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX))
        
        dSize = wx.DisplaySize()
        self.SetPosition(((dSize[0] - 420) / 2, (dSize[1] - 300) / 2))

        self.panel = wx.Panel(self, -1)
        self.panel.SetBackgroundColour('LIGHT STEEL BLUE')
        
        icon = wx.Icon('switch.ico', wx.BITMAP_TYPE_ICO, 16, 16)
        self.SetIcon(icon)
        
        self.rbtnList = []
        self.txtList = []
        
        self.initialUI()
        
    def initialUI(self):
        self.buildProxyGroup()
        self.buildMenu()
        self.CreateStatusBar()
        self.btnRun = wx.Button(self.panel, -1, label='Switch', pos=(180, len(self.rbtnList) * 40 + 20))
        self.btnRun.Bind(wx.EVT_BUTTON, self.switchProxy)
        
    def buildMenu(self):
        menuBar = wx.MenuBar()
        menu = wx.Menu()
        menuBar.Append(menu, 'Proxy')
        mNew = menu.Append(wx.NewId(), 'New', 'Add a new proxy')
        mDel = menu.Append(wx.NewId(), 'Delete', 'Delete current proxy DIRECTLY!!!')
        
        self.Bind(wx.EVT_MENU, self.addNewProxy, mNew)
        self.Bind(wx.EVT_MENU, self.removeCurrentProxy, mDel)
        self.SetMenuBar(menuBar)
    
    def buildProxyGroup(self):
        proxyList = getProxyList()
        length = len(proxyList)
        
        self.SetSize(size=(420, len(proxyList) * 40 + 120))
        
        if length:
            defaultX_R = 50
            defaultX_T = 150
            defaultY = 20
            for i in range(0, length):
                proxyNode = proxyList[i]
                self.rbtnList.append(wx.RadioButton(self.panel, label=proxyNode.keys()[0].capitalize(), 
                                                  pos=(self.defaultX_R, self.defaultY + (i * 40)), 
                                                  name=proxyNode.keys()[0]))
                self.txtList.append(wx.TextCtrl(self.panel, -1, '', 
                                                pos=(self.defaultX_T, self.defaultY + (i * 40)), size=(200, 20)))
                
                if i == 0:
                    self.txtList[i].Hide()
                    continue
                
                self.txtList[i].SetEditable(False)
                self.txtList[i].SetValue(proxyNode.values()[0])
                self.txtList[i].Bind(wx.EVT_LEFT_DCLICK, self.enableEdit)
                self.txtList[i].Bind(wx.EVT_KILL_FOCUS, self.unableEdit)

    def enableEdit(self, event):
        txtCtl = event.GetEventObject()
        txtCtl.SetForegroundColour('Red')
        txtCtl.SetEditable(True)

    def unableEdit(self, event):
        txtCtl = event.GetEventObject()
        
        if txtCtl.IsEditable():
            index = self.txtList.index(txtCtl)
            modifyProxyList(self.rbtnList[index].GetName(), txtCtl.GetValue())
            
            txtCtl.SetForegroundColour('Black')
            txtCtl.SetEditable(False)
        
    def switchProxy(self, event):
        for rbtn in self.rbtnList:
            if rbtn.GetValue():
                setProxyReg(rbtn.GetName())
                
    def addNewProxy(self, event):
        pDialog = MultiTextDialog()
        if pDialog.ShowModal() == wx.ID_OK:
            vName, vAddr = pDialog.fetchInputs()
            if vName and vAddr:
                modifyProxyList(vName, vAddr)
                sz = self.Size
                h = sz[1]
                self.SetSize(size=(sz[0], h + 40))
                self.btnRun.SetPosition((180, h - 60))
                
                self.rbtnList.append(wx.RadioButton(self.panel, label=vName.capitalize(), 
                                                      pos=(self.defaultX_R, self.defaultY + (len(self.rbtnList) * 40)), 
                                                      name=vName))
                self.txtList.append(wx.TextCtrl(self.panel, -1, vAddr, 
                                                pos=(self.defaultX_T, self.defaultY + (len(self.rbtnList) - 1) * 40), 
                                                size=(200, 20)))
        pDialog.Destroy()
        
    def removeCurrentProxy(self, event):
        for index, rbtn in enumerate(self.rbtnList):
            if rbtn.GetValue():
                if index < 2:
                    wx.MessageBox('Cannot delete default option', 'Info', wx.OK | wx.ICON_INFORMATION)
                    break
                modifyProxyList(rbtn.GetName())
                self.reRenderUI(index)
                
    def reRenderUI(self, index):
        sz = self.Size
        h = sz[1]

        tmpRbtn = self.rbtnList[index]
        tmpRbtn.Destroy()
        self.rbtnList.remove(tmpRbtn)
        tmpTxt = self.txtList[index]
        tmpTxt.Destroy()

        while index < len(self.rbtnList) - 1:
            index += 1
            self.rbtnList[index].SetPosition((self.defaultX_R, self.defaultY + (index - 1) * 40))
            self.txtList[index].SetPosition((self.defaultX_T, self.defaultY + (index - 1) * 40))

        self.SetSize(size=(sz[0], h - 40))
        self.btnRun.SetPosition((180, h - 140))


class MultiTextDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, 'New Proxy')
        
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.txtName = wx.TextCtrl(self, -1, name='name')
        self.txtAddr = wx.TextCtrl(self, -1, name='addr')
        ok = wx.Button(self, wx.ID_OK, 'OK')
        
        sizer.Add(self.txtName, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(self.txtAddr, 1, wx.EXPAND | wx.ALL, 5)
        sizer.Add(ok, 0, wx.ALIGN_RIGHT | wx.ALL ^ wx.TOP, 5)
        
        self.SetSizer(sizer)
        self.Center()
        
    def fetchInputs(self):
        return self.txtName.GetValue(), self.txtAddr.GetValue()
    
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = frmProxySwitch(parent=None, id=-1)
    frame.Show()
    app.MainLoop()