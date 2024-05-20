#This is a model file for XUI page
#Junxiang H. 2023.07.09
import os,copy
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
import ShockFinder.Addon.Time as Time
from ShockFinder.Addon.ConfigReader import get_config
from tkinter import *
from tkinter import ttk,filedialog
from multiprocessing import cpu_count
class page(page):
	img={"logo":Image_A}
	pars={}
	parmax=50
	def GS_MPE(self):
		MPE=self.add_menu("Multi-process",submenu=1)
		self.pars["MultiprocessEngine"]={}
		#Multiprocessing
		self.add_row(MPE) #skip row (empty row)
		self.add_title(MPE,"Multi-process")
		Label(self.add_row(MPE,bx=150),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(MPE,bx=150)
		Label(box,text="Engine",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		egs=list(self.pageargs["Infobj"].Config["MultiprocessEngine"].keys())+[None]
		MPE_ENG=ttk.Combobox(box,width=18,height=len(egs) if len(egs)<=10 else 10,values=egs)
		if self.pageargs["Infobj"].Default_MPE in self.pageargs["Infobj"].Config["MultiprocessEngine"]:
			MPE_ENG.set(self.pageargs["Infobj"].Default_MPE)
		else:
			MPE_ENG.set(str(egs[0]))
		MPE_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_mpeeng(event):
			self.pars["MultiprocessEngine"]["Engine"]=MPE_ENG.get()
			self.tkobj.io_recv("Updated MultiprocessEngine-Engine to",self.pars["MultiprocessEngine"]["Engine"])
		self.pars["MultiprocessEngine"]["Engine"]=MPE_ENG.get()
		button_mpeeng=Button(box,text="Update",width=5)
		button_mpeeng.bind("<ButtonRelease>",fun_mpeeng)
		button_mpeeng.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Cores Num",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_PNUM=Entry(box,width=20)
		MPE_PNUM.insert(0,cpu_count() if cpu_count()<=4 and cpu_count()>1 else 4 if cpu_count()>4 else 1)
		MPE_PNUM.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_MPE_PNUM(event):
			self.pars["MultiprocessEngine"]["pnum"]=int(MPE_PNUM.get())
			self.tkobj.io_recv("Updated MultiprocessEngine-pnum to",self.pars["MultiprocessEngine"]["pnum"])
		self.pars["MultiprocessEngine"]["pnum"]=int(MPE_PNUM.get())
		button_MPE_PNUM=Button(box,text="Update",width=5)
		button_MPE_PNUM.bind("<ButtonRelease>",fun_MPE_PNUM)
		button_MPE_PNUM.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Use log",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_do_with_log=ttk.Combobox(box,width=18,height=2,values=[True,False])
		MPE_do_with_log.set(str(True))
		MPE_do_with_log.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_button_do_with_log(event):
			self.pars["MultiprocessEngine"]["do_with_log"]=True if MPE_do_with_log.get()=="True" else False
			self.tkobj.io_recv("Updated MultiprocessEngine-do_with_log to",self.pars["MultiprocessEngine"]["do_with_log"])
		self.pars["MultiprocessEngine"]["do_with_log"]=True if MPE_do_with_log.get()=="True" else False
		button_do_with_log=Button(box,text="Update",width=5)
		button_do_with_log.bind("<ButtonRelease>",fun_button_do_with_log)
		button_do_with_log.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Log file",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_logfile=Entry(box,width=15)
		MPE_logfile.insert(0,str(None))
		MPE_logfile.pack(side="left")
		def fun_selete_logfile(event):
			folder_path=filedialog.asksaveasfilename()
			if folder_path!="":update_entry(MPE_logfile,folder_path,False)
		button=Button(box,text="Select",width=5)
		button.bind("<ButtonRelease>",fun_selete_logfile)
		button.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_logfile(event):
			if MPE_logfile.get()!="":
				self.pars["MultiprocessEngine"]["logfile"]=None if MPE_logfile.get()=="None" else MPE_logfile.get()
				self.tkobj.io_recv("Updated MultiprocessEngine-logfile to",self.pars["MultiprocessEngine"]["logfile"])
		self.pars["MultiprocessEngine"]["logfile"]=None if MPE_logfile.get()=="None" else MPE_logfile.get()
		button_logfile=Button(box,text="Update",width=5)
		button_logfile.bind("<ButtonRelease>",fun_logfile)
		button_logfile.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Show MPE info",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_show_version_info=ttk.Combobox(box,width=18,height=2,values=[True,False])
		MPE_show_version_info.set(str(True))
		MPE_show_version_info.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_show_version_info(event): 
			self.pars["MultiprocessEngine"]["show_version_info"]=True if MPE_show_version_info.get()=="True" else False
			self.tkobj.io_recv("Updated MultiprocessEngine-show_version_info to",self.pars["MultiprocessEngine"]["show_version_info"])
		button_show_version_info=Button(box,text="Update",width=5)
		button_show_version_info.bind("<ButtonRelease>",fun_show_version_info)
		button_show_version_info.pack(side="left")
		self.pars["MultiprocessEngine"]["show_version_info"]=True if MPE_show_version_info.get()=="True" else False
		Label(self.add_row(MPE,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(MPE,bx=150)
		Label(box,text="Show log in screen",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_print_in_screen=ttk.Combobox(box,width=18,height=2,values=[True,False])
		MPE_print_in_screen.set(str(True))
		MPE_print_in_screen.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_sprint_in_screen(event): 
			self.pars["MultiprocessEngine"]["print_in_screen"]=True if MPE_print_in_screen.get()=="True" else False
			self.tkobj.io_recv("Updated MultiprocessEngine-print_in_screen to",self.pars["MultiprocessEngine"]["print_in_screen"])
		self.pars["MultiprocessEngine"]["print_in_screen"]=True if MPE_print_in_screen.get()=="True" else False
		button_print_in_screen=Button(box,text="Update",width=5)
		button_print_in_screen.bind("<ButtonRelease>",fun_sprint_in_screen)
		button_print_in_screen.pack(side="left")
		Label(self.add_row(MPE,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
		def fun_reset(Engine=None,pnum=None,do_with_log=None,logfile=None,show_version_info=None,print_in_screen=None):
			if Engine:
				MPE_ENG.set(Engine)
				fun_mpeeng(None)
			if pnum:
				update_entry(MPE_PNUM,pnum,False)
				fun_MPE_PNUM(None)
			if do_with_log:
				MPE_do_with_log.set(do_with_log)
				fun_button_do_with_log(None)
			if logfile:
				update_entry(MPE_logfile,logfile,False)
				fun_logfile(None)
			if show_version_info:
				MPE_show_version_info.set(show_version_info)
				fun_show_version_info(None)
			if print_in_screen:
				MPE_print_in_screen.set(print_in_screen)
				fun_sprint_in_screen(None)
		self.con_MultiprocessEngine=fun_reset
	def GS_IO(self):
		#Loader
		IO=self.add_menu("Database Storage",submenu=1)
		self.pars["IO"]={}
		self.add_row(IO) #skip row (empty row)
		self.add_title(IO,"After-Analysis Data Storage")
		Label(self.add_row(IO,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(IO,bx=150)
		Label(box,text="Engine",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		IO_ENG=ttk.Combobox(box,width=18,height=5,values=list(self.pageargs["Infobj"].Config["IO"].keys()))
		if self.pageargs["Infobj"].Default_IO in self.pageargs["Infobj"].Config["IO"]:
			IO_ENG.set(self.pageargs["Infobj"].Default_IO)
		else:
			IO_ENG.set(list(self.pageargs["Infobj"].Config["IO"].keys())[0])
		IO_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_IO_ENG(event):
			self.pars["IO"]["Engine"]=IO_ENG.get()
			self.tkobj.io_recv("Updated IO-Engine to",self.pars["IO"]["Engine"])
		button_IO_ENG=Button(box,text="Update",width=5)
		button_IO_ENG.bind("<ButtonRelease>",fun_IO_ENG)
		button_IO_ENG.pack(side="left")
		self.pars["IO"]["Engine"]=IO_ENG.get()
		Label(self.add_row(IO,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(IO,bx=150)
		Label(box,text="Project name",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		IO_filename=Entry(box,width=15)
		IO_filename.pack(side="left")
		def fun_lfd(event):
			folder_path=filedialog.asksaveasfilename()
			if folder_path!="":
				IO_filename.delete(0,"end")
				IO_filename.insert(0,folder_path)
		button=Button(box,text="Select",width=5)
		button.bind("<ButtonRelease>",fun_lfd)
		button.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_filename(event):
			if IO_filename.get()!="":
				self.pars["IO"]["filename"]=IO_filename.get()
				self.tkobj.io_recv("Updated IO-filename to",self.pars["IO"]["filename"])
			else:
				if "filename" in self.pars["IO"].keys():
					del(self.pars["IO"])
		button_filename=Button(box,text="Update",width=5)
		button_filename.bind("<ButtonRelease>",fun_filename)
		button_filename.pack(side="left")
		if IO_filename.get()!="":self.pars["IO"]["filename"]=IO_filename.get()
		Label(self.add_row(IO,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(IO,bx=150)
		Label(box,text="Drop Buffer",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		IO_DropBuffer=ttk.Combobox(box,width=18,height=2,values=[True,False])
		IO_DropBuffer.set(str(True))
		IO_DropBuffer.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_DropBuffer(event): 
			self.pars["IO"]["DropBuffer"]=True if IO_DropBuffer.get()=="True" else False
			self.tkobj.io_recv("Updated IO-DropBuffer to",self.pars["IO"]["DropBuffer"])
		self.pars["IO"]["DropBuffer"]=True if IO_DropBuffer.get()=="True" else False
		button_DropBuffer=Button(box,text="Update",width=5)
		button_DropBuffer.bind("<ButtonRelease>",fun_DropBuffer)
		button_DropBuffer.pack(side="left")
		Label(self.add_row(IO,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
		def fun_reset(Engine=None,filename=None,DropBuffer=None):
			if Engine:
				IO_ENG.set(Engine)
				fun_IO_ENG(None)
			if filename:
				update_entry(IO_filename,filename,False)
				fun_filename(None)
			if DropBuffer:
				update_entry(IO_DropBuffer,DropBuffer,False)
				fun_DropBuffer(None)
		self.con_IO=fun_reset
	def GS_Loader(self):
		#Loader
		Loader=self.add_menu("Simulation Data Loader",submenu=1)
		self.pars["Loader"]={}
		self.add_row(Loader) #skip row (empty row)
		self.add_title(Loader,"Simulation Data Loader")
		Label(self.add_row(Loader,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(Loader,bx=150)
		Label(box,text="Type",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		Loader_ENG=ttk.Combobox(box,width=18,height=5,values=list(self.pageargs["Infobj"].Config["Loader"].keys()))
		Loader_ENG.set(list(self.pageargs["Infobj"].Config["Loader"].keys())[0])
		Loader_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_ENG(event):
			self.pars["Loader"]["Engine"]=Loader_ENG.get()
			self.tkobj.io_recv("Updated Loader-Engine to",self.pars["Loader"]["Engine"])
		button_fun_Loader_ENG=Button(box,text="Update",width=5)
		button_fun_Loader_ENG.bind("<ButtonRelease>",fun_Loader_ENG)
		button_fun_Loader_ENG.pack(side="left")
		self.pars["Loader"]["Engine"]=Loader_ENG.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="File Dir",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_FileDir=Entry(box,width=15)
		Loader_FileDir.insert(0,os.getcwd())
		Loader_FileDir.pack(side="left")
		def fun_lfd(event):
			folder_path=filedialog.askdirectory()
			if folder_path!="":
				Loader_FileDir.delete(0,"end")
				Loader_FileDir.insert(0,folder_path)
		button=Button(box,text="Select",width=5)
		button.bind("<ButtonRelease>",fun_lfd)
		button.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_FileDir(event):
			self.pars["Loader"]["FileDir"]=Loader_FileDir.get()
			self.tkobj.io_recv("Updated Loader-FileDir to",self.pars["Loader"]["FileDir"])
		button_Loader_FileDir=Button(box,text="Update",width=5)
		button_Loader_FileDir.bind("<ButtonRelease>",fun_Loader_FileDir)
		button_Loader_FileDir.pack(side="left")
		self.pars["Loader"]["FileDir"]=Loader_FileDir.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="File Prefix",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_FilePrefix=Entry(box,width=20)
		Loader_FilePrefix.insert(0,"data.")
		Loader_FilePrefix.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_FilePrefix(event):
			self.pars["Loader"]["FilePrefix"]=Loader_FilePrefix.get()
			self.tkobj.io_recv("Updated Loader-FilePrefix to",self.pars["Loader"]["FilePrefix"])
		button_Loader_FilePrefix=Button(box,text="Update",width=5)
		button_Loader_FilePrefix.bind("<ButtonRelease>",fun_Loader_FilePrefix)
		button_Loader_FilePrefix.pack(side="left")
		self.pars["Loader"]["FilePrefix"]=Loader_FilePrefix.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="File Format",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_FileFormat=Entry(box,width=20)
		Loader_FileFormat.insert(0,"04d")
		Loader_FileFormat.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_FileFormat(event):
			self.pars["Loader"]["FileFormat"]=Loader_FileFormat.get()
			self.tkobj.io_recv("Updated Loader-Format to",self.pars["Loader"]["FileFormat"])
		button_Loader_FileFormat=Button(box,text="Update",width=5)
		button_Loader_FileFormat.bind("<ButtonRelease>",fun_Loader_FileFormat)
		button_Loader_FileFormat.pack(side="left")
		self.pars["Loader"]["FileFormat"]=Loader_FileFormat.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="File type",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_Filetype=Entry(box,width=20)
		Loader_Filetype.insert(0,"dbl")
		Loader_Filetype.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_Filetype(event):
			self.pars["Loader"]["Filetype"]=Loader_Filetype.get()
			self.tkobj.io_recv("Updated Loader-Filetype to",self.pars["Loader"]["Filetype"])
		button_Loader_Filetype=Button(box,text="Update",width=5)
		button_Loader_Filetype.bind("<ButtonRelease>",fun_Loader_Filetype)
		button_Loader_Filetype.pack(side="left")
		self.pars["Loader"]["FileType"]=Loader_Filetype.get()
		Label(self.add_row(Loader,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(Loader,bx=150)
		Label(box,text="Interval",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		Loader_InterVal=Entry(box,width=20)
		Loader_InterVal.insert(0,1)
		Loader_InterVal.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_Loader_InterVal(event):
			self.pars["Loader"]["Interval"]=int(Loader_InterVal.get())
			self.tkobj.io_recv("Updated Loader-Interval to",self.pars["Loader"]["Interval"])
		button_Loader_InterVal=Button(box,text="Update",width=5)
		button_Loader_InterVal.bind("<ButtonRelease>",fun_Loader_InterVal)
		button_Loader_InterVal.pack(side="left")
		self.pars["Loader"]["Interval"]=int(Loader_InterVal.get())
		Label(self.add_row(Loader,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
		def fun_reset(Engine=None,FileDir=None,FilePrefix=None,FileFormat=None,FileType=None,Interval=None):
			if Engine:Loader_ENG.set(Engine)
			else:Loader_ENG.set(list(self.pageargs["Infobj"].Config["Loader"].keys())[0])
			fun_Loader_ENG(None)
			if FileDir:
				update_entry(Loader_FileDir,FileDir,False)
				fun_Loader_FileDir(None)
			if FileType:
				update_entry(Loader_Filetype,FileType,False)
				fun_Loader_Filetype(None)
			if FilePrefix:
				update_entry(Loader_FilePrefix,FilePrefix,False)
				fun_Loader_FilePrefix(None)
			if FileFormat:
				update_entry(Loader_FileFormat,FileFormat,False)
				fun_Loader_FileFormat(None)
			if Interval:
				update_entry(Loader_InterVal,Interval,False)
				fun_Loader_InterVal(None)
		self.con_Loader=fun_reset
	def A_Parameters(self):
		#Parameters
		Parameters=self.add_menu("Parameters",submenu=1)
		self.pars["Update"]={}
		self.add_row(Parameters) #skip row (empty row)
		self.add_title(Parameters,"Parameters")
		Label(self.add_row(Parameters,bx=190),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(Parameters,bx=190)
		Label(box,text="Parameter Name",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Parameter Value",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Opera",width=5,fg="green").pack(side="left")
		keys=set(self.pageargs["Infobj"].testdb.data[0].quantities.keys())-set(("vx1","vx2","vx3","SimTime","geometry","rho","prs","Bx1","Bx2","Bx3","output","logfile"))
		def fun(box,entry1,entry2,button,value=None):
			def fun_del(event):
				if entry1.get()!="":
					try:
						del(self.pars["Update"][entry1.get()])
						self.tkobj.io_recv("Delete parameter",entry1.get())
					except:
						if event:self.tkobj.io_recv("Warning: parameter",entry1.get(),"dosen't exist!!!",color="blue")
				entry1.config(state="normal")
				entry2.config(state="normal")
				button.config(text="Save")
				button.bind("<ButtonRelease>",fun_cre)
			def fun_cre(event):
				if entry1.get()!="":
					update_entry(entry1,str_clean(entry1.get()))
					update_entry(entry2,str_clean(entry2.get()))
					self.pars["Update"][entry1.get()]=str_to_float(entry2.get())
					self.tkobj.io_recv("Add parameter",entry1.get(),"to",self.pars["Update"][entry1.get()])
					button.config(text="Modify")
					button.bind("<ButtonRelease>",fun_del)
			def fun_reset(key,value):
				fun_del(None)
				update_entry(entry1,"",False)
				update_entry(entry2,"",False)
				if key!="":
					update_entry(entry1,key)
					update_entry(entry2,value)
					fun_cre(None)
			if entry1.get()!="":# normal
				if value!=None:
					entry2.insert(0,str(value))
				else:
					try:
						entry2.insert(0,str(self.pageargs["Infobj"].testdb.data[0].quantities[entry1.get()]))
					except Exception as err:
						print(err)
				self.pars["Update"][entry1.get()]=str_to_float(entry2.get())
				entry1.config(state="readonly")
				entry2.config(state="readonly")
				button.config(text="Modify")
				button.bind("<ButtonRelease>",fun_del)
			else:
				button.config(text="Save")
				button.bind("<ButtonRelease>",fun_cre)
			return fun_reset
		self.con_Update=[]
		for i in range(self.parmax):
			Label(self.add_row(Parameters,bx=190),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(Parameters,bx=190)
			entry1=Entry(box,width=20)
			if i < len(keys):
				entry1.insert(0,list(keys)[i])
			entry1.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry2=Entry(box,width=20)
			entry2.pack(side="left")
			Label(box,text="| ").pack(side="left")
			button=Button(box,width=5)
			button.pack(side="left")
			self.con_Update.append(fun(box,entry1,entry2,button))
		Label(self.add_row(Parameters,bx=190),text="="*500).place(x=0,y=0,anchor="nw") #end
	def A_Quantities(self):
		Quantities=self.add_menu("Quantities",submenu=1)
		self.add_row(Quantities) #skip row (empty row)
		self.add_title(Quantities,"Quantities")
		Label(self.add_row(Quantities,bx=20),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(Quantities,bx=20)
		Label(box,text="Approach",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Target Quantity",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Saved Result",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Arguments",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Opera",width=5,fg="green").pack(side="left")
		operationlist=list(self.pageargs["Infobj"].Config["AnalysisTool"].keys())+["Gradient","Divergence","Harmonic","Mean","Radial"]
		def get_result(qtname,qto):
			result=""
			try:
				result=self.pageargs["Infobj"].Config["AnalysisTool"][qto].result(qtname,qto)
				if len(result)==1:
					result=result[0]
				else:
					result=str(result)
			except:
				if qto in ("Gradient","Divergence"):
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Differential"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
				elif qto=="Harmonic":
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Harmonic_src"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
				elif qto=="Mean":
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Mean_src"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
				elif qto=="Radial":
					result=self.pageargs["Infobj"].Config["AnalysisLib"]["Radial_src"].result(qtname,qto)
					if len(result)==1:
						result=result[0]
					else:
						result=str(result)
			return strc_vva(result)
		def strc_vva(result):
			return result.replace("(","").replace(")","").replace("[","").replace("]","").replace("\'","").replace("\"","")
		def fun(index,box,cmbox1,entry2,entry3,entry4,button5,button6):
			def fun_set(event): update_entry(entry3,get_result(entry2.get().replace(" ",""),cmbox1.get()).replace(" ",""),False)
			def fun_cre(event):
				if cmbox1.get()!="":
					update_entry(entry2,str_clean(entry2.get()))
					update_entry(entry3,str_clean(entry3.get()))
					update_entry(entry4,str_clean(entry4.get()))
					self.pars[f"{index}_{cmbox1.get()}"]={}
					if strc_vva(entry2.get())!="":
						self.pars[f"{index}_{cmbox1.get()}"]["quantity_name"]=strc_vva(entry2.get())
					if strc_vva(entry3.get())!="":
						self.pars[f"{index}_{cmbox1.get()}"]["result"]=strc_vva(entry3.get())
					for i in entry4.get().split(";"):
						if i!="":
							vi=i.split("=")
							if len(vi)==2:
								qu,qv=vi
								self.pars[f"{index}_{cmbox1.get()}"][qu]=qv.replace(" ","")
							else: self.tkobj.io_recv("Warning: arguments decode error:",i,color="blue")
					self.tkobj.io_recv("Add approach",cmbox1.get(),";",self.pars[f"{index}_{cmbox1.get()}"])
					cmbox1.config(state="disable")
					button6.config(text="Modify")
					button6.bind("<ButtonRelease>",fun_del)
			def fun_del(event):
				if cmbox1.get()!="":
					try:
						del(self.pars[f"{index}_{cmbox1.get()}"])
						self.tkobj.io_recv("Delete approach",cmbox1.get())
					except:
						if event:self.tkobj.io_recv("Warning: approach",cmbox1.get(),"dosen't exist!!!",color="blue")
				cmbox1.config(state="normal")
				entry2.config(state="normal")
				entry3.config(state="normal")
				entry4.config(state="normal")
				button6.config(text="Save")
				button6.bind("<ButtonRelease>",fun_cre)
			def fun_reset(app,quantity_name,result,arguments):
				fun_del(None)
				cmbox1.set("")
				update_entry(entry2,"",False)
				update_entry(entry3,"",False)
				update_entry(entry4,"",False)
				if app!="":
					cmbox1.set(app)
					update_entry(entry2,quantity_name)
					update_entry(entry3,result)
					arg=""
					for key,value in arguments.items():arg+=f"{key}={value};"
					update_entry(entry4,arg)
					fun_cre(None)
			button5.bind("<ButtonRelease>",fun_set)
			button6.bind("<ButtonRelease>",fun_cre)
			return fun_reset
		self.con_Approaches=[]
		for i in range(self.parmax):
			Label(self.add_row(Quantities,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(Quantities,bx=20)
			cmbox1=ttk.Combobox(box,width=18,height=len(operationlist) if len(operationlist)<=10 else 10,values=operationlist)
			cmbox1.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry2=Entry(box,width=20)
			entry2.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry3=Entry(box,width=14)
			entry3.pack(side="left")
			button5=Button(box,text="Get",width=5)
			button5.pack(side="left")
			Label(box,text="| ").pack(side="left")
			entry4=Entry(box,width=20)
			entry4.pack(side="left")
			Label(box,text="| ").pack(side="left")
			button6=Button(box,text="Save",width=5)
			button6.pack(side="left")
			self.con_Approaches.append(fun(i,box,cmbox1,entry2,entry3,entry4,button5,button6))
		Label(self.add_row(Quantities,bx=20),text="="*500).place(x=0,y=0,anchor="nw") #end
	def save(self):
		save=self.add_menu("Save Configuration")
		self.add_row(save) #skip row (empty row)
		self.add_title(save,"Save Configuration")
		box=self.add_row(save,bx=260)
		def Load(event):
			file_path=filedialog.askopenfilename()
			if file_path!="":
				cfg=get_config(file_path)
				try:del cfg["Test"]
				except:pass
				anafs=[]
				for key,value in cfg.items():
					if key in ("MultiprocessEngine","IO","Loader"): eval(f"self.con_{key}(**value)")
					elif key == "Update":
						vl=list(value.items())
						vl+=[("","")]*(self.parmax-len(vl))
						for i in range(self.parmax):self.con_Update[i](*vl[i])
					else: 
						anaf={"app":key,"quantity_name":"","result":"","arguments":{}}
						for k,v in value.items():
							if k in ("quantity_name","result"):
								if type(v) not in (tuple,list):anaf[k]=v
								else:
									vv=""
									for s in v:vv+=f"{s},"
									anaf[k]=vv[:-1] if vv!="" else ""
							else: 
								if type(v) not in (tuple,list):anaf["arguments"][k]=v
								else:
									vv=""
									for s in v:vv+=f"{s},"
									anaf["arguments"][k]=vv[:-1] if vv!="" else ""
						anafs.append(anaf)
				anafs+=[{"app":"","quantity_name":"","result":"","arguments":{}}]*(self.parmax-len(anafs))
				for i in range(self.parmax):self.con_Approaches[i](**anafs[i])
		button=Button(box,text="Load",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",Load)
		Label(box,width=6).pack(side="left")
		def get_anafs(): 
			def get_key(key):
				newkey=""
				for s in key.split("_")[1:]: newkey+=f"_{s}"
				return newkey[1:] if newkey!="" else newkey
			newdicts= {key:value for key,value in self.pars.items() if key not in ("MultiprocessEngine","IO","Loader","Update")}
			sorted_keys=sorted(newdicts.keys(),key=lambda x:int(x.split("_")[0]))
			return {get_key(key): newdicts[key] for key in sorted_keys}
		def Test(event):
			grids=[]
			for i in (grid_x1.get(),grid_x2.get(),grid_x3.get()):
				if i not in ("","None","0"):grids.append(int(i))
			grids=tuple(grids)
			grids_map=((str_to_float(x1_beg.get()),str_to_float(x1_end.get())),(str_to_float(x2_beg.get()),str_to_float(x2_end.get())),(str_to_float(x3_beg.get()),str_to_float(x3_end.get())))[:len(grids)]
			self.tkobj.io_recv("Got Test Data infomation:")
			self.tkobj.io_recv("Geometry:",geometry.get(),color="blue")
			gridsinfo=""
			for i in grids:gridsinfo+=str(i)+" X "
			if gridsinfo!="":gridsinfo=gridsinfo[:-3]
			self.tkobj.io_recv("Grids:",gridsinfo,"("+str(len(grids_map))+"d)",color="blue")
			for i in range(len(grids_map)): self.tkobj.io_recv("x"+str(i+1)+": From",grids_map[i][0],"To",grids_map[i][1],color="blue")
			self.tkobj.io_recv("Creating Test Database...")
			self.pageargs["Infobj"].setup_testdb(geometry=geometry.get(),grids=grids,grids_map=grids_map)
			self.tkobj.io_recv(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			self.tkobj.io_recv("Got Commands:")
			for key,value in self.pars.items():self.tkobj.io_recv(key,":",value,color="blue")
			self.tkobj.io_recv(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
			self.pageargs["Infobj"].testdb.update(**self.pars["Update"])
			self.tkobj.io_recv("Ready for testing..............")
			for key,value in get_anafs().items():
				try:anaf=self.pageargs["Infobj"].Config["AnalysisTool"][key].get
				except:
					try:anaf=self.pageargs["Infobj"].Config["AnalysisLib"][key]
					except:
						self.tkobj.io_recv("Unknown approach:",key,color="red")
						continue
				pas=copy.deepcopy(value)
				pas.update({"info":key})
				for j in pas:pas[j]=retype_string(pas[j])
				self.pageargs["Infobj"].testdb.analysis_data(anaf,**pas)
				if "result" in pas: self.pageargs["Infobj"].testdb.check_quantities(pas["result"])
			self.tkobj.io_recv("Operation completed",color="green")
		button=Button(box,text="Test",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",Test)
		def Save(event):
			file=filedialog.asksaveasfile()
			if file!=None:
				self.tkobj.io_recv("Collecting Parameters:")
				for key,value in self.pars.items():self.tkobj.io_recv(key,":",value)
				self.tkobj.io_recv("Saving to file @",file)
				strc="#ShockFinder Analyzing Configurations\n"
				try:strc+="#Built at "+Time.now()+"\n"
				except:pass
				strc+="#Wacmk.cn/com\n"
				strc+="#https://www.github.com/wacmkxiaoyi/shockfinder\n\n"
				#write MPE
				for key in ("MultiprocessEngine","IO","Loader","Update"):#maintain sequency
					if key in self.pars:
						strc+=key
						for k,v in self.pars[key].items(): strc+=f";{k}={v}"
						strc+=";\n"
				for key,value in get_anafs().items():
					strc+=key
					for k,v in value.items():strc+=f";{k}={v}"
					strc+=";\n"
				file.writelines(strc)
				file.close()
				self.tkobj.io_recv("Operation completed",color="green")
		Label(box,width=6).pack(side="left")
		button=Button(box,text="Save",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",Save)
		self.add_row(save)
		self.add_title(save,"Test Parameters",fg="green",fontsize=22)
		Label(self.add_row(save,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #begin
		box=self.add_row(save,bx=250)
		Label(box,text="Geometry").pack(side="left")
		Label(box,text="|").pack(side="left")
		geometry=ttk.Combobox(box,width=18,values=("SPHERICAL","POLAR","CYLINDRICAL","CARTESIAN"))
		geometry.set("SPHERICAL")
		geometry.pack(side="left")
		Label(box,text="|").pack(side="left")
		def save_geo(event=None):
			defaultinfo=self.pageargs["Infobj"].Config["AnalysisLib"]["TestData"].grids_default[geometry.get()]
			#x1
			try:
				update_entry(grid_x1,self.pageargs["Infobj"].Config["AnalysisLib"]["TestData"].grids_default_num[0],False)
			except:
				pass
			try:
				update_entry(x1_beg,defaultinfo[0][0],False)
			except:
				pass
			try:
				update_entry(x1_end,defaultinfo[0][1],False)
			except:
				pass

			#x2
			try:
				update_entry(grid_x2,self.pageargs["Infobj"].Config["AnalysisLib"]["TestData"].grids_default_num[1],False)
			except:
				pass
			try:
				update_entry(x2_beg,defaultinfo[1][0],False)
			except:
				pass
			try:
				update_entry(x2_end,defaultinfo[1][1],False)
			except:
				pass

			#x3
			try:
				update_entry(grid_x3,self.pageargs["Infobj"].Config["AnalysisLib"]["TestData"].grids_default_num[2],False)
			except:
				pass
			try:
				update_entry(x3_beg,defaultinfo[2][0],False)
			except:
				pass
			try:
				update_entry(x3_end,defaultinfo[2][1],False)
			except:
				pass
		button_geo=Button(box,text="Save")
		button_geo.pack(side="left")
		button_geo.bind("<ButtonRelease>",save_geo)
		
		Label(self.add_row(save,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(save,bx=150)
		Label(box,text="Grid_x1").pack(side="left")
		Label(box,text="|").pack(side="left")
		grid_x1=Entry(box,width=10)
		grid_x1.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="From ").pack(side="left")
		x1_beg=Entry(box,width=15)
		x1_beg.pack(side="left")
		Label(box,text=" to ").pack(side="left")
		x1_end=Entry(box,width=15)
		x1_end.pack(side="left")
		Label(self.add_row(save,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(save,bx=150)
		Label(box,text="Grid_x2").pack(side="left")
		Label(box,text="|").pack(side="left")
		grid_x2=Entry(box,width=10)
		grid_x2.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="From ").pack(side="left")
		x2_beg=Entry(box,width=15)
		x2_beg.pack(side="left")
		Label(box,text=" to ").pack(side="left")
		x2_end=Entry(box,width=15)
		x2_end.pack(side="left")
		Label(self.add_row(save,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(save,bx=150)
		Label(box,text="Grid_x3").pack(side="left")
		Label(box,text="|").pack(side="left")
		grid_x3=Entry(box,width=10)
		grid_x3.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="From ").pack(side="left")
		x3_beg=Entry(box,width=15)
		x3_beg.pack(side="left")
		Label(box,text=" to ").pack(side="left")
		x3_end=Entry(box,width=15)
		x3_end.pack(side="left")
		Label(self.add_row(save,bx=150),text="="*500).place(x=0,y=0,anchor="nw") #end
		save_geo()
	def initial(self):
		self.set_image(self.img["logo"])
		self.save()
		self.add_useless_menu("Global Settings↓")
		self.GS_MPE()
		self.GS_IO()
		self.GS_Loader()
		self.add_useless_menu("Analysis↓")
		self.A_Parameters()
		self.A_Quantities()