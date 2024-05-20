try:
	from ShockFinder.Addon.GUI.XUIlib.imgtool import add_image
except:
	from XUIlib.imgtool import add_image
from tkinter import *
from tkinter.font import Font
from tkinter import ttk,messagebox
import threading
#XUI V1.0
#Junxiang H. 2023.03.07
def update_entry(enobj,value,ro=True):
	if ro:
		enobj.config(state="normal")
	enobj.delete(0,"end")
	enobj.insert(0,value)
	if ro:
		enobj.config(state="readonly")
def retype_string(string):
	if "." in string or "e" in string:
		try:
			string=float(string)
		except:
			if string=="None":
				string=None
			elif string=="True":
				string=True
			elif string=="False":
				string=False
	else:
		try:
			string=int(string)
		except:
			pass
	return string if type(string) !=str or len(string.split(","))==1 else [retype_string(i) for i in string.split(",")]
def checkNone(string):
	if string=="None":
		return None
	return string
def str_clean(strc):
	return strc.replace(" ","_")
def str_cut(strc,length):
	new_length=length-10
	result=""
	n=0
	for i in strc:
		if i=="\t":
			n+=6
		dof=False
		if result!="" and result[-1]=="\n" and (i.upper()>"Z" or i.upper()<"A" ) and (i>"9" or i<"0"):
			result=result[:-2]
			dof=True
		if dof:
			if i!=" ":
				result+=i
			result+="\n"
		else:
			result+=i
		n+=1
		if n==new_length:
			n=0
			if (i.upper()<="Z" and i.upper()>="A" or i<="9" and i>="0"):
				result+="-"
			elif i==" ":
				result=result[:-1]
			result+="\n"
	if result[-1]=="\n":
		result=result[:-1]
	return result
def bk_fun():
	pass
def bk_fun2(strc):
	pass
def value_bind_entry(entry1,entry2,entry2_readonly=True):
	#usage:
	#fun=lambda :value_bind_entry(entry1,entry2))
	try:
		if entry2_readonly:
			entry2.config(state="normal")
		entry2.delete(0,"end")
		entry2.insert(0,entry1.get())
		if entry2_readonly:
			entry2.config(state="readonly")
	except:
		pass
def value_bind_selector(selector1,selector2):
	#usage:
	#fun=lambda :value_bind_entry(entry1,entry2))
	#try:
		if len(selector1.values)!=len(selector2.values):
			return
		for i in selector1.values:
			if i not in selector2.values:
				return
		for i in range(len(selector1.values)):
			for j in range(len(selector2.values)):
				if selector1.values[i]==selector2.values[j]:
					if selector1.var[i].get():
						selector2.cb[j].select()
					else:
						selector2.cb[j].deselect()
	#except:
	#	pass
class Selector:
	def __init__(self,frame,values,default_values=None):
		self.var=[]
		self.cb=[]
		for i in range(len(values)):
			self.var.append(BooleanVar())
			cb=Checkbutton(frame,text=values[i],variable=self.var[-1])
			cb.pack(anchor="nw")
			if default_values!=None and i in default_values:
				cb.select()
			self.cb.append(cb)
		self.values=values
	def get(self):
		result=()
		for i in range(len(self.var)):
			if self.var[i].get():
				result+=(self.values[i],)
		return result
class page:
	set_fmb=False
	def __init__(self,tkobj,**pageargs):
		self.tkobj=tkobj
		self.smb_width=self.tkobj.smb.width-self.tkobj.smb.scrollwidth
		self.smb_height=self.tkobj.smb.height-self.tkobj.smb.scrollwidth
		self.ro_width=self.tkobj.ro.width-self.tkobj.smb.scrollwidth
		self.ro_height=self.tkobj.ro.height-self.tkobj.ro.scrollwidth
		self.fmbindex=self.tkobj.add_first_menu()
		self.pageargs=pageargs
		self.initial()
		self.show()
	def add_useless_menu(self,text=""):
		smbindex=self.tkobj.add_second_menu(self.fmbindex)
		tmpframe=Frame(self.tkobj.smb_item[self.fmbindex][smbindex][1],width=self.smb_width)
		tmpframe.pack()
		lb=Label(tmpframe,text=text,bd=2,relief="solid")
		lb.pack(side="left")
		reqw=max(tmpframe.winfo_reqwidth(),lb.winfo_reqwidth())
		tmpframe.config(width=reqw)
		dd=self.tkobj.smb_item[self.fmbindex][smbindex][0].winfo_reqwidth()-self.tkobj.smb_item[self.fmbindex][smbindex][1].winfo_reqwidth()
		reqw=max(self.tkobj.smb_item[self.fmbindex][smbindex][1].winfo_reqwidth(),tmpframe.winfo_reqwidth())
		self.tkobj.smb_item[self.fmbindex][smbindex][1].unbind("<Button-1>")
		self.tkobj.smb_item[self.fmbindex][smbindex][1].config(width=reqw,cursor="arrow")
		self.tkobj.smb_item[self.fmbindex][smbindex][0].config(width=reqw+dd)
		return smbindex
	def add_menu(self,text="",submenu=0):
		text=submenu*"|----->"+text
		smbindex=self.tkobj.add_second_menu(self.fmbindex)
		tmpframe=Frame(self.tkobj.smb_item[self.fmbindex][smbindex][1],width=self.smb_width)
		tmpframe.pack()
		lb=Label(tmpframe,text=text,fg="red" if submenu==0 else "blue" if submenu==1 else "green")
		lb.pack(side="left")
		lb.bind("<Button-1>",lambda x:self.tkobj.open_ro(x,self.fmbindex,smbindex))
		reqw=max(tmpframe.winfo_reqwidth(),lb.winfo_reqwidth())
		tmpframe.config(width=reqw)
		dd=self.tkobj.smb_item[self.fmbindex][smbindex][0].winfo_reqwidth()-self.tkobj.smb_item[self.fmbindex][smbindex][1].winfo_reqwidth()
		reqw=max(self.tkobj.smb_item[self.fmbindex][smbindex][1].winfo_reqwidth(),tmpframe.winfo_reqwidth())
		self.tkobj.smb_item[self.fmbindex][smbindex][1].config(width=reqw)
		self.tkobj.smb_item[self.fmbindex][smbindex][0].config(width=reqw+dd)
		return smbindex
	def add_item(self,smbindex,height=None):
		return self.tkobj.add_ro(self.fmbindex,smbindex,height)
	def set_item(self,smbindex,roindex,tktype=Label,text=None,length=60,fontsize=18,fg="black"):
		tmp=tktype(self.tkobj.ro_item[self.fmbindex][smbindex][roindex][1],bd=0)
		try:
			tmp.config(text=str_cut(text,length),font=Font(size=fontsize),fg=fg,width=length)
		except:
			pass
		tmp.pack(side="top")
		self.update_window(tmp,smbindex,roindex)
		return tmp
	def add_row(self,smbindex,height=50,bx=50):
		item=self.add_item(smbindex,height)
		box=Frame(self.tkobj.ro_item[self.fmbindex][smbindex][item][1],width=self.tkobj.ro_item[self.fmbindex][smbindex][item][1].winfo_reqwidth()-2*bx,height=height)
		box.place(x=bx,y=0,anchor="nw")
		#return (box,self.tkobj.ro_item[self.fmbindex][smbindex][item][0])
		return box
	def add_title(self,smbindex,title,height=50,fg="blue",fontsize=16):
		#box=self.add_row(smbindex,height,bx=(self.tkobj.ro.useframe.winfo_reqwidth()-len(title)*fontsize**0.88)/2)[0]
		box=self.add_row(smbindex,height,bx=(self.tkobj.ro.useframe.winfo_reqwidth()-len(title)*fontsize**0.88)/2)
		Label(box,text=title,font=Font(size=fontsize),fg=fg,width=len(title)).pack(anchor="center")
	def update_window(self,frame,smbindex,roindex):
		dd=self.tkobj.ro_item[self.fmbindex][smbindex][roindex][0].winfo_reqwidth()-self.tkobj.ro_item[self.fmbindex][smbindex][roindex][1].winfo_reqwidth()
		self.tkobj.ro_item[self.fmbindex][smbindex][roindex][1].config(width=max(self.tkobj.ro_item[self.fmbindex][smbindex][roindex][1].winfo_reqwidth(),frame.winfo_reqwidth()))
		self.tkobj.ro_item[self.fmbindex][smbindex][roindex][0].config(width=self.tkobj.ro_item[self.fmbindex][smbindex][roindex][0].winfo_reqwidth()+dd)
	def initial(self):
		pass
	def show(self):
		pass
	def set_image(self,imgdir):
		if not self.set_fmb:
			add_image(self.tkobj.fmb_item[self.fmbindex][1],imgdir,width=self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-self.tkobj.get_pars("fmb_bd"),height=self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-self.tkobj.get_pars("fmb_bd"),event="<Button-1>",fun=lambda x:self.tkobj.open_smb(x,self.fmbindex))
			self.set_fmb=True
	def set_text(self,strc):
		if not self.set_fmb:
			lb=Label(self.tkobj.fmb_item[self.fmbindex][1],text=strc)
			lb.place(x=0,y=(self.tkobj.fmb.height-self.tkobj.fmb.scrollwidth-2*self.tkobj.get_pars("fmb_bd"))/2,anchor="nw")
			lb.bind("<Button-1>",lambda x:self.tkobj.open_smb(x,self.fmbindex))
			self.set_fmb=True
	def show_error(self,error):
		def show_errmsg():
			messagebox.showerror(title="Invalid data input",message=error)
		threading.Thread(target=show_errmsg).start()
	'''
	def page_basic(self,value_name,value_type,value_defualt,describe,check_fun=None,errmsg="",values=None,button_text="set",describe_height=150,enth=50,selh=300,bkh=50,txw=17,submenu=0,fun=bk_fun):
		dentstr="|----->"
		if submenu>0:
			submenu-=1
		menu=self.add_menu(len(dentstr)*" "*submenu+dentstr+value_name)
		self.add_item(menu,bkh)
		self.set_item(menu,self.add_item(menu,describe_height),text="\t"+describe)
		type1=(Entry,"Entry-readonly")
		type2=(ttk.Combobox,)
		type3=(Selector,)
		if value_type==None:
			return menu
		elif value_type in type1:
			inputbox=self.set_item(menu,self.add_item(menu,enth),Frame)
			Label(inputbox,text="\t\t\t\t"+value_name+": ").pack(side="left")
			value=Entry(inputbox,width=txw)
			value.insert(0,value_defualt)
			value.pack(side="left")
			if value_type=="Entry-readonly":
				value.config(state="readonly")	
		elif value_type in type2:
			inputbox=self.set_item(menu,self.add_item(menu,enth),Frame)
			Label(inputbox,text="\t\t\t\t"+value_name+": ").pack(side="left")
			value=value_type(inputbox,width=txw,values=values)
			value.pack(side="left")
			value.current(value_defualt)
		elif value_type in type3:
			inputbox=self.set_item(menu,self.add_item(menu,selh),Frame)
			Label(inputbox,text="\t\t\t\t"+value_name+": ").pack(side="left")
			f=Frame(inputbox,width=selh,height=selh,bd=0)
			f.pack(side="left")
			sel=value_type(f,values,value_defualt)
			value=sel
		if value_type not in ("Entry-readonly",):
			button=Button(inputbox,text=button_text)
			button.pack(side="left")
			def fun_button(event):
				fun() #do something
			button.bind("<Button-1>",fun_button)
		return (menu,value)
	'''