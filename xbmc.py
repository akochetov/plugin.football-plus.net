# -*- coding: utf-8 -*-

class Keyboard:
    def setDefault(self, str):
        print('Keyboard.setDefault message:%s' % str);

    def setHeading(self, str):
        print('Keyboard.setHeading message:%s' % str);
    def doModal(self):
       pass 
    def isConfirmed(self):
        print('Keyboard.isConfirmed')
        return True
    def getText(self):
        print('Keyboard.getText')
        value = ''
        try:
            value = raw_input()
        except:
            pass
        return value

def executebuiltin(function, block = None):
    print('xbmc.executebuiltin %s %s' % (str(function), str(block)));
def log(message,args):
    print('xbmc.log %s %s' % (message, str(args)));
        