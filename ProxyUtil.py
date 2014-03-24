# coding: UTF-8

from ConfigParser import SafeConfigParser
import _winreg as reg

def getProxyList():
    proxyList = []
    with open("Proxy.ini") as f:
        scp = SafeConfigParser()
        scp.readfp(f)
        for section in scp.sections():
            for opt in scp.options(section):
                proxyList.append({opt: scp.get(section, opt)})

    proxyList.insert(0, {'no proxy*': ''})
    return proxyList

def getValueByOption(option):
    scp = SafeConfigParser()
    scp.read('Proxy.ini')
    return scp.get('Proxy', option)

def modifyProxyList(name, url=None):
    scp = SafeConfigParser()
    scp.read('Proxy.ini')
    if url:
        scp.set('Proxy', name, url)
    else:
        scp.remove_option('Proxy', name)
    
    with open("Proxy.ini", 'w') as f:
        scp.write(f)

def setProxyReg(option):
    key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 
                      0, reg.KEY_ALL_ACCESS)

    if option == 'no proxy*':
        try:
            if reg.QueryValueEx(key, "AutoConfigURL"):
                reg.DeleteValue(key, "AutoConfigURL")
        except WindowsError:
            pass
        reg.SetValueEx(key, "ProxyEnable", 1, reg.REG_DWORD, 0)
    elif option == 'auto*':
        reg.SetValueEx(key, "AutoConfigURL", 1, reg.REG_SZ, getValueByOption(option))
        reg.SetValueEx(key, "ProxyEnable", 1, reg.REG_DWORD, 0)
    else:
        try:
            if reg.QueryValueEx(key, "AutoConfigURL"):
                reg.DeleteValue(key, "AutoConfigURL")
        except WindowsError:
            pass
        
        reg.SetValueEx(key, "ProxyEnable", 1, reg.REG_DWORD, 1)
        reg.SetValueEx(key, "ProxyServer", 1, reg.REG_SZ, getValueByOption(option))

    reg.FlushKey(key)
    reg.CloseKey(key)
    
if __name__ == "__main__":
    print getProxyList()
    addProxy2List('Auto', 'test')
    print getProxyList()
    delProxyFromList('Auto')
    print getProxyList()