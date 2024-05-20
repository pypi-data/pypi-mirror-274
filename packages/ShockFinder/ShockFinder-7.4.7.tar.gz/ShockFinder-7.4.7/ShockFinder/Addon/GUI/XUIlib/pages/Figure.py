#This is a model file for XUI page
#Junxiang H. 2023.07.09
import os,numpy as np,time
from multiprocessing import cpu_count
from XenonUI.XUIlib.imgtool import add_image
from XenonUI.XUIlib.page import *
from ShockFinder.Addon.GUI.XUIlib.ShockFinderFiguresHDF5 import ShockFinderFiguresHDF5
from ShockFinder.Config import ShockFinderDir
	#logo=os.path.join("ShockFinder","Addon","GUI","XUIlib","image","F.png")
from ShockFinder.Addon.Time import now
from tkinter import *
from tkinter import ttk,filedialog
import copy

	
class page(page):
	img={
		"logo":Image_F
	}
	unit_t=None
	unit_r=None
	unit_rho=None
	unit_v=None
	avqt=[[],[],[],[]]
	avgr=[]
	usefultindex=[]
	infomation_max=100
	maxline=10
	maxcross=20
	reset_funs=[]
	def low_pass_filter(self,signal, window_size, cut):
		"""Apply a low-pass filter to the input signal."""
		if cut:
			if type(cut) not in (list,tuple):
				signal[np.where(signal>cut)]=cut
			else:
				try:
					signal[np.where(signal<cut[0])]=cut[0]
					signal[np.where(signal>cut[1])]=cut[1]
				except:
					signal[np.where(signal>cut[0])]=cut[0]
		return np.convolve(signal, np.ones(window_size)/window_size, mode='same') if window_size!=0 else signal
	def Fitting(self,lineinfo):
		x=lineinfo["x"]
		y=lineinfo["y"]
		line=[]
		def get_MARK(strc,x,y,lfi):
			if type(strc) in (list,tuple,np.ndarray):
				result=""
				for i in strc:
					result+=get_MARK(i,x,y,lfi)
				return result
			elif strc!=None and "MARK" in strc:
				return str(round(x[np.argmax(y)],2 if len(strc[4:])==0 else int(strc[4:])))
			elif strc=="lfi":
				return str(lfi)
			return strc
		def get_MARK_bottom(strc,x,y,lfi):
			if type(strc) in (list,tuple,np.ndarray):
				result=""
				for i in strc:
					result+=get_MARK(i,x,y,lfi)
				return result
			elif strc!=None and "MARK" in strc:
				return str(round(x[np.argmin(y)],2 if len(strc[4:])==0 else int(strc[4:])))
			elif strc=="lfi":
				return str(lfi)
			return strc
		def get_info(key,lfind,lineinfo,default):
			return (default if key not in lineinfo.keys() else lineinfo[key]) if key+lfind not in lineinfo.keys() else lineinfo[key+lfind]
		lf=get_info("lf","",lineinfo,"").lower()
		if lf!="manual":
			peakinfos=[]
			lfl={}
			lfc={}
			lfs={}
			lfr=get_info("lfr","",lineinfo,(x[0],x[-1]))
			autox=copy.deepcopy(x[np.where(x>=lfr[0])[0][0]:np.where(x<=lfr[1])[0][-1]+1])
			autoy=copy.deepcopy(y[np.where(x>=lfr[0])[0][0]:np.where(x<=lfr[1])[0][-1]+1])

			lfremove=get_info("lfrem","",lineinfo,())
			lfshow=get_info("lfshow","",lineinfo,"total").lower()
			#lf_min=get_info("lfmin","",lineinfo,np.min(autoy))
			#lf_max=get_info("lfmax","",lineinfo,np.max(autoy))
			checks=("debug","show","red","rem","s","l","c","r")
			def i_check(strc,checks):
				for i in checks:
					if strc[:len(i)]==i:
						return True
				return False
			def get_fitpar(ind,other={}):
				result={"name":ind}
				result.update(other)
				short={"ce":"center","am":"amplitude","sig":"sigma"}
				def parname_replace(parname):
					if parname in short.keys():
						return short[parname]
					return parname
				def rotate_set_par(pars,key,res=None):
					if res==None:
						res=result
					if len(pars)>1:
						if parname_replace(pars[0]) not in res.keys():
							res[parname_replace(pars[0])]={}
						res[parname_replace(pars[0])]=rotate_set_par(pars[1:],key,res[parname_replace(pars[0])])
					else:
						res[parname_replace(pars[0])]=lineinfo[key]
					return res
				for i in lineinfo.keys(): #gobal mode
					if "lf-"==i[:3]:#got a parameter
						pars=i.split("-")[1:]
						if len(pars)==1:
							if parname_replace(pars[0]) not in result.keys():
								result[parname_replace(pars[0])]={"value":lineinfo[i]}
							else:
								result[parname_replace(pars[0])]["value"]=lineinfo[i]
						elif len(pars)>1:
							result=rotate_set_par(pars,i)
				for i in lineinfo.keys():
					if "lf"+ind+"-"==i[:3+len(ind)]:#got a parameter
						pars=i.split("-")[1:]
						if len(pars)==1:
							if parname_replace(pars[0]) not in result.keys():
								result[parname_replace(pars[0])]={"value":lineinfo[i]}
							else:
								result[parname_replace(pars[0])]["value"]=lineinfo[i]
						elif len(pars)>1:
							result=rotate_set_par(pars,i)
				if "amplitude" not in result.keys():
					result["amplitude"]={"value":2*(np.max(autoy)-np.min(autoy))}#,"min":np.min(autoy),"max":2*np.max(autoy)}
				return result

			if lf!="auto":
				for i in lineinfo.keys():
					if "lf" in i and "lf"==i[:2] and not i_check(i[2:],checks) and "-" not in i and i!="lf":
						lfl[i[2:]]=get_info("lfl",i[2:],lineinfo,None)
						lfc[i[2:]]=get_info("lfc",i[2:],lineinfo,None)
						lfs[i[2:]]=get_info("lfs",i[2:],lineinfo,":")
						peakinfos.append(get_fitpar(i[2:],{"center":{"value":lineinfo[i]}}))
			else:
				lfreduce=get_info("lfred","",lineinfo,0.1)
				newy=copy.deepcopy(autoy)
				newy-=np.max(newy)*lfreduce
				newy[np.where(newy<0)]=0
				peaks=[]
				pb=-1
				pe=-1
				pmax=0
				pmaxind=-1
				for i in range(len(autox)):
					if newy[i]==0:
						if pe!=-1: #useful check point
							peaks.append(pmaxind)
							pe=-1#mark last check point is over
						pb=i #reset check point
						pmax=0
					elif pb!=-1: #if not begin:
						pe=i
						if newy[i]>pmax:
							pmax=newy[i]
							pmaxind=i

				stt=""
				for i in range(len(peaks)):
					stt+=str(round(autox[peaks[i]],2))+", "
					peakinfos+=[{"name":"p"+str(i),"center":{"value":autox[peaks[i]]},"amplitude":{"value":autoy[peaks[i]],"min":lf_min,"max":autoy[peaks[i]]}}]
					lfc["p"+str(i)]=get_info("lfc","p"+str(i),lineinfo,None)
					lfs["p"+str(i)]=get_info("lfs","p"+str(i),lineinfo,":")
					lfl["p"+str(i)]=get_info("lfl","p"+str(i),lineinfo,None)
				if stt!="":
					stt=stt[:-2]
					self.tkobj.io_recv("Got peaks: (",len(peaks),")",stt)
				if get_info("lfdebug","",lineinfo,False):
					line.append(self.pageargs["Infobj"].Config["Painter"]["Line"].CreateLine(**{
						"x":autox,
						"y":newy,
						"label":"debug"
						}))
					peakinfos=[]
			if len(peakinfos)!=0:
				result=self.pageargs["Infobj"].Config["Painter"]["Line"].Fitting(autox,autoy,*peakinfos)
				if lfshow in ("total","both"):
					lorlineinfo={
						"x":autox,
						"y":result.best_fit,
						"color":get_info("lfc","t",lineinfo,"red"),
						"linestyle":get_info("lfs","t",lineinfo,"--")
					}
					lorlineinfo.update({"label":get_MARK(get_info("lfl","t",lineinfo,"Fitting"),autox,result.best_fit,"Fitting")})
					line.append(self.pageargs["Infobj"].Config["Painter"]["Line"].CreateLine(**lorlineinfo))
				if lfshow in ("peak","both"):
					nn=0
					for name, comp in result.eval_components().items():
						inde=name.split("_")[0]
						if name!="BKG" and nn not in lfremove:
							lorlineinfo={
								"x":autox,
								"y":comp,
								"color":lfc[inde] if name!="BKG" else None,
								"linestyle":lfs[inde] if name!="BKG" else "--"
							}
							lorlineinfo.update({"label":get_MARK(lfl[inde] if name!="BKG" else "BKG",autox,comp,inde)})
							line.append(self.pageargs["Infobj"].Config["Painter"]["Line"].CreateLine(**lorlineinfo))
							nn+=1

			else:
				'''
				peakinfos=[{
					"name":"Main",
					"center":x[np.argmax(y)],
					"amplitude":np.max(y)-np.min(y)
				}]
				lfl["Main"]=get_info("lfl","",lineinfo,None)
				lfc["Main"]=get_info("lfc","",lineinfo,None)
				lfs["Main"]=get_info("lfs","",lineinfo,":")
				'''
				pass
		else:
			lf=False
			lfr=[]
			lfg=[]
			lfm=[]
			lfl=[]
			lfc=[]
			lfs=[]
			for i in lineinfo.keys():
				if "lf" in i and "lf"==i[:2] and i[2] not in ("c","g","l","m","s") and i!="lf":
					lfg.append(get_info("lfg",i[2:],lineinfo,"10%"))
					lfm.append(get_info("lfm",i[2:],lineinfo,"dogbox"))
					lfl.append(get_info("lfl",i[2:],lineinfo,None))
					lfc.append(get_info("lfc",i[2:],lineinfo,None))
					lfs.append(get_info("lfs",i[2:],lineinfo,":"))
					lfr.append(lineinfo[i])
			if len(lfr)!=0:
				for i in range(len(lfr)):
					lorlineinfo={
						"x":x[np.where(x>=lfr[i][0])[0][0]:np.where(x<=lfr[i][1])[0][-1]+1],
						"y":self.pageargs["Infobj"].Config["Painter"]["Line"].lorentzian_fit(x[np.where(x>=lfr[i][0])[0][0]:np.where(x<=lfr[i][1])[0][-1]+1],y[np.where(x>=lfr[i][0])[0][0]:np.where(x<=lfr[i][1])[0][-1]+1],lfg[i],lfm[i]),
						"color":lfc[i],
						"linestyle":lfs[i]
					}
					lorlineinfo.update({"label":get_MARK(lfl[i],lorlineinfo["x"],lorlineinfo["y"],i)})
					line.append(self.pageargs["Infobj"].Config["Painter"]["Line"].CreateLine(**lorlineinfo))
		return line
	def get_line(self,lineinfo):
		return [self.pageargs["Infobj"].Config["Painter"]["Line"].CreateLine(**lineinfo)]+self.Fitting(lineinfo)
	def get_x(self,qt,rf,re,tf,te,rhof,rhoe,index):
		if qt.get()=="" or index.get()=="":
			return False
		factor=1
		factor*=str_to_float(rf.get())*self.unit_r**str_to_float(re.get())
		factor*=str_to_float(tf.get())*self.unit_t**str_to_float(te.get())
		factor*=str_to_float(rhof.get())*self.unit_rho**str_to_float(rhoe.get())
		ind=self.pageargs["Infobj"].database.tindex.index(int(index.get()))
		if qt.get()in self.pageargs["Infobj"].database.data[ind].grid.keys():
			return factor*self.pageargs["Infobj"].database.data[ind].grid[qt.get()]
		else:
			return factor*self.pageargs["Infobj"].database.data[ind].quantities[qt.get()]
		return False
	def get_y(self,qt,rf,re,tf,te,rhof,rhoe):
		if qt.get()=="":
			return False
		factor=1
		factor*=str_to_float(rf.get())*self.unit_r**str_to_float(re.get())
		factor*=str_to_float(tf.get())*self.unit_t**str_to_float(te.get())
		factor*=str_to_float(rhof.get())*self.unit_rho**str_to_float(rhoe.get())
		result=[]
		for i in self.pageargs["Infobj"].database.data:
			if i!=None:
				result.append(i.quantities[qt.get()]*factor)
		return np.array(result)
	def get_lineinfo(self,x,y,ylb,yco,yls,yargs):
		lineinfo={
			"x":x,
			"y":y,
			"label":checkNone(ylb.get()),
			"color":checkNone(yco.get()),
			"linestyle":yls.get()
		}
		for i in yargs.get().split(";"):
			iic=i.split("=")
			if len(iic)==2:
				lineinfo.update({iic[0]:retype_string(iic[1])})
		def get_par(key,default):
			return lineinfo[key] if key in lineinfo.keys() else default
		lineinfo["y"]=self.low_pass_filter(lineinfo["y"],get_par("filterlevel",0), get_par("cut",None)) if get_par("linefilter",False) else lineinfo["y"]
		return lineinfo
	def get_lineinfo3d(x,y,z,zlb,zco,zls,zargs):
		lineinfo={
			"x":x,
			"y":y,
			"z":z,
			"label":checkNone(zlb.get()),
			"color":checkNone(zco.get()),
			"linestyle":zls.get()
		}
		for i in zargs.get().split(";"):
			iic=i.split("=")
			if len(iic)==2:
				lineinfo.update({iic[0]:retype_string(iic[1])})
		def get_par(key,default):
			return lineinfo[key] if key in lineinfo.keys() else default
		lineinfo["z"]=self.low_pass_filter(lineinfo["z"],get_par("filterlevel",0), get_par("cut",None)) if get_par("linefilter",False) else lineinfo["z"]
		return lineinfo
	def get_figureinfo(self,ft,fx,fy,fxs,fys,fxa,fxb,fya,fyb,fargs):
		figureinfo={
			"title":ft.get(),
			"x_axis":fx.get(),
			"y_axis":fy.get(),
			"xscale":checkNone(fxs.get()),
			"yscale":checkNone(fys.get()),
			"x_lim":None if fxa.get()=="" or fxb.get()=="" else (str_to_float(fxa.get()),str_to_float(fxb.get())),
			"y_lim":None if fya.get()=="" or fyb.get()=="" else (str_to_float(fya.get()),str_to_float(fyb.get()))
		}
		for i in fargs.get().split(";"):
			iic=i.split("=")
			if len(iic)==2:
				figureinfo.update({iic[0]:retype_string(iic[1])})
		return figureinfo
	def get_figureinfo3d(self,ft,fx,fy,fz,fxa,fxb,fya,fyb,fza,fzb,fargs):
		figureinfo={
			"title":ft.get(),
			"x_axis":fx.get(),
			"y_axis":fy.get(),
			"z_axis":fz.get(),
			"x_lim":None if fxa.get()=="" or fxb.get()=="" else (str_to_float(fxa.get()),str_to_float(fxb.get())),
			"y_lim":None if fya.get()=="" or fyb.get()=="" else (str_to_float(fya.get()),str_to_float(fyb.get())),
			"z_lim":None if fza.get()=="" or fzb.get()=="" else (str_to_float(fza.get()),str_to_float(fzb.get()))
		}
		for i in fargs.get().split(";"):
			iic=i.split("=")
			if len(iic)==2:
				figureinfo.update({iic[0]:retype_string(iic[1])})
		return figureinfo
	def get_surfaceinfo(self,x,y,v,vargs):
		surfaceinfo={
			"x":x,
			"y":y,
			"v":v}
		for i in vargs.get().split(";"):
			iic=i.split("=")
			if len(iic)==2:
				surfaceinfo.update({iic[0]:retype_string(iic[1])})
		return surfaceinfo
	def get_scatter3d(self,x,y,z,v,vargs):
		Scatterinfo={
			"x":x,
			"y":y,
			"z":z,
			"v":v
			}
		for i in vargs.get().split(";"):
			iic=i.split("=")
			if len(iic)==2:
				Scatterinfo.update({iic[0]:retype_string(iic[1])})
		return Scatterinfo
	def LD(self):
		LD=self.add_menu("Load",submenu=1)
		self.add_row(LD) 
		self.add_title(LD,"Load Database")
		box=self.add_row(LD,bx=260)
		entry=Entry(box,width=20)
		def select(event):
			folder_path=filedialog.askopenfilename()
			if folder_path!="":
				entry.delete(0,"end")
				entry.insert(0,folder_path)
		button1=Button(box,text="Select",width=5)
		button1.bind("<ButtonRelease>",select)
		button1.pack(side="left")
		entry.pack(side="left")
		self.add_title(LD,"(Please check the progress in DOC window!)",fontsize=8,fg="red")
		def load(event):
			if entry.get()!="":
				if self.pageargs["Infobj"].load(entry.get()):
					self.avqt=[[],[],[],[]]
					self.avgr=[]
					for i in self.pageargs["Infobj"].database.data[0].grid.keys():
						self.avgr.append(i)
					for i in self.pageargs["Infobj"].database.data[0].quantities.keys():
						if type(self.pageargs["Infobj"].database.data[0].quantities[i])==np.ndarray:
							self.avqt[self.pageargs["Infobj"].database.data[0].quantities[i].ndim].append(i)
						else:
							try:
								str_to_float(self.pageargs["Infobj"].database.data[0].quantities[i])
								self.avqt[0].append(i)
							except:
								pass
					self.reload()
					self.tkobj.io_recv("Load",entry.get(),"completed",color="green")
		def view(event):
			self.tkobj.io_recv("Collecting data in",self.LD_index.get())
			ind=self.pageargs["Infobj"].database.tindex.index(int(self.LD_index.get()))
			update_entry(x1,"")
			update_entry(x2,"")
			update_entry(x3,"")
			if "x1" in self.avgr:
				update_entry(x1,str(self.pageargs["Infobj"].database.data[ind].grid["x1"]))
			if "x2" in self.avgr:
				update_entry(x2,str(self.pageargs["Infobj"].database.data[ind].grid["x2"]))
			if "x3" in self.avgr:
				update_entry(x3,str(self.pageargs["Infobj"].database.data[ind].grid["x3"]))
			keys=list(self.pageargs["Infobj"].database.data[ind].quantities.keys())
			for i in range(self.infomation_max):
				update_entry(qtv[i],"" if i>=len(keys) else str(self.pageargs["Infobj"].database.data[ind].quantities[keys[i]]))
				qtn[i].config(text="" if i>=len(keys) else keys[i] if type(self.pageargs["Infobj"].database.data[ind].quantities[keys[i]]) != np.ndarray else "("+str(self.pageargs["Infobj"].database.data[ind].quantities[keys[i]].ndim)+"D)"+keys[i])
		button2=Button(box,text="Load",width=5)
		button2.bind("<ButtonRelease>",load)
		button2.pack(side="left")
		self.add_row(LD)
		box=self.add_row(LD,bx=220)
		Label(box,text="Select An Index:",width=20).pack(side="left")
		self.LD_index=ttk.Combobox(box,width=5,height=10)
		self.LD_index.pack(side="left")
		button=Button(box,text="view",width=5)
		button.bind("<ButtonRelease>",view)
		button.pack(side="left")
		self.add_row(LD)
		self.add_title(LD,"Grids viewer",fg="green",fontsize=14)
		Label(self.add_row(LD),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(LD) 
		Label(box,text="Grid Name",width=10,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Grids Value",width=80,fg="green").pack(side="left")
		Label(self.add_row(LD),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(LD)
		Label(box,width=10,text="x1").pack(side="left")
		Label(box,text="| ").pack(side="left")
		x1=Entry(box,width=80)
		x1.config(state="readonly")
		x1.pack(side="left")
		Label(self.add_row(LD),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(LD)
		Label(box,width=10,text="x2").pack(side="left")
		Label(box,text="| ").pack(side="left")
		x2=Entry(box,width=80)
		x2.config(state="readonly")
		x2.pack(side="left")
		Label(self.add_row(LD),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(LD)
		Label(box,width=10,text="x3").pack(side="left")
		Label(box,text="| ").pack(side="left")
		x3=Entry(box,width=80)
		x3.config(state="readonly")
		x3.pack(side="left")
		Label(self.add_row(LD),text="="*500).place(x=0,y=0,anchor="nw")  #end
		self.add_row(LD) 
		self.add_title(LD,"Quantities viewer",fg="green",fontsize=14)
		Label(self.add_row(LD),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(LD)
		Label(box,text="ID",width=5,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Quantity Name",width=20,fg="green").pack(side="left")
		Label(box,text="| ").pack(side="left")
		Label(box,text="Quantity Value",width=60,fg="green").pack(side="left")
		qtn=[]
		qtv=[]
		for i in range(self.infomation_max):
			Label(self.add_row(LD),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(LD)
			Label(box,text=i,width=5).pack(side="left")
			Label(box,text="| ").pack(side="left")
			qtn.append(Label(box,width=20))
			qtn[-1].pack(side="left")
			Label(box,text="| ").pack(side="left")
			qtv.append(Entry(box,width=60))
			qtv[-1].config(state="readonly")
			qtv[-1].pack(side="left")
		Label(self.add_row(LD),text="="*500).place(x=0,y=0,anchor="nw") #end

	def LD_GS(self):	
		GS=self.add_menu("Global Setting",submenu=1)
		self.add_row(GS) 
		self.add_title(GS,"Global Setting")
		Label(self.add_row(GS,bx=150),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(GS,bx=150)
		Label(box,text="Saved File",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_SF=Entry(box,width=20)
		update_entry(entry_SF,os.path.join(ShockFinderDir,"SavedFigures.hdf5"),False)
		entry_SF.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def select_SF(event):
			folder_path=filedialog.askopenfilename()
			if folder_path!="":
				update_entry(entry_SF,folder_path,False)
		button_SF_SE=Button(box,text="Select",width=5)
		button_SF_SE.bind("<ButtonRelease>",select_SF)
		button_SF_SE.pack(side="left")
		Label(box,width=2).pack(side="left")
		def fun_SF(event):
			if entry_SF.get()!="" and (not os.path.exists(entry_SF.get()) or self.hdf5handler.is_valid_hdf5(entry_SF.get()) or messagebox.askokcancel("Recreate Confirm","The selected file is not a ShockFinder storage file, do you wish to create a new file?")):
				self.hdf5handler.set_file(entry_SF.get())
				[i() for i in self.reset_funs]
		button_SF=Button(box,text="Load",width=5)
		button_SF.bind("<ButtonRelease>",fun_SF)
		button_SF.pack(side="left")
		fun_SF(None)
		Label(self.add_row(GS,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(GS,bx=150)
		Label(box,text="Multi-Process Engine",width=20).pack(side="left")
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
			self.pageargs["Infobj"].set_MPE(MPE_ENG.get())
			self.tkobj.io_recv("Updated Multi-process Engine to",self.pageargs["Infobj"].MultiprocessEngine)
		button_mpeeng=Button(box,text="Update",width=5)
		button_mpeeng.bind("<ButtonRelease>",fun_mpeeng)
		button_mpeeng.pack(side="left")
		Label(self.add_row(GS,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(GS,bx=150)
		Label(box,text="Cores Num",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		MPE_PNUM=Entry(box,width=20)
		update_entry(MPE_PNUM,self.pageargs["Infobj"].LMPEINFO["pnum"],False)
		MPE_PNUM.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_MPE_PNUM(event):
			if int(MPE_PNUM.get())>cpu_count()-self.pageargs["Infobj"].LMPEINFO["cpu_leave"]:
				update_entry(MPE_PNUM,cpu_count()-self.pageargs["Infobj"].LMPEINFO["cpu_leave"],False)
				self.pageargs["Infobj"].LMPEINFO["pnum"]=int(MPE_PNUM.get())
				self.tkobj.io_recv("Updated Multi-process cores num to",self.pageargs["Infobj"].LMPEINFO["pnum"],"(Exceed upper limit,",self.pageargs["Infobj"].LMPEINFO["cpu_leave"]," used for maintaining system stable)",color="blue")
			else:
				self.pageargs["Infobj"].LMPEINFO["pnum"]=int(MPE_PNUM.get())
				self.tkobj.io_recv("Updated Multi-process cores num to",self.pageargs["Infobj"].LMPEINFO["pnum"])
		button_MPE_PNUM=Button(box,text="Update",width=5)
		button_MPE_PNUM.bind("<ButtonRelease>",fun_MPE_PNUM)
		button_MPE_PNUM.pack(side="left")
		Label(self.add_row(GS,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(GS,bx=150)
		Label(box,text="Database Storage Engine",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		egs=list(self.pageargs["Infobj"].Config["IO"].keys())
		IO_ENG=ttk.Combobox(box,width=18,height=len(egs) if len(egs)<=10 else 10,values=egs)
		if self.pageargs["Infobj"].Default_IO in self.pageargs["Infobj"].Config["IO"]:
			IO_ENG.set(self.pageargs["Infobj"].Default_IO)
		else:
			IO_ENG.set(egs[0])
		IO_ENG.pack(side="left")
		Label(box,text="| ").pack(side="left")
		def fun_IOENG(event):
			self.pageargs["Infobj"].set_IO(IO_ENG.get())
			self.tkobj.io_recv("Updated IO Engine to",self.pageargs["Infobj"].IO)
		button_IOENG=Button(box,text="Update",width=5)
		button_IOENG.bind("<ButtonRelease>",fun_IOENG)
		button_IOENG.pack(side="left")
		Label(self.add_row(GS,bx=150),text="="*500).place(x=0,y=0,anchor="nw")  #end
	
	def UnitSet(self):
		bigbox=self.add_menu("Set Units",submenu=1)
		self.add_row(bigbox)
		self.add_title(bigbox,"Units",fg="red",fontsize=22)
		
		#Quick box
		def reset_savedunits():
			self.tkobj.io_recv("Reseting Units set ...")
			savedbox.config(values=()+self.hdf5handler.read_units())
		self.reset_funs.append(reset_savedunits)
		def load_savedunits(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading units",savedbox.get(),"...",color="blue")
				savedunits=self.hdf5handler.read_units(savedbox.get())
				update_entry(entry_r,savedunits["length"],False)
				update_entry(entry_t,savedunits["time"],False)
				fun_set_units(None)
				update_entry(entry_rho,savedunits["density"],False)
				fun_rho(None)
				update_entry(entry_rb,savedunits["rb"],False)
				update_entry(entry_lam,savedunits["lam"],False)
				update_entry(entry_mach,savedunits["mach"],False)
				update_entry(entry_rb,savedunits["rb"],False)
				update_entry(entry_mass,savedunits["mass"],False)
				update_entry(entry_gamma,savedunits["gamma"],False)
				update_entry(entry_rs,savedunits["rs"],False)
				update_entry(entry_theinj,savedunits["theinj"],False)
				update_entry(entry_enginj,savedunits["enginj"],False)
				update_entry(entry_mfinj,savedunits["mfinj"],False)
				update_entry(entry_rhoinj,savedunits["rhoinj"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_savedunits(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete unit "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting units",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_units(savedbox.get())
			reset_savedunits()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_units())
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_savedunits)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_savedunits)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		self.add_row(bigbox)
		self.add_title(bigbox,"Set by manual")
		Label(self.add_row(bigbox,bx=150),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=150)
		Label(box,text="length (cm)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_r=Entry(box,width=20)
		entry_r.pack(side="left")
		def fun_set_units(event):
			if entry_r.get()!="":
				try:
					self.unit_r=str_to_float(entry_r.get())
					self.tkobj.io_recv("Set unit of length to",self.unit_r,"(cm)")
					self.unit_t=str_to_float(entry_t.get())
					self.tkobj.io_recv("Set unit of time to",self.unit_t,"(s)")
					self.unit_v=self.unit_r/self.unit_t
					update_entry(entry_v,self.unit_v)
					self.tkobj.io_recv("Set unit of velocity to",self.unit_v,"(cm/s)")
				except Exception as err:
					self.tkobj.io_recv(err,color="red")
		Label(box,text="| ").pack(side="left")
		button=Button(box,text="Set",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",fun_set_units)
		Label(self.add_row(bigbox,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=150)
		Label(box,text="time (s)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_t=Entry(box,width=20)
		entry_t.pack(side="left")
		Label(box,text="| ").pack(side="left")
		button=Button(box,text="Set",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",fun_set_units)
		Label(self.add_row(bigbox,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=150)
		Label(box,text="velocity (cm/s)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_v=Entry(box,width=20)
		entry_v.pack(side="left")
		entry_v.config(state="readonly")
		Label(self.add_row(bigbox,bx=150),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=150)
		Label(box,text="density (g/cm^3)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_rho=Entry(box,width=20)
		entry_rho.pack(side="left")
		def fun_rho(event):
			if entry_rho.get()!="":
				try:
					self.unit_rho=str_to_float(entry_rho.get())
					self.tkobj.io_recv("Set unit of density to",self.unit_rho,"(g/cm^3)")
				except Exception as err:
					self.tkobj.io_recv(err,color="red")
		Label(box,text="| ").pack(side="left")
		button=Button(box,text="Set",width=5)
		button.pack(side="left")
		button.bind("<ButtonRelease>",fun_rho)
		Label(self.add_row(bigbox,bx=150),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def fun_equ(event=None):
			try:
				rb=str_to_float(entry_rb.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Outer boundary error:",err,color="red")
			try:
				lam=str_to_float(entry_lam.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Lambda error:",err,color="red")
			try:
				mach=str_to_float(entry_mach.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Mach number error:",err,color="red")
			try:
				mass=str_to_float(entry_mass.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Mass error:",err,color="red")
			try:
				gamma=str_to_float(entry_gamma.get())
			except Exception as err:
				return self.tkobj.io_recv("Read gamma error:",err,color="red")
			try:
				rs=int(entry_rs.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Radius type error:",err,color="red")
			try:
				theta_inj=str_to_float(entry_theinj.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Theta@Inject error:",err,color="red")
			try:
				eng=str_to_float(entry_enginj.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Net energy@Inject error:",err,color="red")
			try:
				injflux=str_to_float(entry_mfinj.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Massflux@Inject error:",err,color="red")
			try:
				injrho=str_to_float(entry_rhoinj.get())
			except Exception as err:
				return self.tkobj.io_recv("Read Density@Inject error:",err,color="red")
			hequantities=self.pageargs["Infobj"].Config["AnalysisLib"]["Equilibrium"].Equilibrium(rb,lam,mach,gamma,rs,eng,theta_inj)
			units=self.pageargs["Infobj"].Config["AnalysisLib"]["Equilibrium"].Unit(mass,self.pageargs["Infobj"].Config["AnalysisLib"]["Equilibrium"].YearMassFlux_to_MassFlux(injflux),injrho,hequantities)
			self.unit_r=units["unit_r"]
			entry_r.delete(0,"end")
			entry_r.insert(0,self.unit_r)
			self.unit_t=units["unit_t"]
			entry_t.delete(0,"end")
			entry_t.insert(0,self.unit_t)
			self.unit_v=units["unit_r"]/units["unit_t"]
			update_entry(entry_v,self.unit_v)
			self.unit_rho=units["unit_rho"]
			entry_rho.delete(0,"end")
			entry_rho.insert(0,self.unit_rho)
			if event!=None:
				self.tkobj.io_recv("Set unit of length to",self.unit_r,"(cm)")
				self.tkobj.io_recv("Set unit of time to",self.unit_t,"(s)")
				self.tkobj.io_recv("Set unit of density to",self.unit_rho,"(g/cm^3)")
				self.tkobj.io_recv("Set unit of velocity to",self.unit_v,"(cm/s)")
		self.add_row(bigbox)
		self.add_title(bigbox,"Set from Equilibrium")
		Label(self.add_row(bigbox,bx=200),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Outer boundary",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_rb=Entry(box,width=20)
		entry_rb.pack(side="left")
		entry_rb.insert(0,200)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Lambda",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_lam=Entry(box,width=20)
		entry_lam.pack(side="left")
		entry_lam.insert(0,1.75)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Mach number",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_mach=Entry(box,width=20)
		entry_mach.pack(side="left")
		entry_mach.insert(0,5)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Mass",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_mass=Entry(box,width=20)
		entry_mass.pack(side="left")
		entry_mass.insert(0,10)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="gamma",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_gamma=Entry(box,width=20)
		entry_gamma.pack(side="left")
		entry_gamma.insert(0,4/3)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Radius type (rs)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_rs=ttk.Combobox(box,width=20,height=2,values=[1,2])
		entry_rs.pack(side="left")
		entry_rs.set(1)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Theta@Inject",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_theinj=Entry(box,width=20)
		entry_theinj.pack(side="left")
		entry_theinj.insert(0,0)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Net energy@Inject",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_enginj=Entry(box,width=20)
		entry_enginj.pack(side="left")
		entry_enginj.insert(0,0)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Massflux@Inject (Msun/yr)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_mfinj=Entry(box,width=20)
		entry_mfinj.pack(side="left")
		entry_mfinj.insert(0,6.25e-11)
		Label(self.add_row(bigbox,bx=200),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=200)
		Label(box,text="Density@Inject (dimle)",width=20).pack(side="left")
		Label(box,text="| ").pack(side="left")
		entry_rhoinj=Entry(box,width=20)
		entry_rhoinj.pack(side="left")
		entry_rhoinj.insert(0,1)
		Label(self.add_row(bigbox,bx=200),text="="*500).place(x=0,y=0,anchor="nw")  #end
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Calculate",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",fun_equ)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_units() and not messagebox.askokcancel("Rewrite Confirm","Rewrite unit "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving units",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"length":entry_r.get(),
						"time":entry_t.get(),
						"density":entry_rho.get(),
						"rb":entry_rb.get(),
						"lam":entry_lam.get(),
						"mach":entry_mach.get(),
						"rb":entry_rb.get(),
						"mass":entry_mass.get(),
						"gamma":entry_gamma.get(),
						"rs":entry_rs.get(),
						"theinj":entry_theinj.get(),
						"enginj":entry_enginj.get(),
						"mfinj":entry_mfinj.get(),
						"rhoinj":entry_rhoinj.get()
					}
					self.hdf5handler.write_units({entry_save.get():dd})
					reset_savedunits()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
		fun_equ()
	def QuickSaved(self):
		bigbox=self.add_menu("Quick Saved",submenu=1)
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Saved",fg="red",fontsize=24)

		
		def reorganize_keys(d):
			# Determine if the dictionary contains nested dictionaries
			first_value = next(iter(d.values()))
			if isinstance(first_value, dict):
				# If d is a dictionary of dictionaries
				inner_keys = list(first_value.keys())
				transformed = {
				k: {outer_k: v[k] if k in v else None for outer_k, v in d.items()} 
					for k in inner_keys
				}
				return transformed
			else:
				# If d is a simple dictionary
				return {str(index): item for index, item in enumerate(d)}
		def list_to_dict(lst, attr, key=None):
			# If key is a string, convert it into a tuple
			if isinstance(key, str):
				key = (key,)
			# Extract the attribute from each object and proceed based on the key
			def extract_data(item):
				data = getattr(item, attr, None)
				if data is None:
					return None
				if isinstance(key, (tuple, list)):
					return {k: v for k, v in data.items() if k in key}
				else:
					return data
			
			# Get transformed data for the list
			transformed_data = {str(index): extract_data(item) for index, item in enumerate(lst)}
			
			# Check if any item had the attribute missing and return None if so
			if any(value is None for value in transformed_data.values()):
				return None
			
			return transformed_data

		self.add_row(bigbox)
		self.add_title(bigbox,"0d Data",fg="green")
		def reset_0D():
			self.tkobj.io_recv("Reseting 0d data set ...")
			box_0D.config(values=self.hdf5handler.read_data("0D"))
		self.reset_funs.append(reset_0D)
		def load_0D(event):
			if box_0D.get()=="":
				return
			varname=box_0D.get() if entry_as_0D.get()=="" else entry_as_0D.get()
			self.tkobj.io_recv("Loading 0d data",box_0D.get(),"as",varname,"...",color="blue")
			try:
				dataget={varname:self.hdf5handler.read_data("0D",box_0D.get())}
				self.pageargs["Infobj"].database.update_with_index(**reorganize_keys(dataget))
				self.avqt[0].append(varname)
				self.reload()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def save_0D(event):
			if self.box_0D.get()=="":
				return
			varname=self.box_0D.get() if entry_to_0D.get()=="" else entry_to_0D.get()
			if varname in self.hdf5handler.read_data("0D") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 0d Data "+varname+" ?"):
				return
			self.tkobj.io_recv("Saving 0d data",self.box_0D.get(),"to",varname,"...",color="blue")
			try:
				self.hdf5handler.write_data("0D",{varname:reorganize_keys(list_to_dict(self.pageargs["Infobj"].database.data,"quantities",self.box_0D.get()))[self.box_0D.get()]})
				reset_0D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def del_0D(event):
			if box_0D.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 0d Data "+box_0D.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 0d data",box_0D.get())
			try:
				self.hdf5handler.del_data("0D",box_0D.get())
				reset_0D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Load",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		box_0D=ttk.Combobox(box,width=17,height=10,values=self.hdf5handler.read_data("0D"))
		box_0D.pack(side="left")
		Label(box,text="as").pack(side="left")
		entry_as_0D=Entry(box,width=17)
		entry_as_0D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_0D)
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_0D)
		Label(self.add_row(bigbox,bx=130),text="-"*500).place(x=0,y=0,anchor="nw")  #next
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Save",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		self.box_0D=ttk.Combobox(box,width=17,height=10)
		self.box_0D.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_to_0D=Entry(box,width=17)
		entry_to_0D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save_0D)
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #end


		self.add_row(bigbox)
		self.add_title(bigbox,"1D Data",fg="green")
		def reset_1D():
			self.tkobj.io_recv("Reseting 1D data set ...")
			box_1D.config(values=self.hdf5handler.read_data("1D"))
		self.reset_funs.append(reset_1D)
		def load_1D(event):
			if box_1D.get()=="":
				return
			varname=box_1D.get() if entry_as_1D.get()=="" else entry_as_1D.get()
			self.tkobj.io_recv("Loading 1D data",box_1D.get(),"as",varname,"...",color="blue")
			try:
				dataget={varname:self.hdf5handler.read_data("1D",box_1D.get())}
				self.pageargs["Infobj"].database.update_with_index(**reorganize_keys(dataget))
				if varname not in ("x1","x2","x3"):
					self.avqt[1].append(varname)
				self.reload()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def save_1D(event):
			if self.box_1D.get()=="":
				return
			varname=self.box_1D.get() if entry_to_1D.get()=="" else entry_to_1D.get()
			if varname in self.hdf5handler.read_data("1D") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 1D Data "+varname+" ?"):
				return
			self.tkobj.io_recv("Saving 1D data",self.box_1D.get(),"to",varname,"...",color="blue")
			try:
				try:
					self.hdf5handler.write_data("1D",{varname:reorganize_keys(list_to_dict(self.pageargs["Infobj"].database.data,"quantities",self.box_1D.get()))[self.box_1D.get()]})
				except:
					self.tkobj.io_recv(self.box_1D.get(),"no found in quantities libaries, try to find in grid libaries...")
					self.hdf5handler.write_data("1D",{varname:reorganize_keys(list_to_dict(self.pageargs["Infobj"].database.data,"grid",self.box_1D.get()))[self.box_1D.get()]})
				reset_1D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def del_1D(event):
			if box_1D.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 1D Data "+box_1D.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 1D data",box_1D.get())
			try:
				self.hdf5handler.del_data("1D",box_1D.get())
				reset_1D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Load",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		box_1D=ttk.Combobox(box,width=17,height=10,values=self.hdf5handler.read_data("1D"))
		box_1D.pack(side="left")
		Label(box,text="as").pack(side="left")
		entry_as_1D=Entry(box,width=17)
		entry_as_1D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_1D)
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_1D)
		Label(self.add_row(bigbox,bx=130),text="-"*500).place(x=0,y=0,anchor="nw")  #next
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Save",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		self.box_1D=ttk.Combobox(box,width=17,height=10)
		self.box_1D.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_to_1D=Entry(box,width=17)
		entry_to_1D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save_1D)
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #end

		self.add_row(bigbox)
		self.add_title(bigbox,"2D Data",fg="green")
		def reset_2D():
			self.tkobj.io_recv("Reseting 2D data set ...")
			box_2D.config(values=self.hdf5handler.read_data("2D"))
		self.reset_funs.append(reset_2D)
		def load_2D(event):
			if box_2D.get()=="":
				return
			varname=box_2D.get() if entry_as_2D.get()=="" else entry_as_2D.get()
			self.tkobj.io_recv("Loading 2D data",box_2D.get(),"as",varname,"...",color="blue")
			try:
				dataget={varname:self.hdf5handler.read_data("2D",box_2D.get())}
				self.pageargs["Infobj"].database.update_with_index(**reorganize_keys(dataget))
				self.avqt[2].append(varname)
				self.reload()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def save_2D(event):
			if self.box_2D.get()=="":
				return
			varname=self.box_2D.get() if entry_to_2D.get()=="" else entry_to_2D.get()
			if varname in self.hdf5handler.read_data("2D") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 2D Data "+varname+" ?"):
				return
			self.tkobj.io_recv("Saving 2D data",self.box_2D.get(),"to",varname,"...",color="blue")
			try:
				self.hdf5handler.write_data("2D",{varname:reorganize_keys(list_to_dict(self.pageargs["Infobj"].database.data,"quantities",self.box_2D.get()))[self.box_2D.get()]})
				reset_2D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def del_2D(event):
			if box_2D.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 2D Data "+box_2D.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 2D data",box_2D.get())
			try:
				self.hdf5handler.del_data("2D",box_2D.get())
				reset_2D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Load",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		box_2D=ttk.Combobox(box,width=17,height=10,values=self.hdf5handler.read_data("2D"))
		box_2D.pack(side="left")
		Label(box,text="as").pack(side="left")
		entry_as_2D=Entry(box,width=17)
		entry_as_2D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_2D)
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_2D)
		Label(self.add_row(bigbox,bx=130),text="-"*500).place(x=0,y=0,anchor="nw")  #next
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Save",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		self.box_2D=ttk.Combobox(box,width=17,height=10)
		self.box_2D.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_to_2D=Entry(box,width=17)
		entry_to_2D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save_2D)
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #end

		self.add_row(bigbox)
		self.add_title(bigbox,"3D Data",fg="green")
		def reset_3D():
			self.tkobj.io_recv("Reseting 3D data set ...")
			box_3D.config(values=self.hdf5handler.read_data("3D"))
		self.reset_funs.append(reset_3D)
		def load_3D(event):
			if box_3D.get()=="":
				return
			varname=box_3D.get() if entry_as_3D.get()=="" else entry_as_3D.get()
			self.tkobj.io_recv("Loading 3D data",box_3D.get(),"as",varname,"...",color="blue")
			try:
				dataget={varname:self.hdf5handler.read_data("3D",box_3D.get())}
				self.pageargs["Infobj"].database.update_with_index(**reorganize_keys(dataget))
				self.avqt[3].append(varname)
				self.reload()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def save_3D(event):
			if self.box_3D.get()=="":
				return
			varname=self.box_3D.get() if entry_to_3D.get()=="" else entry_to_3D.get()
			if varname in self.hdf5handler.read_data("3D") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 3D Data "+varname+" ?"):
				return
			self.tkobj.io_recv("Saving 3D data",self.box_3D.get(),"to",varname,"...",color="blue")
			try:
				self.hdf5handler.write_data("3D",{varname:reorganize_keys(list_to_dict(self.pageargs["Infobj"].database.data,"quantities",self.box_3D.get()))[self.box_3D.get()]})
				reset_3D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		def del_3D(event):
			if box_3D.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 3D Data "+box_3D.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 3D data",box_3D.get())
			try:
				self.hdf5handler.del_data("3D",box_3D.get())
				reset_3D()
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error:",err,color="red")
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Load",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		box_3D=ttk.Combobox(box,width=17,height=10,values=self.hdf5handler.read_data("3D"))
		box_3D.pack(side="left")
		Label(box,text="as").pack(side="left")
		entry_as_3D=Entry(box,width=17)
		entry_as_3D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_3D)
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_3D)
		Label(self.add_row(bigbox,bx=130),text="-"*500).place(x=0,y=0,anchor="nw")  #next
		box=self.add_row(bigbox,bx=130)
		Label(box,text="Save",width=5).pack(side="left")
		Label(box,text="|").pack(side="left")
		self.box_3D=ttk.Combobox(box,width=17,height=10)
		self.box_3D.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_to_3D=Entry(box,width=17)
		entry_to_3D.pack(side="left")
		Label(box,text="|").pack(side="left")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save_3D)
		Label(self.add_row(bigbox,bx=130),text="="*500).place(x=0,y=0,anchor="nw")  #end

	def FFT(self): #support 0d
		bigbox=self.add_menu("Fast Fourier Transform",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"Fast Fourier Transform (FFT)",fg="red",fontsize=24)
		self.add_title(bigbox,"(FFT only supports scale (0d))",fontsize=10)
		def reset_saved():
			self.tkobj.io_recv("Reseting 2D FFT configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("2D","FFT"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading FFT configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("2D","FFT",savedbox.get())
				update_entry(entry_xtf,savedcfg["xtf"],False)
				update_entry(entry_xte,savedcfg["xte"],False)
				update_entry(entry_yrf,savedcfg["yrf"],False)
				update_entry(entry_yre,savedcfg["yre"],False)
				update_entry(entry_ytf,savedcfg["ytf"],False)
				update_entry(entry_yte,savedcfg["yte"],False)
				update_entry(entry_yrhof,savedcfg["yrhof"],False)
				update_entry(entry_yrhoe,savedcfg["yrhoe"],False)
				update_entry(entry_ylb,savedcfg["ylb"],False)
				update_entry(entry_yco,savedcfg["yco"],False)
				update_entry(entry_yls,savedcfg["yls"],False)
				update_entry(entry_yargs,savedcfg["yargs"],False)
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_fxs,savedcfg["fxs"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fys,savedcfg["fys"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete FFT configuration"+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting FFT configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("2D","FFT",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("2D","FFT"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Line infomation",fg="green")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Axis").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8).pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Label").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Color").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Linestyle").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="X (Time)").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="Time Secquency",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="-",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_xtf=Entry(box,width=7)
		entry_xtf.insert(0,1)
		entry_xtf.pack(side="left")
		Label(box,text="Utim^").pack(side="left")
		entry_xte=Entry(box,width=7)
		entry_xte.insert(0,1)
		entry_xte.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="-",width=20).pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Y (FFT)").pack(side="left")
		Label(box,text="|").pack(side="left")
		self.FFT_Qt=ttk.Combobox(box,width=17,height=10,values=self.avqt[0])
		self.FFT_Qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_yrf=Entry(box,width=7)
		entry_yrf.pack(side="left")
		entry_yrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_yre=Entry(box,width=7)
		entry_yre.pack(side="left")
		entry_yre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_ytf=Entry(box,width=7)
		entry_ytf.pack(side="left")
		entry_ytf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_yte=Entry(box,width=7)
		entry_yte.pack(side="left")
		entry_yte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_yrhof=Entry(box,width=7)
		entry_yrhof.pack(side="left")
		entry_yrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_yrhoe=Entry(box,width=7)
		entry_yrhoe.pack(side="left")
		entry_yrhoe.insert(0,0)
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8).pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ylb=Entry(box,width=20)
		entry_ylb.insert(0,str(None))
		entry_ylb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_yco=Entry(box,width=20)
		entry_yco.insert(0,str(None))
		entry_yco.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_yls=Entry(box,width=20)
		entry_yls.insert(0,"-")
		entry_yls.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_yargs=Entry(box,width=20)
		entry_yargs.pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"Frequency (Hz)")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=8)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=8)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxs=Entry(box,width=20)
		entry_fxs.insert(0,str(None))
		entry_fxs.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y Scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=8)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=8)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fys=Entry(box,width=20)
		entry_fys.insert(0,str(None))
		entry_fys.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawfft(event):
			if self.FFT_Qt.get()=="":
				return
			try:
			#if True:
				self.tkobj.io_recv("Figuring FFT with",self.FFT_Qt.get(),"...")
				#get figinfo
				figureinfo=self.get_figureinfo(entry_ft,entry_fx,entry_fy,entry_fxs,entry_fys,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fargs)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)
				#get lineinfo
				
				factor=1
				factor*=str_to_float(entry_yrf.get())*self.unit_r**str_to_float(entry_yre.get())
				factor*=str_to_float(entry_ytf.get())*self.unit_t**str_to_float(entry_yte.get())
				factor*=str_to_float(entry_yrhof.get())*self.unit_rho**str_to_float(entry_yrhoe.get())
				ft=[]
				tt=range(len(self.pageargs["Infobj"].database.data))
				if "Time" in figureinfo.keys():
					if type(figureinfo["Time"]) not in (list,tuple,np.ndarray):
						figureinfo["Time"]=[figureinfo["Time"]]
					for i in figureinfo["Time"]:
						if i>len(tt):
							return self.tkobj.io_recv("Error: Time list exceeds limit",color="red")
					tt=np.arange(*figureinfo["Time"])
				dt=(tt[-1]-tt[0])/(len(tt)-1)

				for i in tt:
					if self.pageargs["Infobj"].database.data[i]!=None:
						ft.append(self.pageargs["Infobj"].database.data[i].quantities[self.FFT_Qt.get()]*factor)
				ft=np.array(ft)
				if "Interval" in self.pageargs["Infobj"].database.infomation.keys():
					Interval=self.pageargs["Infobj"].database.infomation["Interval"]
				else:
					Interval=1
				filt=False
				filv=0
				cut=None
				ori=entry_yargs.get()
				newargs=""
				for i in entry_yargs.get().split(";"):
					add=True
					iic=i.split("=")
					if len(iic)==2:
						if iic[0]=="linefilter":
							filt=retype_string(iic[1])
							add=False
						elif iic[0]=="filterlevel":
							filv=retype_string(iic[1])
							add=False
						elif iic[0]=="cut":
							cut=retype_string(iic[1])
							add=False
					if add:
						newargs+=i+";"
				if newargs!="":
					newargs=newargs[:-1]
				ft=self.low_pass_filter(ft,filv,cut) if filt else ft
				update_entry(entry_yargs,newargs,False)
				x,y=self.pageargs["Infobj"].Config["AnalysisLib"]["FFT"](ft,unit=dt*str_to_float(entry_xtf.get())*self.unit_t**str_to_float(entry_xte.get()),interval=Interval)
				#lineinfo=self.get_lineinfo(x,y,entry_ylb,entry_yco,entry_yls,entry_yargs)
				#self.tkobj.io_recv("Collected lineinfo:",lineinfo)
				line=self.get_line(self.get_lineinfo(x,y,entry_ylb,entry_yco,entry_yls,entry_yargs))
				update_entry(entry_yargs,ori,False)
				self.pageargs["Infobj"].Config["Painter"]["P2D"].line(*line,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawfft)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("2D","FFT") and not messagebox.askokcancel("Rewrite Confirm","Rewrite FFT configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving FFT configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"xtf":entry_xtf.get(),
						"xte":entry_xte.get(),
						"yrf":entry_yrf.get(),
						"yre":entry_yre.get(),
						"ytf":entry_ytf.get(),
						"yte":entry_yte.get(),
						"yrhof":entry_yrhof.get(),
						"yrhoe":entry_yrhoe.get(),
						"ylb":entry_ylb.get(),
						"yco":entry_yco.get(),
						"yls":entry_yls.get(),
						"yargs":entry_yargs.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"fxs":entry_fxs.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fys":entry_fys.get(),
						"fargs":entry_fargs.get()
					}
					self.hdf5handler.write_config("2D","FFT",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
	def Surface2d(self):
		bigbox=self.add_menu("Surface",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"2D Surface",fg="red",fontsize=24)
		self.add_title(bigbox,"(2D Surface only supports 2d)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 2D Surface configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("2D","Surfaces"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading Surface configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("2D","Surfaces",savedbox.get())
				update_entry(entry_vrf,savedcfg["vrf"],False)
				update_entry(entry_vre,savedcfg["vre"],False)
				update_entry(entry_vtf,savedcfg["vtf"],False)
				update_entry(entry_vte,savedcfg["vte"],False)
				update_entry(entry_vrhof,savedcfg["vrhof"],False)
				update_entry(entry_vrhoe,savedcfg["vrhoe"],False)
				update_entry(entry_vargs,savedcfg["vargs"],False)
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_fxs,savedcfg["fxs"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fys,savedcfg["fys"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 2D Surface configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 2D Surface configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("2D","Surfaces",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("2D","Surfaces"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Surface infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox)
		Label(box,width=20,text="Index").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=80,text="Other Arguments").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		self.P2DSur_Qt=ttk.Combobox(box,width=17,height=10,values=self.avqt[2])
		self.P2DSur_Qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_vrf=Entry(box,width=7)
		entry_vrf.pack(side="left")
		entry_vrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_vre=Entry(box,width=7)
		entry_vre.pack(side="left")
		entry_vre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_vtf=Entry(box,width=7)
		entry_vtf.pack(side="left")
		entry_vtf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_vte=Entry(box,width=7)
		entry_vte.pack(side="left")
		entry_vte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_vrhof=Entry(box,width=7)
		entry_vrhof.pack(side="left")
		entry_vrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_vrhoe=Entry(box,width=7)
		entry_vrhoe.pack(side="left")
		entry_vrhoe.insert(0,0)
		box=self.add_row(bigbox)
		self.P2DSur_index=ttk.Combobox(box,width=17,height=10,values=self.usefultindex)
		self.P2DSur_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_vargs=Entry(box,width=66)
		entry_vargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"X")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=8)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=8)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxs=Entry(box,width=20)
		entry_fxs.insert(0,str(None))
		entry_fxs.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y Scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=8)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=8)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fys=Entry(box,width=20)
		entry_fys.insert(0,str(None))
		entry_fys.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawsur2d(event):
			if self.P2DSur_Qt.get()=="" or self.P2DSur_index.get()=="":
				return
			try:
				self.tkobj.io_recv("Figuring Surface with",self.P2DSur_Qt.get(),"...")
				#get figinfo

				figureinfo=self.get_figureinfo(entry_ft,entry_fx,entry_fy,entry_fxs,entry_fys,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fargs)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

				#begining to drow
				factor=1
				factor*=str_to_float(entry_vrf.get())*self.unit_r**str_to_float(entry_vre.get())
				factor*=str_to_float(entry_vtf.get())*self.unit_t**str_to_float(entry_vte.get())
				factor*=str_to_float(entry_vrhof.get())*self.unit_rho**str_to_float(entry_vrhoe.get())
				ind=self.pageargs["Infobj"].database.tindex.index(int(self.P2DSur_index.get()))
				try:
					x=self.pageargs["Infobj"].database.data[ind].grid["x1"]
				except:
					x=self.pageargs["Infobj"].database.data[ind].quantities["x1"]
				try:
					y=self.pageargs["Infobj"].database.data[ind].grid["x2"]
				except:
					y=self.pageargs["Infobj"].database.data[ind].quantities["x2"]
				v=self.pageargs["Infobj"].database.data[ind].quantities[self.P2DSur_Qt.get()]*factor
				if self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="SPHERICAL":
					x,y,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rot_to_xoz(x,y,v)
				elif self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="POLAR":
					x,y,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rop_to_xoy(x,y,v)
				surfaceinfo=self.get_surfaceinfo(x,y,v,entry_vargs)

				self.tkobj.io_recv("Collected surfaceinfo:",surfaceinfo)
				surface=self.pageargs["Infobj"].Config["Painter"]["Surface"].CreateSurface(**surfaceinfo)
				self.pageargs["Infobj"].Config["Painter"]["P2D"].surface(surface,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawsur2d)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("2D","Surfaces") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 2D Surface configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving 2D Surface configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"vrf":entry_vrf.get(),
						"vre":entry_vre.get(),
						"vtf":entry_vtf.get(),
						"vte":entry_vte.get(),
						"vrhof":entry_vrhof.get(),
						"vrhoe":entry_vrhoe.get(),
						"vargs":entry_vargs.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"fxs":entry_fxs.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fys":entry_fys.get(),
						"fargs":entry_fargs.get()
					}
					self.hdf5handler.write_config("2D","Surfaces",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
	def Line2d(self): #support 0d
		bigbox=self.add_menu("Lines",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"2D Lines",fg="red",fontsize=24)
		self.add_title(bigbox,"(Lins only supports 1D)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 2D Lines configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("2D","Lines"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading 2D Lines configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("2D","Lines",savedbox.get())
				update_entry(entry_xrf,savedcfg["xrf"],False)
				update_entry(entry_xre,savedcfg["xre"],False)
				update_entry(entry_xtf,savedcfg["xtf"],False)
				update_entry(entry_xte,savedcfg["xte"],False)
				update_entry(entry_xrhof,savedcfg["xrhof"],False)
				update_entry(entry_xrhoe,savedcfg["xrhoe"],False)
				update_entry(entry_syrf,savedcfg["syrf"],False)
				update_entry(entry_syre,savedcfg["syre"],False)
				update_entry(entry_sytf,savedcfg["sytf"],False)
				update_entry(entry_syte,savedcfg["syte"],False)
				update_entry(entry_syrhof,savedcfg["syrhof"],False)
				update_entry(entry_syrhoe,savedcfg["syrhoe"],False)
				update_entry(entry_sylb,savedcfg["sylb"],False)
				update_entry(entry_syco,savedcfg["syco"],False)
				update_entry(entry_syls,savedcfg["syls"],False)
				update_entry(entry_syargs,savedcfg["syargs"],False)
				for i in range(self.maxline):
					try:
						update_entry(entry_yrf[i],savedcfg["yrf"+str(i)],False)
						update_entry(entry_yre[i],savedcfg["yre"+str(i)],False)
						update_entry(entry_ytf[i],savedcfg["ytf"+str(i)],False)
						update_entry(entry_yte[i],savedcfg["yte"+str(i)],False)
						update_entry(entry_yrhof[i],savedcfg["yrhof"+str(i)],False)
						update_entry(entry_yrhoe[i],savedcfg["yrhoe"+str(i)],False)
						update_entry(entry_ylb[i],savedcfg["ylb"+str(i)],False)
						update_entry(entry_yco[i],savedcfg["yco"+str(i)],False)
						update_entry(entry_yls[i],savedcfg["yls"+str(i)],False)
						update_entry(entry_yargs[i],savedcfg["yargs"+str(i)],False)
					except:
						pass
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_fxs,savedcfg["fxs"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fys,savedcfg["fys"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 2D Line configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 2D Lines configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("2D","Lines",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("2D","Lines"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Line infomation",fg="green")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Axis").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Index").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Label").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Color").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Linestyle").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=2,text="X").pack(side="left")
		self.Line2d_x_index=ttk.Combobox(box,width=3,height=10,values=self.usefultindex)
		self.Line2d_x_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		self.Line2d_x_qt=ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1])
		self.Line2d_x_qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_xrf=Entry(box,width=7)
		entry_xrf.pack(side="left")
		entry_xrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_xre=Entry(box,width=7)
		entry_xre.pack(side="left")
		entry_xre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_xtf=Entry(box,width=7)
		entry_xtf.pack(side="left")
		entry_xtf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_xte=Entry(box,width=7)
		entry_xte.pack(side="left")
		entry_xte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_xrhof=Entry(box,width=7)
		entry_xrhof.pack(side="left")
		entry_xrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_xrhoe=Entry(box,width=7)
		entry_xrhoe.pack(side="left")
		entry_xrhoe.insert(0,0)
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Y (Share X)").pack(side="left")
		Label(box,text="|").pack(side="left")
		self.Line2d_sy_qt=ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1])
		self.Line2d_sy_qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syrf=Entry(box,width=7)
		entry_syrf.pack(side="left")
		entry_syrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_syre=Entry(box,width=7)
		entry_syre.pack(side="left")
		entry_syre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_sytf=Entry(box,width=7)
		entry_sytf.pack(side="left")
		entry_sytf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_syte=Entry(box,width=7)
		entry_syte.pack(side="left")
		entry_syte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_syrhof=Entry(box,width=7)
		entry_syrhof.pack(side="left")
		entry_syrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_syrhoe=Entry(box,width=7)
		entry_syrhoe.pack(side="left")
		entry_syrhoe.insert(0,0)
		box=self.add_row(bigbox,bx=20)
		self.Line2d_sy_index=ttk.Combobox(box,width=6,height=10,values=self.usefultindex)
		self.Line2d_sy_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_sylb=Entry(box,width=20)
		entry_sylb.insert(0,str(None))
		entry_sylb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syco=Entry(box,width=20)
		entry_syco.insert(0,str(None))
		entry_syco.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syls=Entry(box,width=20)
		entry_syls.insert(0,"-")
		entry_syls.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syargs=Entry(box,width=20)
		entry_syargs.pack(side="left")

		entry_yrf=[]
		entry_yre=[]
		entry_ytf=[]
		entry_yte=[]
		entry_yrhof=[]
		entry_yrhoe=[]
		entry_ylb=[]
		entry_yco=[]
		entry_yls=[]
		entry_yargs=[]
		self.Line2d_y_qt=[]
		self.Line2d_y_index=[]
		for i in range(self.maxline):
			Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(bigbox,bx=20)
			Label(box,width=8,text="Y"+str(i+1)).pack(side="left")
			Label(box,text="|").pack(side="left")
			self.Line2d_y_qt.append(ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1]))
			self.Line2d_y_qt[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yrf.append(Entry(box,width=7))
			entry_yrf[-1].pack(side="left")
			entry_yrf[-1].insert(0,1)
			Label(box,text="Ulen^").pack(side="left")
			entry_yre.append(Entry(box,width=7))
			entry_yre[-1].pack(side="left")
			entry_yre[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_ytf.append(Entry(box,width=7))
			entry_ytf[-1].pack(side="left")
			entry_ytf[-1].insert(0,1)
			Label(box,text="Utim^").pack(side="left")
			entry_yte.append(Entry(box,width=7))
			entry_yte[-1].pack(side="left")
			entry_yte[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_yrhof.append(Entry(box,width=7))
			entry_yrhof[-1].pack(side="left")
			entry_yrhof[-1].insert(0,1)
			Label(box,text="Urho^").pack(side="left")
			entry_yrhoe.append(Entry(box,width=7))
			entry_yrhoe[-1].pack(side="left")
			entry_yrhoe[-1].insert(0,0)
			box=self.add_row(bigbox,bx=20)
			self.Line2d_y_index.append(ttk.Combobox(box,width=6,height=10,values=self.usefultindex))
			self.Line2d_y_index[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_ylb.append(Entry(box,width=20))
			entry_ylb[-1].insert(0,str(None))
			entry_ylb[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yco.append(Entry(box,width=20))
			entry_yco[-1].insert(0,str(None))
			entry_yco[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yls.append(Entry(box,width=20))
			entry_yls[-1].insert(0,"-")
			entry_yls[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yargs.append(Entry(box,width=20))
			entry_yargs[-1].pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"X")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=8)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=8)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxs=Entry(box,width=20)
		entry_fxs.insert(0,str(None))
		entry_fxs.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y Scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=8)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=8)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fys=Entry(box,width=20)
		entry_fys.insert(0,str(None))
		entry_fys.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawlines(event):
			try:
				x=self.get_x(self.Line2d_x_qt,entry_xrf,entry_xre,entry_xtf,entry_xte,entry_xrhof,entry_xrhoe,self.Line2d_x_index)
				if str(x)=="False":
					return
				self.tkobj.io_recv("Figuring Lines ...")
				sy=self.get_x(self.Line2d_sy_qt,entry_syrf,entry_syre,entry_sytf,entry_syte,entry_syrhof,entry_syrhoe,self.Line2d_sy_index)
				if str(sy)!="False":
					line_s=self.get_line(self.get_lineinfo(x,sy,entry_sylb,entry_syco,entry_syls,entry_syargs))[0]
				lines=[]
				for i in range(self.maxline):
					y=self.get_x(self.Line2d_y_qt[i],entry_yrf[i],entry_yre[i],entry_ytf[i],entry_yte[i],entry_yrhof[i],entry_yrhoe[i],self.Line2d_y_index[i])
					if str(y)!="False":
						lines+=self.get_line(self.get_lineinfo(x,y,entry_ylb[i],entry_yco[i],entry_yls[i],entry_yargs[i]))

					#get figinfo
				figureinfo=self.get_figureinfo(entry_ft,entry_fx,entry_fy,entry_fxs,entry_fys,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fargs)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

					#begining to drow
				if str(sy)!="False":
					self.pageargs["Infobj"].Config["Painter"]["P2D"].line_share_x(line_s,*lines,**figureinfo)
				else:
					self.pageargs["Infobj"].Config["Painter"]["P2D"].line(*lines,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawlines)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("2D","Lines") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 2D line configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving 2D Lines configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"xrf":entry_xrf.get(),
						"xre":entry_xre.get(),
						"xtf":entry_xtf.get(),
						"xte":entry_xte.get(),
						"xrhof":entry_xrhof.get(),
						"xrhoe":entry_xrhoe.get(),
						"syrf":entry_syrf.get(),
						"syre":entry_syre.get(),
						"sytf":entry_sytf.get(),
						"syte":entry_syte.get(),
						"syrhof":entry_syrhof.get(),
						"syrhoe":entry_syrhoe.get(),
						"sylb":entry_sylb.get(),
						"syco":entry_syco.get(),
						"syls":entry_syls.get(),
						"syargs":entry_syargs.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"fxs":entry_fxs.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fys":entry_fys.get(),
						"fargs":entry_fargs.get()
					}
					for i in range(self.maxline):
						try:
							dd["yrf"+str(i)]=entry_yrf[i].get()
							dd["yre"+str(i)]=entry_yre[i].get()
							dd["ytf"+str(i)]=entry_ytf[i].get()
							dd["yte"+str(i)]=entry_yte[i].get()
							dd["yrhof"+str(i)]=entry_yrhof[i].get()
							dd["yrhoe"+str(i)]=entry_yrhoe[i].get()
							dd["ylb"+str(i)]=entry_ylb[i].get()
							dd["yco"+str(i)]=entry_yco[i].get()
							dd["yls"+str(i)]=entry_yls[i].get()
							dd["yargs"+str(i)]=entry_yargs[i].get()
						except:
							pass
					self.hdf5handler.write_config("2D","Lines",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
	def TimeSequency(self): #support 0d
		bigbox=self.add_menu("Time Sequency",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"Time Sequency",fg="red",fontsize=24)
		self.add_title(bigbox,"(TimeSequency only supports 0D)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 2D TimeSequency configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("2D","TimeSequency"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading TimeSequency configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("2D","TimeSequency",savedbox.get())
				update_entry(entry_xtf,savedcfg["xtf"],False)
				update_entry(entry_xte,savedcfg["xte"],False)
				update_entry(entry_syrf,savedcfg["syrf"],False)
				update_entry(entry_syre,savedcfg["syre"],False)
				update_entry(entry_sytf,savedcfg["sytf"],False)
				update_entry(entry_syte,savedcfg["syte"],False)
				update_entry(entry_syrhof,savedcfg["syrhof"],False)
				update_entry(entry_syrhoe,savedcfg["syrhoe"],False)
				update_entry(entry_sylb,savedcfg["sylb"],False)
				update_entry(entry_syco,savedcfg["syco"],False)
				update_entry(entry_syls,savedcfg["syls"],False)
				update_entry(entry_syargs,savedcfg["syargs"],False)
				for i in range(self.maxline):
					try:
						update_entry(entry_yrf[i],savedcfg["yrf"+str(i)],False)
						update_entry(entry_yre[i],savedcfg["yre"+str(i)],False)
						update_entry(entry_ytf[i],savedcfg["ytf"+str(i)],False)
						update_entry(entry_yte[i],savedcfg["yte"+str(i)],False)
						update_entry(entry_yrhof[i],savedcfg["yrhof"+str(i)],False)
						update_entry(entry_yrhoe[i],savedcfg["yrhoe"+str(i)],False)
						update_entry(entry_ylb[i],savedcfg["ylb"+str(i)],False)
						update_entry(entry_yco[i],savedcfg["yco"+str(i)],False)
						update_entry(entry_yls[i],savedcfg["yls"+str(i)],False)
						update_entry(entry_yargs[i],savedcfg["yargs"+str(i)],False)
					except:
						pass
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_fxs,savedcfg["fxs"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fys,savedcfg["fys"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 2D TimeSequency configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting TimeSequency configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("2D","TimeSequency",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("2D","TimeSequency"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end


		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Line infomation",fg="green")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Axis").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8).pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Label").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Color").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Linestyle").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="Time Secquency",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="-",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_xtf=Entry(box,width=7)
		entry_xtf.insert(0,1)
		entry_xtf.pack(side="left")
		Label(box,text="Utim^").pack(side="left")
		entry_xte=Entry(box,width=7)
		entry_xte.insert(0,1)
		entry_xte.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="-",width=20).pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Y (Share X)").pack(side="left")
		Label(box,text="|").pack(side="left")
		self.TS_sy_qt=ttk.Combobox(box,width=17,height=10,values=self.avqt[0])
		self.TS_sy_qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syrf=Entry(box,width=7)
		entry_syrf.pack(side="left")
		entry_syrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_syre=Entry(box,width=7)
		entry_syre.pack(side="left")
		entry_syre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_sytf=Entry(box,width=7)
		entry_sytf.pack(side="left")
		entry_sytf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_syte=Entry(box,width=7)
		entry_syte.pack(side="left")
		entry_syte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_syrhof=Entry(box,width=7)
		entry_syrhof.pack(side="left")
		entry_syrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_syrhoe=Entry(box,width=7)
		entry_syrhoe.pack(side="left")
		entry_syrhoe.insert(0,0)
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8).pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_sylb=Entry(box,width=20)
		entry_sylb.insert(0,str(None))
		entry_sylb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syco=Entry(box,width=20)
		entry_syco.insert(0,str(None))
		entry_syco.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syls=Entry(box,width=20)
		entry_syls.insert(0,"-")
		entry_syls.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_syargs=Entry(box,width=20)
		entry_syargs.pack(side="left")

		entry_yrf=[]
		entry_yre=[]
		entry_ytf=[]
		entry_yte=[]
		entry_yrhof=[]
		entry_yrhoe=[]
		entry_ylb=[]
		entry_yco=[]
		entry_yls=[]
		entry_yargs=[]
		self.TS_qt=[]
		for i in range(self.maxline):
			Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(bigbox,bx=20)
			Label(box,width=8,text="Y"+str(i+1)).pack(side="left")
			Label(box,text="|").pack(side="left")
			self.TS_qt.append(ttk.Combobox(box,width=17,height=10,values=self.avqt[0]))
			self.TS_qt[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yrf.append(Entry(box,width=7))
			entry_yrf[-1].pack(side="left")
			entry_yrf[-1].insert(0,1)
			Label(box,text="Ulen^").pack(side="left")
			entry_yre.append(Entry(box,width=7))
			entry_yre[-1].pack(side="left")
			entry_yre[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_ytf.append(Entry(box,width=7))
			entry_ytf[-1].pack(side="left")
			entry_ytf[-1].insert(0,1)
			Label(box,text="Utim^").pack(side="left")
			entry_yte.append(Entry(box,width=7))
			entry_yte[-1].pack(side="left")
			entry_yte[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_yrhof.append(Entry(box,width=7))
			entry_yrhof[-1].pack(side="left")
			entry_yrhof[-1].insert(0,1)
			Label(box,text="Urho^").pack(side="left")
			entry_yrhoe.append(Entry(box,width=7))
			entry_yrhoe[-1].pack(side="left")
			entry_yrhoe[-1].insert(0,0)
			box=self.add_row(bigbox,bx=20)
			Label(box,width=8).pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_ylb.append(Entry(box,width=20))
			entry_ylb[-1].insert(0,str(None))
			entry_ylb[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yco.append(Entry(box,width=20))
			entry_yco[-1].insert(0,str(None))
			entry_yco[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yls.append(Entry(box,width=20))
			entry_yls[-1].insert(0,"-")
			entry_yls[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_yargs.append(Entry(box,width=20))
			entry_yargs[-1].pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"X")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=8)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=8)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxs=Entry(box,width=20)
		entry_fxs.insert(0,str(None))
		entry_fxs.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y Scale").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=8)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=8)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fys=Entry(box,width=20)
		entry_fys.insert(0,str(None))
		entry_fys.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawlines(event):
#			if True:
			try:
				x=[]
				for i in range(len(self.pageargs["Infobj"].database.data)):
					if self.pageargs["Infobj"].database.data[i]!=None:
						x.append(i*str_to_float(entry_xtf.get())*self.unit_t**str_to_float(entry_xte.get()))
				x=np.array(x)
				sy=self.get_y(self.TS_sy_qt,entry_syrf,entry_syre,entry_sytf,entry_syte,entry_syrhof,entry_syrhoe)
				self.tkobj.io_recv("Figuring Lines ...")
				lines=[]
				for i in range(self.maxline):
					y=self.get_y(self.TS_qt[i],entry_yrf[i],entry_yre[i],entry_ytf[i],entry_yte[i],entry_yrhof[i],entry_yrhoe[i])
					if str(y)!="False":
						lines+=self.get_line(self.get_lineinfo(x,y,entry_ylb[i],entry_yco[i],entry_yls[i],entry_yargs[i]))
					#get figinfo
				figureinfo=self.get_figureinfo(entry_ft,entry_fx,entry_fy,entry_fxs,entry_fys,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fargs)
				
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

					#begining to drow
				if str(sy)!="False":
					line_s=self.get_line(self.get_lineinfo(x,sy,entry_sylb,entry_syco,entry_syls,entry_syargs))[0]
					self.pageargs["Infobj"].Config["Painter"]["P2D"].line_share_x(line_s,*lines,**figureinfo)
				else:
					self.pageargs["Infobj"].Config["Painter"]["P2D"].line(*lines,**figureinfo)

				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawlines)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("2D","TimeSequency") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 2D TimeSequency configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving TimeSequency configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"xtf":entry_xtf.get(),
						"xte":entry_xte.get(),
						"syrf":entry_syrf.get(),
						"syre":entry_syre.get(),
						"sytf":entry_sytf.get(),
						"syte":entry_syte.get(),
						"syrhof":entry_syrhof.get(),
						"syrhoe":entry_syrhoe.get(),
						"sylb":entry_sylb.get(),
						"syco":entry_syco.get(),
						"syls":entry_syls.get(),
						"syargs":entry_syargs.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"fxs":entry_fxs.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fys":entry_fys.get(),
						"fargs":entry_fargs.get()
					}
					for i in range(self.maxline):
						try:
							dd["yrf"+str(i)]=entry_yrf[i].get()
							dd["yre"+str(i)]=entry_yre[i].get()
							dd["ytf"+str(i)]=entry_ytf[i].get()
							dd["yte"+str(i)]=entry_yte[i].get()
							dd["yrhof"+str(i)]=entry_yrhof[i].get()
							dd["yrhoe"+str(i)]=entry_yrhoe[i].get()
							dd["ylb"+str(i)]=entry_ylb[i].get()
							dd["yco"+str(i)]=entry_yco[i].get()
							dd["yls"+str(i)]=entry_yls[i].get()
							dd["yargs"+str(i)]=entry_yargs[i].get()
						except:
							pass
					self.hdf5handler.write_config("2D","TimeSequency",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)

	def Line3d(self): #support 0d
		bigbox=self.add_menu("Lines",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"3D Lines",fg="red",fontsize=24)
		self.add_title(bigbox,"(Lins only supports 1D)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 3D Lines configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("3D","Lines"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading 3D Lines configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("3D","Lines",savedbox.get())
				update_entry(entry_xrf,savedcfg["xrf"],False)
				update_entry(entry_xre,savedcfg["xre"],False)
				update_entry(entry_xtf,savedcfg["xtf"],False)
				update_entry(entry_xte,savedcfg["xte"],False)
				update_entry(entry_xrhof,savedcfg["xrhof"],False)
				update_entry(entry_xrhoe,savedcfg["xrhoe"],False)
				update_entry(entry_yrf,savedcfg["yrf"],False)
				update_entry(entry_yre,savedcfg["yre"],False)
				update_entry(entry_ytf,savedcfg["ytf"],False)
				update_entry(entry_yte,savedcfg["yte"],False)
				update_entry(entry_yrhof,savedcfg["yrhof"],False)
				update_entry(entry_yrhoe,savedcfg["yrhoe"],False)
				for i in range(self.maxline):
					try:
						update_entry(entry_zrf[i],savedcfg["zrf"+str(i)],False)
						update_entry(entry_zre[i],savedcfg["zre"+str(i)],False)
						update_entry(entry_ztf[i],savedcfg["ztf"+str(i)],False)
						update_entry(entry_zte[i],savedcfg["zte"+str(i)],False)
						update_entry(entry_zrhof[i],savedcfg["zrhof"+str(i)],False)
						update_entry(entry_zrhoe[i],savedcfg["zrhoe"+str(i)],False)
						update_entry(entry_zlb[i],savedcfg["zlb"+str(i)],False)
						update_entry(entry_zco[i],savedcfg["zco"+str(i)],False)
						update_entry(entry_zls[i],savedcfg["zls"+str(i)],False)
						update_entry(entry_zargs[i],savedcfg["zargs"+str(i)],False)
					except:
						pass
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fz,savedcfg["fz"],False)
				update_entry(entry_fza,savedcfg["fza"],False)
				update_entry(entry_fzb,savedcfg["fzb"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 3D Line configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 3D Lines configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("3D","Lines",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("3D","Lines"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Line infomation",fg="green")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Axis").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Index").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Label").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Color").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Linestyle").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=2,text="x").pack(side="left")
		self.Line3d_x_index=ttk.Combobox(box,width=3,height=10,values=self.usefultindex)
		self.Line3d_x_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		self.Line3d_x_qt=ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1])
		self.Line3d_x_qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_xrf=Entry(box,width=7)
		entry_xrf.pack(side="left")
		entry_xrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_xre=Entry(box,width=7)
		entry_xre.pack(side="left")
		entry_xre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_xtf=Entry(box,width=7)
		entry_xtf.pack(side="left")
		entry_xtf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_xte=Entry(box,width=7)
		entry_xte.pack(side="left")
		entry_xte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_xrhof=Entry(box,width=7)
		entry_xrhof.pack(side="left")
		entry_xrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_xrhoe=Entry(box,width=7)
		entry_xrhoe.pack(side="left")
		entry_xrhoe.insert(0,0)
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=2,text="Y").pack(side="left")
		self.Line3d_y_index=ttk.Combobox(box,width=3,height=10,values=self.usefultindex)
		self.Line3d_y_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		self.Line3d_y_qt=ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1])
		self.Line3d_y_qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_yrf=Entry(box,width=7)
		entry_yrf.pack(side="left")
		entry_yrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_yre=Entry(box,width=7)
		entry_yre.pack(side="left")
		entry_yre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_ytf=Entry(box,width=7)
		entry_ytf.pack(side="left")
		entry_ytf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_yte=Entry(box,width=7)
		entry_yte.pack(side="left")
		entry_yte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_yrhof=Entry(box,width=7)
		entry_yrhof.pack(side="left")
		entry_yrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_yrhoe=Entry(box,width=7)
		entry_yrhoe.pack(side="left")
		entry_yrhoe.insert(0,0)


		entry_zrf=[]
		entry_zre=[]
		entry_ztf=[]
		entry_zte=[]
		entry_zrhof=[]
		entry_zrhoe=[]
		entry_zlb=[]
		entry_zco=[]
		entry_zls=[]
		entry_zargs=[]
		self.Line3d_z_qt=[]
		self.Line3d_z_index=[]
		for i in range(self.maxline):
			Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(bigbox,bx=20)
			Label(box,width=8,text="Z"+str(i+1)).pack(side="left")
			Label(box,text="|").pack(side="left")
			self.Line3d_z_qt.append(ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1]))
			self.Line3d_z_qt[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zrf.append(Entry(box,width=7))
			entry_zrf[-1].pack(side="left")
			entry_zrf[-1].insert(0,1)
			Label(box,text="Ulen^").pack(side="left")
			entry_zre.append(Entry(box,width=7))
			entry_zre[-1].pack(side="left")
			entry_zre[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_ztf.append(Entry(box,width=7))
			entry_ztf[-1].pack(side="left")
			entry_ztf[-1].insert(0,1)
			Label(box,text="Utim^").pack(side="left")
			entry_zte.append(Entry(box,width=7))
			entry_zte[-1].pack(side="left")
			entry_zte[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_zrhof.append(Entry(box,width=7))
			entry_zrhof[-1].pack(side="left")
			entry_zrhof[-1].insert(0,1)
			Label(box,text="Urho^").pack(side="left")
			entry_zrhoe.append(Entry(box,width=7))
			entry_zrhoe[-1].pack(side="left")
			entry_zrhoe[-1].insert(0,0)
			box=self.add_row(bigbox,bx=20)
			self.Line3d_z_index.append(ttk.Combobox(box,width=6,height=10,values=self.usefultindex))
			self.Line3d_z_index[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zlb.append(Entry(box,width=20))
			entry_zlb[-1].insert(0,str(None))
			entry_zlb[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zco.append(Entry(box,width=20))
			entry_zco[-1].insert(0,str(None))
			entry_zco[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zls.append(Entry(box,width=20))
			entry_zls[-1].insert(0,"-")
			entry_zls[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zargs.append(Entry(box,width=20))
			entry_zargs[-1].pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"X")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=19)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=19)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=19)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=19)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Z").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Z limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fz=Entry(box,width=20)
		entry_fz.insert(0,"Z")
		entry_fz.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fza=Entry(box,width=19)
		entry_fza.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fzb=Entry(box,width=19)
		entry_fzb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawlines(event):
			try:
				x=self.get_x(self.Line3d_x_qt,entry_xrf,entry_xre,entry_xtf,entry_xte,entry_xrhof,entry_xrhoe,self.Line3d_x_index)
				if str(x)=="False":
					return
				y=self.get_x(self.Line3d_y_qt,entry_yrf,entry_yre,entry_ytf,entry_yte,entry_yrhof,entry_yrhoe,self.Line3d_y_index)
				if str(y)=="False":
					return
				self.tkobj.io_recv("Figuring Lines ...")
				lines=[]
				for i in range(self.maxline):
					z=self.get_x(self.Line3d_z_qt[i],entry_zrf[i],entry_zre[i],entry_ztf[i],entry_zte[i],entry_zrhof[i],entry_zrhoe[i],self.Line3d_z_index[i])
					if str(z)!="False":
						lines+=(self.get_line(self.get_lineinfo3d(x,y,z,entry_zlb[i],entry_zco[i],entry_zls[i],entry_zargs[i])))
					#get figinfo
				figureinfo=self.get_figureinfo3d(entry_ft,entry_fx,entry_fy,entry_fz,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fza,entry_fzb,entry_fargs)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

					#begining to drow

				self.pageargs["Infobj"].Config["Painter"]["P3D"].line(*lines,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawlines)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("3D","Lines") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 3D line configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving 3D Lines configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"xrf":entry_xrf.get(),
						"xre":entry_xre.get(),
						"xtf":entry_xtf.get(),
						"xte":entry_xte.get(),
						"xrhof":entry_xrhof.get(),
						"xrhoe":entry_xrhoe.get(),
						"yrf":entry_yrf.get(),
						"yre":entry_yre.get(),
						"ytf":entry_ytf.get(),
						"yte":entry_yte.get(),
						"yrhof":entry_yrhof.get(),
						"yrhoe":entry_yrhoe.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fz":entry_fz.get(),
						"fza":entry_fza.get(),
						"fzb":entry_fzb.get(),
						"fargs":entry_fargs.get()
					}
					for i in range(self.maxline):
						try:
							dd["zrf"+str(i)]=entry_zrf[i].get()
							dd["zre"+str(i)]=entry_zre[i].get()
							dd["ztf"+str(i)]=entry_ztf[i].get()
							dd["zte"+str(i)]=entry_zte[i].get()
							dd["zrhof"+str(i)]=entry_zrhof[i].get()
							dd["zrhoe"+str(i)]=entry_zrhoe[i].get()
							dd["zlb"+str(i)]=entry_zlb[i].get()
							dd["zco"+str(i)]=entry_zco[i].get()
							dd["zls"+str(i)]=entry_zls[i].get()
							dd["zargs"+str(i)]=entry_zargs[i].get()
						except:
							pass
					self.hdf5handler.write_config("3D","Lines",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
	def Surface3d(self):
		bigbox=self.add_menu("Surface",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"3D Surface",fg="red",fontsize=24)
		self.add_title(bigbox,"(3D Surface supports 2d, 3d)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 3D Surface configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("3D","Surfaces"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading 3D Surface configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("3D","Surfaces",savedbox.get())
				update_entry(entry_vrf,savedcfg["vrf"],False)
				update_entry(entry_vre,savedcfg["vre"],False)
				update_entry(entry_vtf,savedcfg["vtf"],False)
				update_entry(entry_vte,savedcfg["vte"],False)
				update_entry(entry_vrhof,savedcfg["vrhof"],False)
				update_entry(entry_vrhoe,savedcfg["vrhoe"],False)
				update_entry(entry_vargs,savedcfg["vargs"],False)
				for i in range(self.maxcross):
					try:
						update_entry(cross_x[i],savedcfg["cross_x"+str(i)],False)
						update_entry(cross_y[i],savedcfg["cross_y"+str(i)],False)
						update_entry(cross_z[i],savedcfg["cross_z"+str(i)],False)
					except:
						pass
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fz,savedcfg["fz"],False)
				update_entry(entry_fza,savedcfg["fza"],False)
				update_entry(entry_fzb,savedcfg["fzb"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 3D Surface configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 3D Surface configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("3D","Surfaces",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("3D","Surfaces"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Surface infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox)
		Label(box,width=20,text="Index").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=80,text="Other Arguments").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		self.P3DSur_Qt=ttk.Combobox(box,width=17,height=10,values=self.avqt[2]+self.avqt[3])
		self.P3DSur_Qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_vrf=Entry(box,width=7)
		entry_vrf.pack(side="left")
		entry_vrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_vre=Entry(box,width=7)
		entry_vre.pack(side="left")
		entry_vre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_vtf=Entry(box,width=7)
		entry_vtf.pack(side="left")
		entry_vtf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_vte=Entry(box,width=7)
		entry_vte.pack(side="left")
		entry_vte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_vrhof=Entry(box,width=7)
		entry_vrhof.pack(side="left")
		entry_vrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_vrhoe=Entry(box,width=7)
		entry_vrhoe.pack(side="left")
		entry_vrhoe.insert(0,0)
		box=self.add_row(bigbox)
		self.P3DSur_index=ttk.Combobox(box,width=17,height=10,values=self.usefultindex)
		self.P3DSur_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_vargs=Entry(box,width=66)
		entry_vargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end


		cross_x=[]
		cross_y=[]
		cross_z=[]
		self.add_row(bigbox)
		self.add_title(bigbox,"3D Surface cross",fg="green")
		Label(self.add_row(bigbox,bx=120),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=120)
		Label(box,width=5,text="ID").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Z").pack(side="left")
		for i in range(self.maxcross):
			Label(self.add_row(bigbox,bx=120),text="="*500).place(x=0,y=0,anchor="nw")  #next
			box=self.add_row(bigbox,bx=120)
			Label(box,width=5,text=str(i+1)).pack(side="left")
			Label(box,text="|").pack(side="left")
			cross_x.append(Entry(box,width=20))
			cross_x[-1].insert(0,i)
			cross_x[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			cross_y.append(Entry(box,width=20))
			cross_y[-1].insert(0,i)
			cross_y[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			cross_z.append(Entry(box,width=20))
			cross_z[-1].insert(0,0)
			cross_z[-1].pack(side="left")
		Label(self.add_row(bigbox,bx=120),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"X")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=19)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=19)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=19)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=19)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Z").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Z limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fz=Entry(box,width=20)
		entry_fz.insert(0,"Z")
		entry_fz.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fza=Entry(box,width=19)
		entry_fza.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fzb=Entry(box,width=19)
		entry_fzb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawsur3d(event):
			if self.P3DSur_Qt.get()=="" or self.P3DSur_index.get()=="":
				return
			try:
				self.tkobj.io_recv("Figuring Surface with",self.P3DSur_Qt.get(),"...")
				#get figinfo
				figureinfo=self.get_figureinfo3d(entry_ft,entry_fx,entry_fy,entry_fz,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fza,entry_fzb,entry_fargs)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

				#begining to drow
				factor=1
				factor*=str_to_float(entry_vrf.get())*self.unit_r**str_to_float(entry_vre.get())
				factor*=str_to_float(entry_vtf.get())*self.unit_t**str_to_float(entry_vte.get())
				factor*=str_to_float(entry_vrhof.get())*self.unit_rho**str_to_float(entry_vrhoe.get())
				ind=self.pageargs["Infobj"].database.tindex.index(int(self.P3DSur_index.get()))
				try:
					x=self.pageargs["Infobj"].database.data[ind].grid["x1"]
				except:
					x=self.pageargs["Infobj"].database.data[ind].quantities["x1"]
				try:
					y=self.pageargs["Infobj"].database.data[ind].grid["x2"]
				except:
					y=self.pageargs["Infobj"].database.data[ind].quantities["x2"]
				v=self.pageargs["Infobj"].database.data[ind].quantities[self.P3DSur_Qt.get()]*factor
				if v.ndim==2:#2d:
					if self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="SPHERICAL":
						x,y,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rot_to_xoz(x,y,v)
					elif self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="POLAR":
						x,y,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rop_to_xoy(x,y,v)

				else:#3d
					z=self.pageargs["Infobj"].database.data[ind].grid["x3"]
					if self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="SPHERICAL":
						x,y,z,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rtp_to_xyz(x,y,z,v)
					elif self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="POLAR":
						x,y,z,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rzp_to_xyz(x,z,y,v) #rzp->xzy
					cx=[str_to_float(i) for i in cross_x.get()]
					cy=[str_to_float(i) for i in cross_y.get()]
					cz=[str_to_float(i) for i in cross_z.get()]
					x,y,v=self.pageargs["Infobj"].Config["Painter"]["P3D"]._3D_to_2D(x,y,z,v,cx,cy,cz)
				
				surfaceinfo=self.get_surfaceinfo(x,y,v,entry_vargs)
				self.tkobj.io_recv("Collected surfaceinfo:",surfaceinfo)
				surface=self.pageargs["Infobj"].Config["Painter"]["Surface"].CreateSurface(**surfaceinfo)
				self.pageargs["Infobj"].Config["Painter"]["P3D"].surface(surface,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawsur3d)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("3D","Surfaces") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 3D Surface configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving 3D Surface configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"vrf":entry_vrf.get(),
						"vre":entry_vre.get(),
						"vtf":entry_vtf.get(),
						"vte":entry_vte.get(),
						"vrhof":entry_vrhof.get(),
						"vrhoe":entry_vrhoe.get(),
						"vargs":entry_vargs.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fz":entry_fz.get(),
						"fza":entry_fza.get(),
						"fzb":entry_fzb.get(),
						"fargs":entry_fargs.get()
					}
					for i in range(self.maxcross):
						try:
							dd["cross_x"+str(i)]=cross_x[i].get()
							dd["cross_y"+str(i)]=cross_y[i].get()
							dd["cross_z"+str(i)]=cross_z[i].get()
						except:
							pass
					self.hdf5handler.write_config("3D","Surfaces",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
	def TimeSequency3d(self): #support 0d
		bigbox=self.add_menu("Time Sequency",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"3D Time Sequency",fg="red",fontsize=24)
		self.add_title(bigbox,"(3D TimeSequency supports 1D)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 3D TimeSequency configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("3D","TimeSequency"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading 3D TimeSequency configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("3D","TimeSequency",savedbox.get())
				update_entry(entry_xtf,savedcfg["xtf"],False)
				update_entry(entry_xte,savedcfg["xte"],False)
				update_entry(entry_yrf,savedcfg["yrf"],False)
				update_entry(entry_yre,savedcfg["yre"],False)
				update_entry(entry_ytf,savedcfg["ytf"],False)
				update_entry(entry_yte,savedcfg["yte"],False)
				update_entry(entry_yrhof,savedcfg["yrhof"],False)
				update_entry(entry_yrhoe,savedcfg["yrhoe"],False)
				for i in range(self.maxline):
					try:
						update_entry(entry_zrf[i],savedcfg["zrf"+str(i)],False)
						update_entry(entry_zre[i],savedcfg["zre"+str(i)],False)
						update_entry(entry_ztf[i],savedcfg["ztf"+str(i)],False)
						update_entry(entry_zte[i],savedcfg["zte"+str(i)],False)
						update_entry(entry_zrhof[i],savedcfg["zrhof"+str(i)],False)
						update_entry(entry_zrhoe[i],savedcfg["zrhoe"+str(i)],False)
						update_entry(entry_zlb[i],savedcfg["zlb"+str(i)],False)
						update_entry(entry_zco[i],savedcfg["zco"+str(i)],False)
						update_entry(entry_zls[i],savedcfg["zls"+str(i)],False)
						update_entry(entry_zargs[i],savedcfg["zargs"+str(i)],False)
					except:
						pass
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fz,savedcfg["fz"],False)
				update_entry(entry_fza,savedcfg["fza"],False)
				update_entry(entry_fzb,savedcfg["fzb"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 3D Line configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 3D TimeSequency configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("3D","TimeSequency",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("3D","TimeSequency"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Line infomation",fg="green")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Axis").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8).pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Label").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Color").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Linestyle").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="Time Secquency",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="-",width=20).pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_xtf=Entry(box,width=7)
		entry_xtf.insert(0,1)
		entry_xtf.pack(side="left")
		Label(box,text="Utim^").pack(side="left")
		entry_xte=Entry(box,width=7)
		entry_xte.insert(0,1)
		entry_xte.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,text="-",width=20).pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox,bx=20)
		Label(box,width=8,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		self.TS3d_y_qt=ttk.Combobox(box,width=17,height=10,values=["x1","x2","x3"]+self.avqt[1])
		self.TS3d_y_qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_yrf=Entry(box,width=7)
		entry_yrf.pack(side="left")
		entry_yrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_yre=Entry(box,width=7)
		entry_yre.pack(side="left")
		entry_yre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_ytf=Entry(box,width=7)
		entry_ytf.pack(side="left")
		entry_ytf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_yte=Entry(box,width=7)
		entry_yte.pack(side="left")
		entry_yte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_yrhof=Entry(box,width=7)
		entry_yrhof.pack(side="left")
		entry_yrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_yrhoe=Entry(box,width=7)
		entry_yrhoe.pack(side="left")
		entry_yrhoe.insert(0,0)

		entry_zrf=[]
		entry_zre=[]
		entry_ztf=[]
		entry_zte=[]
		entry_zrhof=[]
		entry_zrhoe=[]
		entry_zlb=[]
		entry_zco=[]
		entry_zls=[]
		entry_zargs=[]
		self.TS3d_z_qt=[]
		for i in range(self.maxline):
			Label(self.add_row(bigbox,bx=20),text="-"*500).place(x=0,y=0,anchor="nw") #next
			box=self.add_row(bigbox,bx=20)
			Label(box,width=8,text="Z"+str(i+1)).pack(side="left")
			Label(box,text="|").pack(side="left")
			self.TS3d_z_qt.append(ttk.Combobox(box,width=17,height=10,values=["x1"+"x2"+"x3"]+self.avqt[1]))
			self.TS3d_z_qt[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zrf.append(Entry(box,width=7))
			entry_zrf[-1].pack(side="left")
			entry_zrf[-1].insert(0,1)
			Label(box,text="Ulen^").pack(side="left")
			entry_zre.append(Entry(box,width=7))
			entry_zre[-1].pack(side="left")
			entry_zre[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_ztf.append(Entry(box,width=7))
			entry_ztf[-1].pack(side="left")
			entry_ztf[-1].insert(0,1)
			Label(box,text="Utim^").pack(side="left")
			entry_zte.append(Entry(box,width=7))
			entry_zte[-1].pack(side="left")
			entry_zte[-1].insert(0,0)
			Label(box,text="|").pack(side="left")
			entry_zrhof.append(Entry(box,width=7))
			entry_zrhof[-1].pack(side="left")
			entry_zrhof[-1].insert(0,1)
			Label(box,text="Urho^").pack(side="left")
			entry_zrhoe.append(Entry(box,width=7))
			entry_zrhoe[-1].pack(side="left")
			entry_zrhoe[-1].insert(0,0)
			box=self.add_row(bigbox,bx=20)
			Label(box,width=8).pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zlb.append(Entry(box,width=20))
			entry_zlb[-1].insert(0,str(None))
			entry_zlb[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zco.append(Entry(box,width=20))
			entry_zco[-1].insert(0,str(None))
			entry_zco[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zls.append(Entry(box,width=20))
			entry_zls[-1].insert(0,"-")
			entry_zls[-1].pack(side="left")
			Label(box,text="|").pack(side="left")
			entry_zargs.append(Entry(box,width=20))
			entry_zargs[-1].pack(side="left")
		Label(self.add_row(bigbox,bx=20),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"Time")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=19)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=19)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=19)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=19)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Z").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Z limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fz=Entry(box,width=20)
		entry_fz.insert(0,"Z")
		entry_fz.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fza=Entry(box,width=19)
		entry_fza.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fzb=Entry(box,width=19)
		entry_fzb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawlines(event):
			try:
				self.tkobj.io_recv("Figuring Lines ...")
				lines=[]
				for i in range(len(self.pageargs["Infobj"].database.data)):
					if self.pageargs["Infobj"].database.data[i]!=None:
						x=i*str_to_float(entry_xtf.get())*self.unit_t**str_to_float(entry_xte.get())
						y=self.get_x(self.TS3d_y_qt,entry_yrf,entry_yre,entry_ytf,entry_yte,entry_yrhof,entry_yrhoe,i)
						if str(y)=="False":
							return
						for j in range(self.maxline):
							z=self.get_x(self.TS3d_z_qt[j],entry_zrf[j],entry_zre[j],entry_ztf[j],entry_zte[j],entry_zrhof[j],entry_zrhoe[j],i)
							if str(z)=="False" or len(z)!=len(y):
								continue
							lines+=self.get_line(self.get_lineinfo3d(np.full((len(y),),x),y,z,entry_zlb[j],entry_zco[j],entry_zls[j],entry_zargs[j]))
				
				#get figinfo
				figureinfo=self.get_figureinfo3d(entry_ft,entry_fx,entry_fy,entry_fz,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fza,entry_fzb)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

				rg=np.arange(0,len(lines),len(lines)/10 if len(lines)>10 else 1)
				if "Time" in figureinfo.keys():
					if type(figureinfo["Time"]) not in (list,tuple,np.ndarray):
						figureinfo["Time"]=[figureinfo["Time"]]
					for i in figureinfo["Time"]:
						if i>len(lines):
							return self.tkobj.io_recv("Error: Time list exceeds limit",color="red")
					rg=np.arange(*figureinfo["Time"])
				newlines=[]
				for i in rg:
					try:
						newlines.append(lines[int(i)])
					except:
						continue
					#begining to drow
				self.pageargs["Infobj"].Config["Painter"]["P3D"].line(*newlines,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawlines)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("3D","TimeSequency") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 3D TimeSequency configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving 3D TimeSequency configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"xtf":entry_xtf.get(),
						"xte":entry_xte.get(),
						"yrf":entry_yrf.get(),
						"yre":entry_yre.get(),
						"ytf":entry_ytf.get(),
						"yte":entry_yte.get(),
						"yrhof":entry_yrhof.get(),
						"yrhoe":entry_yrhoe.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fz":entry_fz.get(),
						"fza":entry_fza.get(),
						"fzb":entry_fzb.get(),
						"fargs":entry_fargs.get()
					}
					for i in range(self.maxline):
						try:
							dd["zrf"+str(i)]=entry_zrf[i].get()
							dd["zre"+str(i)]=entry_zre[i].get()
							dd["ztf"+str(i)]=entry_ztf[i].get()
							dd["zte"+str(i)]=entry_zte[i].get()
							dd["zrhof"+str(i)]=entry_zrhof[i].get()
							dd["zrhoe"+str(i)]=entry_zrhoe[i].get()
							dd["zlb"+str(i)]=entry_zlb[i].get()
							dd["zco"+str(i)]=entry_zco[i].get()
							dd["zls"+str(i)]=entry_zls[i].get()
							dd["zargs"+str(i)]=entry_zargs[i].get()
						except:
							pass
					self.hdf5handler.write_config("3D","TimeSequency",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)

	def Scatter3d(self):
		bigbox=self.add_menu("Scatter",submenu=2)
		self.add_row(bigbox)
		self.add_title(bigbox,"3D Scatter",fg="red",fontsize=24)
		self.add_title(bigbox,"(3D Scatter 3d)",fontsize=10)

		def reset_saved():
			self.tkobj.io_recv("Reseting 3D Scatter configuration ...")
			savedbox.config(values=()+self.hdf5handler.read_config("3D","Scatter"))
		self.reset_funs.append(reset_saved)
		def load_saved(event):
			if savedbox.get()=="":
				return
			try:
				self.tkobj.io_recv("Loading 3D Scatter configuration",savedbox.get(),"...",color="blue")
				savedcfg=self.hdf5handler.read_config("3D","Scatter",savedbox.get())
				update_entry(entry_vrf,savedcfg["vrf"],False)
				update_entry(entry_vre,savedcfg["vre"],False)
				update_entry(entry_vtf,savedcfg["vtf"],False)
				update_entry(entry_vte,savedcfg["vte"],False)
				update_entry(entry_vrhof,savedcfg["vrhof"],False)
				update_entry(entry_vrhoe,savedcfg["vrhoe"],False)
				update_entry(entry_vargs,savedcfg["vargs"],False)
				update_entry(entry_fx,savedcfg["fx"],False)
				update_entry(entry_fxa,savedcfg["fxa"],False)
				update_entry(entry_fxb,savedcfg["fxb"],False)
				update_entry(entry_ft,savedcfg["ft"],False)
				update_entry(entry_fy,savedcfg["fy"],False)
				update_entry(entry_fya,savedcfg["fya"],False)
				update_entry(entry_fyb,savedcfg["fyb"],False)
				update_entry(entry_fz,savedcfg["fz"],False)
				update_entry(entry_fza,savedcfg["fza"],False)
				update_entry(entry_fzb,savedcfg["fzb"],False)
				update_entry(entry_fargs,savedcfg["fargs"],False)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Error: unknown key",err,color="red")
		def del_saved(event):
			if savedbox.get()=="" or not messagebox.askokcancel("Delete Confirm","Delete 3D Scatter configuration "+savedbox.get()+" ?"):
				return
			self.tkobj.io_recv("Deleting 3D Scatter configuration",savedbox.get(),"...",color="blue")
			self.hdf5handler.del_config("3D","Scatter",savedbox.get())
			reset_saved()
			self.tkobj.io_recv("Operation completed",color="green")
		self.add_row(bigbox)
		self.add_title(bigbox,"Quick Box",fg="green")
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox,bx=100)
		Label(box,width=20,text="Saved Configurations | ").pack(side="left")
		savedbox=ttk.Combobox(box,width=17,height=10,values=()+self.hdf5handler.read_config("3D","Scatter"))
		savedbox.pack(side="left")
		Label(box,text="|",width=3).pack(side="left")
		button=Button(box,text="Delete",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",del_saved)
		Label(box,width=3).pack(side="left")
		button=Button(box,text="Load",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",load_saved)
		Label(self.add_row(bigbox,bx=100),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#line info
		self.add_row(bigbox)
		self.add_title(bigbox,"Scatter infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="Quantity").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of length").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of time").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="unit of density").pack(side="left")
		box=self.add_row(bigbox)
		Label(box,width=20,text="Index").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=80,text="Other Arguments").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		self.P3DCat_Qt=ttk.Combobox(box,width=17,height=10,values=self.avqt[3])
		self.P3DCat_Qt.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_vrf=Entry(box,width=7)
		entry_vrf.pack(side="left")
		entry_vrf.insert(0,1)
		Label(box,text="Ulen^").pack(side="left")
		entry_vre=Entry(box,width=7)
		entry_vre.pack(side="left")
		entry_vre.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_vtf=Entry(box,width=7)
		entry_vtf.pack(side="left")
		entry_vtf.insert(0,1)
		Label(box,text="Utim^").pack(side="left")
		entry_vte=Entry(box,width=7)
		entry_vte.pack(side="left")
		entry_vte.insert(0,0)
		Label(box,text="|").pack(side="left")
		entry_vrhof=Entry(box,width=7)
		entry_vrhof.pack(side="left")
		entry_vrhof.insert(0,1)
		Label(box,text="Urho^").pack(side="left")
		entry_vrhoe=Entry(box,width=7)
		entry_vrhoe.pack(side="left")
		entry_vrhoe.insert(0,0)
		box=self.add_row(bigbox)
		self.P3DCat_index=ttk.Combobox(box,width=17,height=10,values=self.usefultindex)
		self.P3DCat_index.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_vargs=Entry(box,width=66)
		entry_vargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end

		#Figure info
		self.add_row(bigbox)
		self.add_title(bigbox,"Figure infomation",fg="green")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #begin
		box=self.add_row(bigbox)
		Label(box,width=20,text="X").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="X limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Title").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fx=Entry(box,width=20)
		entry_fx.insert(0,"X")
		entry_fx.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fxa=Entry(box,width=19)
		entry_fxa.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fxb=Entry(box,width=19)
		entry_fxb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_ft=Entry(box,width=20)
		entry_ft.pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Y").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Y limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fy=Entry(box,width=20)
		entry_fy.insert(0,"Y")
		entry_fy.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fya=Entry(box,width=19)
		entry_fya.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fyb=Entry(box,width=19)
		entry_fyb.pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		Label(box,width=20,text="Z").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=40,text="Z limit").pack(side="left")
		Label(box,text="|").pack(side="left")
		Label(box,width=20,text="Other Args").pack(side="left")
		Label(self.add_row(bigbox),text="-"*500).place(x=0,y=0,anchor="nw") #next
		box=self.add_row(bigbox)
		entry_fz=Entry(box,width=20)
		entry_fz.insert(0,"Z")
		entry_fz.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fza=Entry(box,width=19)
		entry_fza.pack(side="left")
		Label(box,text="to").pack(side="left")
		entry_fzb=Entry(box,width=19)
		entry_fzb.pack(side="left")
		Label(box,text="|").pack(side="left")
		entry_fargs=Entry(box,width=20)
		entry_fargs.pack(side="left")
		Label(self.add_row(bigbox),text="="*500).place(x=0,y=0,anchor="nw")  #end
		def drawsur3d(event):
			if self.P3DCat_Qt.get()=="" or self.P3DCat_index.get()=="":
				return
			try:
				self.tkobj.io_recv("Figuring Scatter with",self.P3DSur_Qt.get(),"...")
				#get figinfo
				figureinfo=self.get_figureinfo3d(entry_ft,entry_fx,entry_fy,entry_fz,entry_fxa,entry_fxb,entry_fya,entry_fyb,entry_fza,entry_fzb,entry_fargs)
				self.tkobj.io_recv("Collected Figureinfo:",figureinfo)

				#begining to drow
				factor=1
				factor*=str_to_float(entry_vrf.get())*self.unit_r**str_to_float(entry_vre.get())
				factor*=str_to_float(entry_vtf.get())*self.unit_t**str_to_float(entry_vte.get())
				factor*=str_to_float(entry_vrhof.get())*self.unit_rho**str_to_float(entry_vrhoe.get())
				ind=self.pageargs["Infobj"].database.tindex.index(int(self.P3DSur_index.get()))
				try:
					x=self.pageargs["Infobj"].database.data[ind].grid["x1"]
				except:
					x=self.pageargs["Infobj"].database.data[ind].quantities["x1"]
				try:
					y=self.pageargs["Infobj"].database.data[ind].grid["x2"]
				except:
					y=self.pageargs["Infobj"].database.data[ind].quantities["x2"]
				try:
					z=self.pageargs["Infobj"].database.data[ind].grid["x3"]
				except:
					z=self.pageargs["Infobj"].database.data[ind].quantities["x3"]
				v=self.pageargs["Infobj"].database.data[ind].quantities[self.P3DSur_Qt.get()]*factor
				if self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="SPHERICAL":
					x,y,z,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rtp_to_xyz(x,y,z,v)
				elif self.pageargs["Infobj"].database.data[ind].quantities["geometry"]=="POLAR":
					x,y,z,v=self.pageargs["Infobj"].Config["Painter"]["Basic"].rzp_to_xyz(x,z,y,v) #rzp->xzy
				Scatterinfo=self.get_scatter3d(x,y,z,v,entry_vargs)
				self.tkobj.io_recv("Collected Scatterinfo:",Scatterinfo)
				Scatter=self.pageargs["Infobj"].Config["Painter"]["Scatter"].CreateScatter(**Scatterinfo)
				self.pageargs["Infobj"].Config["Painter"]["P3D"].scatter(Scatter,**figureinfo)
				self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv("Figuring failure, error:",err,color="red")
		box=self.add_row(bigbox,bx=200)
		button=Button(box,text="Draw",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",drawsur3d)
		Label(box,width=5).pack(side="left")
		entry_save=Entry(box,width=15)
		entry_save.pack(side="left")
		Label(box,width=5).pack(side="left")
		def save(event):
			try:
				if entry_save!="":
					if entry_save.get() in self.hdf5handler.read_config("3D","Scatter") and not messagebox.askokcancel("Rewrite Confirm","Rewrite 3D Scatter configuration "+entry_save.get()+" ?"):
						return
					self.tkobj.io_recv("Saving 3D Scatter configuration",entry_save.get(),"...",color="blue")
					dd={
						"SavedTime":now(),
						"vrf":entry_vrf.get(),
						"vre":entry_vre.get(),
						"vtf":entry_vtf.get(),
						"vte":entry_vte.get(),
						"vrhof":entry_vrhof.get(),
						"vrhoe":entry_vrhoe.get(),
						"vargs":entry_vargs.get(),
						"fx":entry_fx.get(),
						"fxa":entry_fxa.get(),
						"fxb":entry_fxb.get(),
						"ft":entry_ft.get(),
						"fy":entry_fy.get(),
						"fya":entry_fya.get(),
						"fyb":entry_fyb.get(),
						"fz":entry_fz.get(),
						"fza":entry_fza.get(),
						"fzb":entry_fzb.get(),
						"fargs":entry_fargs.get()
					}
					self.hdf5handler.write_config("3D","Scatter",{entry_save.get():dd})
					reset_saved()
					self.tkobj.io_recv("Operation completed",color="green")
			except Exception as err:
				self.tkobj.io_recv(err,color="red")
		button=Button(box,text="Save",width=10)
		button.pack(side="left")
		button.bind("<ButtonRelease>",save)
	def reload(self):
		self.usefultindex=[]
		for i in range(len(self.pageargs["Infobj"].database.data)):
			if self.pageargs["Infobj"].database.data[i]!=None:
				self.usefultindex.append(self.pageargs["Infobj"].database.tindex[i])
		self.LD_index.config(values=self.usefultindex)
		self.FFT_Qt.config(values=[""]+self.avqt[0])
		self.box_0D.config(values=[""]+self.avqt[0]+["geometry"])
		self.box_1D.config(values=[""]+["x1","x2","x3"]+self.avqt[1])
		self.box_2D.config(values=[""]+self.avqt[2])
		self.box_3D.config(values=[""]+self.avqt[3])
		self.P2DSur_Qt.config(values=[""]+self.avqt[2])
		self.P2DSur_index.config(values=[""]+self.usefultindex)
		self.P3DSur_Qt.config(values=[""]+self.avqt[2]+self.avqt[3])
		self.P3DSur_index.config(values=[""]+self.usefultindex)
		self.P3DCat_Qt.config(values=[""]+self.avqt[2]+self.avqt[3])
		self.P3DCat_index.config(values=[""]+self.usefultindex)
		Lineusage=[""]+["x1","x2","x3"]+self.avqt[1]
		#["TimeSequency"]+
		self.Line2d_x_qt.config(values=Lineusage)
		self.Line2d_x_index.config(values=[""]+self.usefultindex)
		self.Line2d_sy_qt.config(values=Lineusage)
		self.Line2d_sy_index.config(values=[""]+self.usefultindex)
		self.Line3d_x_qt.config(values=Lineusage)
		self.Line3d_x_index.config(values=[""]+self.usefultindex)
		self.Line3d_y_qt.config(values=Lineusage)
		self.Line3d_y_index.config(values=[""]+self.usefultindex)
		self.TS3d_y_qt.config(values=Lineusage)
		self.TS_sy_qt.config(values=[""]+self.avqt[0])
		for i in range(self.maxline):
			self.Line2d_y_qt[i].config(values=Lineusage)
			self.Line2d_y_index[i].config(values=[""]+self.usefultindex) 
			self.Line3d_z_qt[i].config(values=Lineusage)
			self.Line3d_z_index[i].config(values=[""]+self.usefultindex)
			self.TS_qt[i].config(values=[""]+self.avqt[0])
			self.TS3d_z_qt[i].config(values=Lineusage)

	def initial(self):
		self.hdf5handler=ShockFinderFiguresHDF5(self.tkobj.io_recv)
		self.set_image(self.img["logo"])
		self.add_useless_menu("Database↓")
		self.LD()
		self.LD_GS()
		self.add_useless_menu("Figure↓")
		self.UnitSet()
		self.QuickSaved()
		self.add_useless_menu("-------2D-------")
		self.TimeSequency()
		self.FFT()
		self.Line2d()
		self.Surface2d()
		self.add_useless_menu("-------3D-------")
		self.TimeSequency3d()
		self.Line3d()
		self.Surface3d()
		self.Scatter3d()