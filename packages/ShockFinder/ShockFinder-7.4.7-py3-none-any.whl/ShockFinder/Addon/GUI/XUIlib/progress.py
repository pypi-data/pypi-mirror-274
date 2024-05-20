from tkinter import Frame
#XUI V1.0
#Junxiang H. 2023.03.07
class progress:
	default_pa="#000000"
	default_pb="#ffffff"
	def __init__(self,su_p,su_t,width,height,bd=1,be=2,length=10):
		self.su_p=su_p
		self.su_t=su_t
		self.width=width-bd
		self.height=height
		self.length=length
		self.bd=bd
		self.ppa=[]
		self.ppb=[]
		for i in range(length):
			self.ppa.append(Frame(self.su_p,width=self.width,height=self.height,bd=0,bg=self.default_pa))
			self.ppa[-1].pack(side="left")
			tmpf=Frame(self.ppa[-1],width=self.width-2*self.bd,height=self.height-2*self.bd,bd=0,bg=self.default_pb)
			tmpf.place(x=self.bd,y=self.bd,anchor="nw")
			self.ppb.append(Frame(tmpf,width=0,height=self.height-2*self.bd,bd=0,bg="red"))
			if i!=length-1:
				Frame(self.su_p,width=be,height=self.height).pack(side="left")
	def get_pb_color(self,pro):
		if pro<20*self.length/10:
			return "#00ffd8"
		elif pro<40*self.length/10:
			return "#00ff7e"
		elif pro<60*self.length/10:
			return "green"
		elif pro<80*self.length/10:
			return "#f0ff00"
		else:
			return "red"
	def set_pro(self,pro,total=None,used=None,sr=""):
		color=self.get_pb_color(pro)
		rempro=pro
		for i in range(self.length):
			self.ppb[i].place_forget()
			if rempro>100/self.length:
				self.ppb[i].config(bg=color,width=self.width-2*self.bd)
				self.ppb[i].place(x=0,y=0,anchor="nw")
				rempro-=100/self.length
			elif rempro>0:
				tw=self.width-2*self.bd
				prc=rempro/(100/self.length)
				uw=int(prc*tw)
				self.ppb[i].config(bg=color,width=uw)
				self.ppb[i].place(x=0,y=0,anchor="nw")
				rempro=0
		if self.su_t!=None:
			if total==None or used==None:
				self.su_t.config(text=sr+"("+str(pro)+"%)")
			else:
				self.su_t.config(text=sr+"("+str(used)+"/"+str(total)+", "+str(pro)+"%)")
			return self.su_t.winfo_reqwidth()