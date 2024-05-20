#XUI V1.0
#Junxiang H. 2023.03.07
import psutil,threading,time,os
from tkinter import *
from tkinter import ttk
try:
	from ShockFinder.Addon.GUI.XUIlib.imgtool import add_image
	from ShockFinder.Addon.GUI.XUIlib.progress import progress
	cpuboxshower_logo=os.path.join("ShockFinder","Addon","GUI","XUIlib","image","cpu.jpeg")
	ramboxshower_logo=os.path.join("ShockFinder","Addon","GUI","XUIlib","image","ram.png")
	diskboxshower_logo=os.path.join("ShockFinder","Addon","GUI","XUIlib","image","disk.jpeg")
except:
	from XUIlib.imgtool import add_image
	from XUIlib.progress import progress
	cpuboxshower_logo=os.path.join("XUIlib","image","cpu.jpeg")
	ramboxshower_logo=os.path.join("XUIlib","image","ram.png")
	diskboxshower_logo=os.path.join("XUIlib","image","disk.jpeg")
def get_cpu():
	result={"total":psutil.cpu_percent()}
	tmp=psutil.cpu_percent(percpu=True)
	for i in range(len(tmp)):
		result[i]=tmp[i]
	return result
def get_memory():
	#total, available, percent
	tmp=psutil.virtual_memory()
	tmpv=psutil.swap_memory()
	result={
		"phi_total":tmp.total,
		"phi_used":tmp.used,
		"phi_percent":tmp.percent,
		"v_total":tmpv.total,
		"v_used":tmpv.used,
		"v_percent":tmpv.percent,
		"total":tmp.total+tmpv.total,
		"used":tmp.used+tmpv.used,
		"percent":round((tmp.used+tmpv.used)/(tmp.total+tmpv.total)*100,2)
	}
	return result
def get_disk():
	result={}
	for i in psutil.disk_partitions():
		tmp=psutil.disk_usage(i.device)
		result[i.device]={
			"total":tmp.total,
			"used":tmp.used,
			"percent":tmp.percent
		}
	tmp_t=0
	tmp_u=0
	for i in result.keys():
		tmp_t+=result[i]["total"]
		tmp_u+=result[i]["used"]
	result["total"]={"total":tmp_t,"used":tmp_u,"percent":round(tmp_u/tmp_t*100,2)}
	return result
def unit_change(value):
	if value<1024:
		return str(value)
	elif value<1024**2:
		return str(round(value/1024,2))+"KB"
	elif value<1024**3:
		return str(round(value/1024**2,2))+"MB"
	elif value<1024**4:
		return str(round(value/1024**3,2))+"GB"
	elif value<1024**5:
		return str(round(value/1024**4,2))+"TB"
	elif value<1024**6:
		return str(round(value/1024**5,2))+"PB"
	return str(round(value/1024**6,2))+"EB"
class SystemInfo:
	def __init__(self,tkobj):
		self.tkobj=tkobj
	def lunch(self,refresh=None):
		self.refresh=refresh
		self.select_refresh()
		self.cpu()
		self.ram()
		self.disk()
		self.run=True
		threading.Thread(target=self.auto_update).start()
	def update(self):
		#cpu
		cpuinfo=get_cpu()
		self.cpuboxshower_label.config(text=" CPU: ("+str(cpuinfo["total"])+"%)")
		reqw=max(self.cpuboxshower_box_oriwidth,self.cpuboxshower_logo.winfo_reqwidth()+self.cpuboxshower_label.winfo_reqwidth())
		self.cpuboxshower_box.config(width=reqw)
		self.cpuboxshower.config(width=reqw+self.cpuboxshower_oriwidth-self.cpuboxshower_box_oriwidth)
		reqw=0
		for i in range(len(self.cpus_progress)):
			reqw=max(reqw,180+self.cpus_progress[i].set_pro(cpuinfo[i],sr=""))
		reqw=max(self.cpus_box_oriwidth,reqw)
		self.cpus_box.config(width=reqw)
		self.cpus.config(width=reqw+self.cpus_oriwidth-self.cpus_box_oriwidth)

		#ram
		raminfo=get_memory()
		self.ramboxshower_label.config(text=" RAM: ("+unit_change(raminfo["used"])+"/"+unit_change(raminfo["total"])+", "+str(raminfo["percent"])+"%)")
		reqw=max(self.ramboxshower_box_oriwidth,self.ramboxshower_logo.winfo_reqwidth()+self.ramboxshower_label.winfo_reqwidth())
		self.ramboxshower_box.config(width=reqw)
		self.ramboxshower.config(width=reqw+self.ramboxshower_oriwidth-self.ramboxshower_box_oriwidth)
		reqw=max(self.rams_box_oriwidth,180+self.ram_phi_progress.set_pro(raminfo["phi_percent"],total=unit_change(raminfo["phi_total"]),used=unit_change(raminfo["phi_used"])),180+self.ram_v_progress.set_pro(raminfo["v_percent"],total=unit_change(raminfo["v_total"]),used=unit_change(raminfo["v_used"])))
		self.rams_box.config(width=reqw)
		self.rams.config(width=reqw+self.rams_oriwidth-self.rams_box_oriwidth)

		#disk
		dkinfo=get_disk()
		self.diskboxshower_label.config(text=" Disks: ("+unit_change(dkinfo["total"]["used"])+"/"+unit_change(dkinfo["total"]["total"])+", "+str(dkinfo["total"]["percent"])+"%)")
		reqw=max(self.diskboxshower_oriwidth,self.diskboxshower_logo.winfo_reqwidth()+self.diskboxshower_label.winfo_reqwidth())
		self.diskboxshower_box.config(width=reqw)
		self.diskboxshower.config(width=reqw+self.diskboxshower_oriwidth-self.diskboxshower_box_oriwidth)
		reqw=0
		n=0
		for i in dkinfo.keys():
			if i!="total":
				reqw=max(reqw,180+self.disks_progress[n].set_pro(dkinfo[i]["percent"],total=unit_change(dkinfo[i]["total"]),used=unit_change(dkinfo[i]["used"])))
				n+=1
		reqw=max(self.disks_box_oriwidth,reqw)
		self.disks_box.config(width=reqw)
		self.disks.config(width=reqw+self.disks_oriwidth-self.disks_box_oriwidth)
	def cpu(self):
		self.cpuboxshower,self.cpuboxshower_box=self.tkobj.add_item(self.tkobj.cpu,height=50)
		self.cpuboxshower_box.config(cursor="hand2")
		self.cpuboxshower_logo=Label(self.cpuboxshower_box,bd=0)
		self.cpuboxshower_logo.place(x=0,y=0,anchor="nw")
		self.cpuboxshower_label=Label(self.cpuboxshower_box)
		self.cpuboxshower_label.place(x=40,y=5,anchor="nw")
		self.cpus_info()
		def show_cpus_info(event=None):
			if self.cpus_show:
				self.cpus.pack_forget()
				self.cpus_show=False
			else:
				self.cpus_show=True
				self.ramboxshower.pack_forget()
				self.rams.pack_forget()
				self.diskboxshower.pack_forget()
				self.disks.pack_forget()
				self.cpus.pack(anchor="nw")
				self.ramboxshower.pack(anchor="nw")
				if self.rams_show:
					self.rams.pack(anchor="nw")
				self.diskboxshower.pack(anchor="nw")
				if self.disks_show:
					self.disks.pack(anchor="nw")
		add_image(self.cpuboxshower_logo,cpuboxshower_logo,30,30,"<Button-1>",show_cpus_info)
		self.cpuboxshower_box.bind("<Button-1>",show_cpus_info)
		self.cpuboxshower_label.bind("<Button-1>",show_cpus_info)
		self.cpuboxshower_box_oriwidth=self.cpuboxshower_box.winfo_reqwidth()
		self.cpuboxshower_oriwidth=self.cpuboxshower.winfo_reqwidth()
	def cpus_info(self):
		cpunum=len(tuple(get_cpu().keys()))-1
		self.cpus,self.cpus_box=self.tkobj.add_item(self.tkobj.cpu,height=50*cpunum)
		self.cpus_progress=[]
		for i in range(cpunum):
			Label(self.cpus_box,text="CPU"+str(i)+":").place(x=0,y=i*50,anchor="nw")
			pp=Frame(self.cpus_box,width=12*10,height=24)
			pp.place(x=50,y=i*50,anchor="nw")
			pt=Label(self.cpus_box)
			pt.place(x=180,y=i*50,anchor="nw")
			self.cpus_progress.append(progress(pp,pt,12,24))
		self.cpus.pack_forget()
		self.cpus_show=False
		self.cpus_oriwidth=self.cpus.winfo_reqwidth()
		self.cpus_box_oriwidth=self.cpus_box.winfo_reqwidth()
	def ram(self):
		self.ramboxshower,self.ramboxshower_box=self.tkobj.add_item(self.tkobj.cpu,height=50)
		self.ramboxshower_box.config(cursor="hand2")
		self.ramboxshower_logo=Label(self.ramboxshower_box,bd=0)
		self.ramboxshower_logo.place(x=0,y=0,anchor="nw")
		self.ramboxshower_label=Label(self.ramboxshower_box)
		self.ramboxshower_label.place(x=40,y=5,anchor="nw")
		self.rams_info()
		def show_rams_info(event=None):
			if self.rams_show:
				self.rams.pack_forget()
				self.rams_show=False
			else:
				self.rams_show=True
				self.diskboxshower.pack_forget()
				self.disks.pack_forget()
				self.rams.pack(anchor="nw")
				self.diskboxshower.pack(anchor="nw")
				if self.disks_show:
					self.disks.pack(anchor="nw")
		add_image(self.ramboxshower_logo,ramboxshower_logo,30,30,"<Button-1>",show_rams_info)
		self.ramboxshower_box.bind("<Button-1>",show_rams_info)
		self.ramboxshower_label.bind("<Button-1>",show_rams_info)
		self.ramboxshower_oriwidth=self.ramboxshower.winfo_reqwidth()
		self.ramboxshower_box_oriwidth=self.ramboxshower_box.winfo_reqwidth()
	def rams_info(self):
		self.rams,self.rams_box=self.tkobj.add_item(self.tkobj.cpu,height=100)
		Label(self.rams_box,text="PRAM:").place(x=0,y=0,anchor="nw")
		pp=Frame(self.rams_box,width=12*10,height=24)
		pp.place(x=50,y=0,anchor="nw")
		pt=Label(self.rams_box)
		pt.place(x=180,y=0,anchor="nw")
		self.ram_phi_progress=progress(pp,pt,12,24)
		Label(self.rams_box,text="SWAP:").place(x=0,y=50,anchor="nw")
		pp=Frame(self.rams_box,width=12*10,height=24)
		pp.place(x=50,y=50,anchor="nw")
		pt=Label(self.rams_box)
		pt.place(x=180,y=50,anchor="nw")
		self.ram_v_progress=progress(pp,pt,12,24)
		self.rams.pack_forget()
		self.rams_show=False
		self.rams_oriwidth=self.rams.winfo_reqwidth()
		self.rams_box_oriwidth=self.rams_box.winfo_reqwidth()
	def disk(self):
		self.diskboxshower,self.diskboxshower_box=self.tkobj.add_item(self.tkobj.cpu,height=50)
		self.diskboxshower_box.config(cursor="hand2")
		self.diskboxshower_logo=Label(self.diskboxshower_box,bd=0)
		self.diskboxshower_logo.place(x=0,y=0,anchor="nw")
		self.diskboxshower_label=Label(self.diskboxshower_box)
		self.diskboxshower_label.place(x=40,y=5,anchor="nw")
		self.disks_info()
		def show_disks_info(event=None):
			if self.disks_show:
				self.disks.pack_forget()
				self.disks_show=False
			else:
				self.disks_show=True
				self.disks.pack(anchor="nw")
		add_image(self.diskboxshower_logo,diskboxshower_logo,30,30,"<Button-1>",show_disks_info)
		self.diskboxshower_box.bind("<Button-1>",show_disks_info)
		self.diskboxshower_label.bind("<Button-1>",show_disks_info)
		self.diskboxshower_oriwidth=self.diskboxshower.winfo_reqwidth()
		self.diskboxshower_box_oriwidth=self.diskboxshower_box.winfo_reqwidth()
	def disks_info(self):
		dkinfo=get_disk()
		disknum=len(tuple(dkinfo.keys()))-1
		self.disks,self.disks_box=self.tkobj.add_item(self.tkobj.cpu,height=50*disknum)
		self.disks_progress=[]
		n=0
		for i in dkinfo.keys():
			if i!="total":
				Label(self.disks_box,text=i.split("\\")[0]).place(x=0,y=n*50,anchor="nw")
				pp=Frame(self.disks_box,width=12*10,height=24)
				pp.place(x=50,y=n*50,anchor="nw")
				pt=Label(self.disks_box)
				pt.place(x=180,y=n*50,anchor="nw")
				self.disks_progress.append(progress(pp,pt,12,24))
				n+=1
		self.disks.pack_forget()
		self.disks_show=False
		self.disks_oriwidth=self.disks.winfo_reqwidth()
		self.disks_box_oriwidth=self.disks_box.winfo_reqwidth()
	def select_refresh(self):
		sr,sr_box=self.tkobj.add_item(self.tkobj.cpu,height=40)
		sr_lb1=Label(sr_box,text="Refresh:")
		sr_lb1.pack(side=LEFT)
		values=[1,2,5,10,15,20,30,40,50,60,120,300,600,1800,3600]
		self.sr_combo=ttk.Combobox(sr_box,width=5,values=values)
		if self.refresh==None:
			self.sr_combo.current(2)
		else:
			n=0
			while n<len(values) and values[n]<self.refresh:
				n+=1
			if n>0:
				n-=1
			self.sr_combo.current(n)
		self.sr_combo.pack(side=LEFT)
		sr_lb2=Label(sr_box,text=" (second)")
		sr_lb2.pack(side=LEFT)
		sr_oriwidth=sr.winfo_reqwidth()
		sr_box_oriwidth=sr_box.winfo_reqwidth()
		reqw=max(sr_box_oriwidth,sr_lb1.winfo_reqwidth()+self.sr_combo.winfo_reqwidth()+sr_lb2.winfo_reqwidth())
		sr_box.config(width=reqw)
		sr.config(width=reqw+sr_oriwidth-sr_box_oriwidth)
	def auto_update(self):
		while self.run:
			try:
				self.update()
				time.sleep(int(self.sr_combo.get()))
			except:
				break
	def close(self):
		self.run=False