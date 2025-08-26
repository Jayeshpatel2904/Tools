#$language = "Python"
#$interface = "1.0"

# StartSessionInTabByArgument.py
#
# Description:
# Starts session in new tab, session name provided as parameter

def main():

    objMainTab = crt.GetScriptTab()
    objSvr3Tab = objMainTab.Clone
    objSvr2Tab = objMainTab.Clone


    objMainTab.Caption = "server1.domain.com (gateway/jump)"
    objSvr2Tab.Caption = "server2.domain.com"
    objSvr3Tab.Caption = "server3.domain.com"
    
    crt.Dialog.MessageBox(str(crt.GetTabCount()))

main()