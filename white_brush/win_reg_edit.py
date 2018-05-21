from winreg import *

aReg = ConnectRegistry(None,HKEY_CURRENT_USER)

# replace path to python and path to script below!

aKey = OpenKey(aReg, r"Software\Classes\*\shell", 0, KEY_WRITE)
try:
   newKey = CreateKey(aKey, "Whitebrush")
   SetValue(newKey, "command", REG_SZ, "C:\Path\To\python.exe C:\Path\To\script.py %1")
except EnvironmentError:
    print("Encountered problems writing into the Registry...")
CloseKey(aKey)

print("Successfully updated registry")

CloseKey(aReg)