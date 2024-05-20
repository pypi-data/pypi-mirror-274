#File type: extension <class page> set
#By Junxiang H., 2023/07/9
#wacmk.com/cn Tech. Supp.

#This script updates automaticly! Do not Modify!
#Update time:2023-07-11 15:25:18

Pages={}
try:
	try:
		import ShockFinder.Addon.GUI.XUIlib.pages.Figure as Figure
	except:
		import XUIlib.pages.Figure as Figure
	Pages["Figure"]=Figure
except Exception as err:
	print("Page: Figure import failure:",err)

try:
	try:
		import ShockFinder.Addon.GUI.XUIlib.pages.Analyze as Analyze
	except:
		import XUIlib.pages.Analyze as Analyze
	Pages["Analyze"]=Analyze
except Exception as err:
	print("Page: Analyze import failure:",err)

try:
	try:
		import ShockFinder.Addon.GUI.XUIlib.pages.Exit as Exit
	except:
		import XUIlib.pages.Exit as Exit
	Pages["Exit"]=Exit
except Exception as err:
	print("Page: Exit import failure:",err)

try:
	try:
		import ShockFinder.Addon.GUI.XUIlib.pages.Help as Help
	except:
		import XUIlib.pages.Help as Help
	Pages["Help"]=Help
except Exception as err:
	print("Page: Help import failure:",err)

if __name__=="__main__":
	print("Testing Model:",__file__)
	print("Pages:")
	for i in Pages.keys():
		print(i,":",Pages[i])
		print("\t",Pages[i].page)