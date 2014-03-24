from distutils.core import setup
import py2exe

includes = ["wx", "_winreg", "ConfigParser", "ProxyUtil"]

opts = {"py2exe":  
            {"compressed": 1,
             "optimize": 2,
             "includes": includes
             }
           }

setup(
      version = "0.1",
      options = opts,
      zipfile = None,
      windows = [{'script':'ProxySwitch.py',
                  'icon_resources':[(1, 'switch.ico')]}],
      data_files = ['Proxy.ini', 'switch.ico'],
      )