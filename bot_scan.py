from os.path import dirname, basename, isfile, join
import sys
import glob
import importlib

modules = glob.glob(join(dirname(__file__),"bots", "*.py"))

modules= ["bots." + i.rsplit("\\",2)[-1].split('.')[0] for i in modules]
   
callBot = None
for i,k in enumerate(modules):
    print(str(i)+". " + k.split('.')[1])
while callBot is None:
    try:
        choice = int(input("Enter your bot number: "))
        importlib.import_module(modules[choice])
        callBot = sys.modules[modules[choice]].callBot
        break
    except:
        print("unable to import bot")
        pass
