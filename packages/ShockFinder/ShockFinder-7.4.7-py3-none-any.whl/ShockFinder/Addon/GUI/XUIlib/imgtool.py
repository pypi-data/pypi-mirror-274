from PIL import Image,ImageTk
from tkinter import Frame,Label
def get_img(file,width,height):
	img = Image.open(file).resize((width,height))
	return ImageTk.PhotoImage(img)
class add_image(Frame):
	def __init__(self,master,file,width=None,height=None,event=None,fun=None,**kw):
		Frame.__init__(self,master,**kw)
		self.master = master
		self.showImg(file,width,height,event,fun)
	def showImg(self,file,width,height,event,fun):
		if width!=None and height!=None:
			photo = get_img(file=file,width=width,height=height)
		elif width!=None and height==None:
			photo = get_img(file=file,width=width)
		elif width==None and height!=None:
			photo = get_img(file=file,height=height)
		else:
			photo = get_img(file=file)
		label = Label(self.master,image=photo)
		label.image = photo # 添加对图片的引用
		if event!=None:
			if type(event) is tuple or type(event) is list:
				for i in range(len(event)):
					label.bind(event[i],fun[i])
			else:
				label.bind(event,fun)
		label.pack()