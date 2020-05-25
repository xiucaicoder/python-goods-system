import pymssql
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkFont
from tkinter import * 
import tkinter.messagebox as messagebox # 弹窗
# 打包的时候会用到（十进制的一个库）
import decimal
decimal.__version__

 
class StartPage:
	def __init__(self, parent_window):
		parent_window.destroy() # 销毁上一个窗口
		self.window = tk.Tk()  # 初始框的声明
		self.window.title('商品信息管理系统')
		self.window.geometry('300x410+500+100') # 这里的乘是小x，第一个参数表示窗口的长，第二个表示宽，第三个表示的距离屏幕左边界的距离，第三个为距离上边界的距离
 
		label = Label(self.window, text="商品信息管理系统", font=("Verdana", 20))
		label.pack(pady=100)  # pady=100 这个label距离窗口上边界的距离，这里设置为100刚好居中
 
		# command=lambda:  可以带参数，注意带参数的类不要写括号，否者，这里调用会直接执行(class test:)
		Button(self.window, text="管理员登陆", font=tkFont.Font(size=16), command=lambda: AdminPage(self.window), width=30, height=2,
			   fg='white', bg='gray', activebackground='black', activeforeground='white').pack()	# pack() 方法会使得组件在窗口中自动布局
		Button(self.window, text="数据库初始化", font=tkFont.Font(size=16), command=self.Initialization, width=30, height=2,
			   fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
		Button(self.window, text="退出系统", height=2, font=tkFont.Font(size=16), width=30, command=self.window.destroy,
			   fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
 
		self.window.mainloop() # 主消息循环


	# 创建数据库
	def Initialization(self):
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'master') # 服务器名,账户,密码,数据库名
		cursor = db.cursor()
		print('建立数据库中......')
		sql = """
		-- 创建EMIS数据库
		CREATE DATABASE EMIS ON PRIMARY
		(
			NAME='EMIS_data',--主文件逻辑文件名
			FILENAME='G:\\SQL Server\\EMIS_data.mdf', --主文件文件名
			SIZE=5mb,--系统默认创建的时候会给主文件分配初始大小
			MAXSIZE=500MB,--主文件的最大值
			filegrowth=15%-- 主文件的增长幅度
		)
		LOG ON
		(
			name='EMIS_log',--日志文件逻辑文件名
			filename='G:\\SQL Server\\EMIS_log.ldf',--日志文件屋里文件名
			SIZE=5MB,--日志文件初始大小
			filegrowth=0 --启动自动增长
		)
		"""

		try:
			db.autocommit(True)     # 这个句话可以防止python创建数据库的时候报错（python连接数据库机制的问题）
			cursor.execute(sql)
			db.commit()
		except:
			messagebox.showinfo('警告！', '数据库连接失败！')
		cursor.close()  # 关闭游标
		db.close()  # 关闭数据库连接
		self.jianbiao() # 进行建表操作

	# 创建数据表
	def jianbiao(self):
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') # 服务器名,账户,密码,数据库名
		cursor = db.cursor()
		print('建立数据表中......')
		sql = """
		---创建管理员数据表
		CREATE TABLE t_admin (
		admin_id varchar(255) NOT NULL,
		admin_pass varchar(255) DEFAULT NULL,
		PRIMARY KEY (admin_id)
		);

		---插入管理账户和密码
		INSERT INTO t_admin VALUES ('admin', 'admin');


		---创建商品表
		CREATE TABLE t_goods (
		id varchar(20) NOT NULL,
		name varchar(20) DEFAULT NULL,
		gender varchar(7) DEFAULT NULL,
		age varchar(7) DEFAULT NULL,
		PRIMARY KEY (id)
		);
		
		---向学生表中插入数据
		INSERT INTO t_goods VALUES ('1000000', '小米1', '1999', '1000');
		INSERT INTO t_goods VALUES ('1000001', '小米2', '1999', '1500');
		INSERT INTO t_goods VALUES ('1000002', '小米3', '1999', '1000');
		INSERT INTO t_goods VALUES ('1000003', '小米4', '1999', '900');
		INSERT INTO t_goods VALUES ('1000004', '小米5', '1999', '2000');
		INSERT INTO t_goods VALUES ('1000005', '小米6', '2499', '10000');
		INSERT INTO t_goods VALUES ('1000006', '小米8', '2599', '20000');

		
		---创建买家信息数据表
		CREATE TABLE t_buyer (
		SNO varchar(20) NOT NULL,
		NAME varchar(255) DEFAULT NULL,
		NUMBER varchar(255) DEFAULT NULL,
		dizhi varchar(255) DEFAULT NULL
		);
		
		---向卖家信息数据表中插入数据
		INSERT INTO t_buyer VALUES ('08300205', '小红', '1', '天津市');
		INSERT INTO t_buyer VALUES ('08300206', '小明', '3', '北京市');
		INSERT INTO t_buyer VALUES ('08300207', '小芬', '1', '安阳市');
		INSERT INTO t_buyer VALUES ('08080929', '小爱', '10', '武汉市');


		---创建订单信息表
		CREATE TABLE t_order(
		id varchar(20) NOT NULL,
		SNO varchar(20) DEFAULT NULL,
		buy_time varchar(255) DEFAULT NULL,
		vic varchar(255) DEFAULT NULL,
		buy_money varchar(255) DEFAULT NULL,
		PRIMARY KEY (SNO)
		);
		
		---向订单信息表中插入数据
		INSERT INTO t_order VALUES ('1000000', '08300205', '2013-7', '是', '1899');
		INSERT INTO t_order VALUES ('1000002', '08300206', '2014-5', '是', '1999');
		INSERT INTO t_order VALUES ('1000003', '08300207', '2018-9', '是', '2499');
		INSERT INTO t_order VALUES ('1000004', '08080929', '2019-12', '是', '2999');
		"""

		try:
			cursor.execute(sql)
			db.commit()
		except:
			messagebox.showinfo('警告！', '数据库连接失败！')
		cursor.close()  # 关闭游标
		db.close()  # 关闭数据库连接
		self.create_chufaqi()

	# 创建触发器
	def create_chufaqi(self):
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') # 服务器名,账户,密码,数据库名
		cursor = db.cursor()
		print('建立触发器中......')
		sql = """
		--- 为商品表和订单表创建update触发器
		create Trigger tru_goods 
		On t_goods                         --在Student表中创建触发器 
		for Update                         --为什么事件触发 
		As                                 --事件触发后所要做的事情 
		IF update(id)
		BEGIN
		declare @stuidnew varchar(20) --从临时表Inserted记录新的的学号ID 
		declare @stuidold varchar(20) --从临时表Deleted记录跟新以前旧的的学号ID
		select @stuidold=id from Deleted
		select @stuidnew=id from Inserted
		update t_order set id=@stuidnew where id=@stuidold
		print @stuidnew
		print @stuidold
		end
		"""

		try:
			cursor.execute(sql)
			db.commit()
		except:
			messagebox.showinfo('警告！', '数据库连接失败！')
		cursor.close()  # 关闭游标
		db.close()  # 关闭数据库连接
		self.create_cunchu1() # 创建触发器1

	# 创建存储过程1
	def create_cunchu1(self):
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') # 服务器名,账户,密码,数据库名
		cursor = db.cursor()
		print('建立存储过程1中......')
		sql = """
		-- 创建删除指定行的存储过程
		create procedure proc_delete
		@商品id varchar(20)
		as 
		DELETE FROM t_goods WHERE id = @商品id
		--use EMIS
		--exec proc_delete 00001
		"""

		try:
			cursor.execute(sql)
			db.commit()
		except:
			messagebox.showinfo('警告！', '数据库连接失败！')
		cursor.close()  # 关闭游标
		db.close()  # 关闭数据库连接
		self.create_cunchu2()

	# 创建存储过程2
	def create_cunchu2(self):
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') # 服务器名,账户,密码,数据库名
		cursor = db.cursor()
		print('建立存储过程2中......')
		sql = """
		-- 创建查询的存储过程
		create procedure proc_cha
		@name varchar(20)
		as 
		select * from t_goods
		where name=@name
		--use EMIS
		--exec proc_cha 小米
		"""

		try:
			cursor.execute(sql)
			db.commit()
			messagebox.showinfo('提示', '数据库已成功初始化')
		except:
			messagebox.showinfo('警告！', '数据库连接失败！')
		cursor.close()  # 关闭游标
		db.close()  # 关闭数据库连接

 
#管理员登陆页面
class AdminPage:
	def __init__(self, parent_window):
		parent_window.destroy() # 销毁上一个界面
		self.window = tk.Tk()  # 初始框的声明
		self.window.title('管理员登陆页面')
		self.window.geometry('450x300+500+100')

		# 创建画布，这里可以存放照片等组件
		canvas = tk.Canvas(self.window, height=200, width=500)
		image_file = tk.PhotoImage(file='welcome.gif')
		image = canvas.create_image(0,0, anchor='nw', image=image_file)	# 前两个参数为画布得坐标，anchor=nw则是把图片的左上角作为锚定点
		canvas.pack(side='top')	# 使用pack将画布进行简单得布局，放到了上半部分

		# 创建提示信息
		tk.Label(self.window, text='登录名: ').place(x=80, y= 150)
		tk.Label(self.window, text='登陆密码: ').place(x=80, y= 190)

		self.admin_username = tk.Entry(self.window)
		self.admin_username.place(x=160, y=150)
		self.admin_pass = tk.Entry(self.window, show='*')
		self.admin_pass.place(x=160, y=190)
		# 登陆和返回首页得按钮
		btn_login = tk.Button(self.window, text='登陆',  width=10, command=self.login)
		btn_login.place(x=120, y=230)
		btn_back = Button(self.window, text="返回首页", width=8, font=tkFont.Font(size=12), command=self.back)
		btn_back.place(x=270, y=230)
		self.window.mainloop()

	# 登陆的函数
	def login(self): 
		# 数据库操作 查询管理员表
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') # 服务器名,账户,密码,数据库名
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "SELECT * FROM t_admin where admin_id = '%s'" % (self.admin_username.get())  # 这里得user_name即为admin_id，这里是输入的用户名
		try:
		# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表，这里是返回的二元元组，如(('id','title'),('id','title'))
			results = cursor.fetchall()
			for row in results:
				admin_id = row[0]
				admin_pass = row[1]
				# 打印结果
				print("管理员账号为：%s, \n\n管理员密码为：%s" % (admin_id, admin_pass))
		except:
			print("Error: unable to fecth data")
			messagebox.showinfo('警告！', '用户名或密码不正确！')
		db.close()  # 关闭数据库连接

		print("正在登陆管理员管理界面.......")

		# 判断输入的账号密码与数据库中的信息是否一致a
		if self.admin_pass.get() == admin_pass:
			All_admin(self.window)   # 进入管理员子菜单操作界面
		else:
			messagebox.showinfo('警告！', '用户名或密码不正确！')

	# 使得系统点击关闭的x号上返回指定页面，而不是关闭
	def back(self):
		StartPage(self.window) # 显示主窗口 销毁本窗口
 

# 管理员子菜单操作界面
class All_admin:
	def __init__(self, parent_window):
		parent_window.destroy() # 自定销毁上一个界面
		self.window = tk.Tk()  # 初始框的声明
		self.window.title('信息管理界面')
		self.window.geometry('300x410+500+100')
		label = Label(self.window, text="请选择需要进行的操作", font=("Verdana", 20))
		label.pack(pady=100)  # pady=100 界面的长度

		Button(self.window, text="商品信息管理", font=tkFont.Font(size=16), width=30, height=2, command=lambda: AdminManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
		Button(self.window, text="买家信息管理", font=tkFont.Font(size=16), width=30,height=2, command=lambda:User_AdminManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()
		Button(self.window, text="订单信息管理", font=tkFont.Font(size=16), width=30, height=2, command=lambda:Buy_AdminManage(self.window),
			fg='white', bg='gray', activebackground='black', activeforeground='white').pack()

		self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
		self.window.mainloop()  # 进入消息循环

	def back(self):
		StartPage(self.window) # 显示主窗口 销毁本窗口


# 商品信息操作界面
class AdminManage:
	def __init__(self, parent_window):
		parent_window.destroy() 	# 自动销毁上一个界面
		self.window = Tk()  		# 初始框的声明
		self.window.title('管理员操作界面')
		self.window.geometry("650x685+300+30")	# 初始窗口在屏幕中的位置
		self.frame_left_top = tk.Frame(width=300, height=200)	# 指定框架，在窗口上可以显示，这里指定四个框架	
		self.frame_right_top = tk.Frame(width=200, height=200)
		self.frame_center = tk.Frame(width=500, height=350)
		self.frame_bottom = tk.Frame(width=650, height=70)
 
		# 定义下方中心列表区域
		self.columns = ("商品id", "商品名称", "商品价格", "销售数量")
		self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
        # 添加竖直滚动条
		self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
		# 定义树形结构与滚动条
		self.tree.configure(yscrollcommand=self.vbar.set)

		# 定义id1为修改id时的暂存变量，这个是为了更新信息而设计的
		self.id1 = 0
 
		# 表格的标题
		self.tree.column("商品id", width=150, anchor='center')
		self.tree.column("商品名称", width=150, anchor='center')
		self.tree.column("商品价格", width=100, anchor='center')
		self.tree.column("销售数量", width=100, anchor='center')
 
		# grid方法将tree和vbar进行布局
		self.tree.grid(row=0, column=0, sticky=NSEW)
		self.vbar.grid(row=0, column=1, sticky=NS)
	
		# 定义几个数组，为中间的那个大表格做一些准备
		self.id = []
		self.name = []
		self.gender = []
		self.age = []

		# 打开数据库连接
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "SELECT * FROM t_goods"
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				self.id.append(row[0])
				self.name.append(row[1])
				self.gender.append(row[2])
				self.age.append(row[3])
		except:
			messagebox.showinfo('警告！', '数据库连接失败！')
		db.close()# 关闭数据库连接
 
 
		print("test***********************")
		for i in range(min(len(self.id), len(self.name), len(self.gender), len(self.age))):  # 写入数据
			self.tree.insert('', i, values=(self.id[i], self.name[i], self.gender[i], self.age[i]))
 
		for col in self.columns:  # 绑定函数，使表头可排序(这里的command=lambda _col=col还不是太懂)
			self.tree.heading(col, text=col, command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
		self.top_title = Label(self.frame_left_top, text="商品信息:", font=('Verdana', 20))
		self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)   # NSEW表示允许组件向4个方向都可以拉伸

		# 定义下方区域
		self.chaxun = StringVar()
		self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
		self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
		self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
		self.right_bottom_gender_entry.grid(row=0, column=1)
 
		self.left_top_frame = tk.Frame(self.frame_left_top)
		self.var_id = StringVar()  # 声明学号
		self.var_name = StringVar()  # 声明姓名
		self.var_gender = StringVar()  # 声明性别
		self.var_age = StringVar()  # 声明年龄
		# 商品id
		self.right_top_id_label = Label(self.frame_left_top, text="商品id： ", font=('Verdana', 15))
		self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
		self.right_top_id_label.grid(row=1, column=0)
		self.right_top_id_entry.grid(row=1, column=1)
		# 商品名称
		self.right_top_name_label = Label(self.frame_left_top, text="商品名称：", font=('Verdana', 15))
		self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
		self.right_top_name_label.grid(row=2, column=0)  # 位置设置
		self.right_top_name_entry.grid(row=2, column=1)
		# 商品价格
		self.right_top_gender_label = Label(self.frame_left_top, text="商品价格：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_gender,font=('Verdana', 15))
		self.right_top_gender_label.grid(row=3, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=3, column=1)
		# 销售数量
		self.right_top_gender_label = Label(self.frame_left_top, text="销售数量：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_age, font=('Verdana', 15))
		self.right_top_gender_label.grid(row=4, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=4, column=1)
 
		# 定义右上方区域
		self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))
		self.tree.bind('<Button-1>', self.click)  # 左键获取位置(tree.bind可以绑定一系列的事件，可以搜索ttk相关参数查看)
		self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)
		self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=20,command=self.updata_row)
		self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=20,command=self.del_row)
 

		# 定义下方区域，查询功能块
		self.chaxun = StringVar()
		self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
		self.right_bottom_button = ttk.Button(self.frame_bottom, text='商品名称查询', width=20, command=self.put_data)
		self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
		self.right_bottom_gender_entry.grid(row=0, column=1)


		# 右上角按钮的位置设置
		self.right_top_title.grid(row=1, column=0, pady=10)
		self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
		self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
		self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
 
		# 整体区域定位，利用了Frame和grid进行布局
		self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
		self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
		self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
		self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		# 设置固定组件，(0)就是将组件进行了固定
		self.frame_left_top.grid_propagate(0)
		self.frame_right_top.grid_propagate(0)
		self.frame_center.grid_propagate(0)
		self.frame_bottom.grid_propagate(0)
 
		self.frame_left_top.tkraise() # 开始显示主菜单，tkraise()提高z轴的顺序（不太懂）
		self.frame_right_top.tkraise() # 开始显示主菜单
		self.frame_center.tkraise() # 开始显示主菜单
		self.frame_bottom.tkraise() # 开始显示主菜单
 
		self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击，执行back方法
		self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
	def put_data(self):
		self.delButton()	# 先将表格内的内容全部清空

		# print(self.chaxun.get())	# 输入框内的内容	
		# 打开数据库连接，准备查找指定的信息
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "use EMIS   exec proc_cha '%s'"  % (self.chaxun.get())
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()

			# 再次进行初始化，进行首行数据的插入
			self.id = []
			self.name = []
			self.gender = []
			self.age = []
			# 向表格中插入数据
			for row in results:
				self.id.append(row[0])
				self.name.append(row[1])
				self.gender.append(row[2])
				self.age.append(row[3])

		except:
			print("Error: unable to fetch data")
			messagebox.showinfo('警告！', '数据库连接失败！')
			db.close()# 关闭数据库连接
		
		print("进行数据的插入")
		for i in range(min(len(self.id), len(self.name), len(self.gender), len(self.age))):  # 写入数据
			self.tree.insert('', i, values=(self.id[i], self.name[i], self.gender[i], self.age[i]))
 
		for col in self.columns:  # 绑定函数，使表头可排序
			self.tree.heading(col, text=col,
							  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))


	# 清空表格中的所有信息
	def delButton(self):
		x=self.tree.get_children()
		for item in x:
			self.tree.delete(item)


	# 在表格上的点击事件，这里是作用就是一点击表格就可以将信息直接写到左上角的框框中
	def click(self, event):
		self.col = self.tree.identify_column(event.x)  # 通过tree.identify_column()函数可以直接获取到列
		self.row = self.tree.identify_row(event.y)  # 行
 
		print(self.col)
		print(self.row)
		self.row_info = self.tree.item(self.row, "values")
		self.var_id.set(self.row_info[0])
		self.id1 = self.var_id.get()
		self.var_name.set(self.row_info[1])
		self.var_gender.set(self.row_info[2])
		self.var_age.set(self.row_info[3])
		self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id, font=('Verdana', 15))
 
	# 点击中间的表格的表头，可以将那一列进行排序
	def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
		l = [(tv.set(k, col), k) for k in tv.get_children('')]
		l.sort(reverse=reverse)  # 排序方式
		for index, (val, k) in enumerate(l):  # 根据排序后索引移动
			tv.move(k, '', index)
		tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
 
	def new_row(self):
		print('123')
		print(self.var_id.get())
		print(self.id)
		if str(self.var_id.get()) in self.id:
			messagebox.showinfo('警告！', '该商品已存在！')
		else:
			if self.var_id.get() != '' and self.var_name.get() != '' and self.var_gender.get() != '' and self.var_age.get() != '':
				# 打开数据库连接
				db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
				cursor = db.cursor()  # 使用cursor()方法获取操作游标
				sql = "INSERT INTO t_goods(id, name, gender, age) \
				       VALUES ('%s', '%s', '%s', '%s')" % \
					  (self.var_id.get(), self.var_name.get(), self.var_gender.get(), self.var_age.get())  # SQL 插入语句
				try:
					cursor.execute(sql)  # 执行sql语句
					db.commit()  # 提交到数据库执行
				except:
					db.rollback()  # 发生错误时回滚
					messagebox.showinfo('警告！', '数据库连接失败！')
				db.close()  # 关闭数据库连接
 
				self.id.append(self.var_id.get())
				self.name.append(self.var_name.get())
				self.gender.append(self.var_gender.get())
				self.age.append(self.var_age.get())
				self.tree.insert('', len(self.id) - 1, values=(
				self.id[len(self.id) - 1], self.name[len(self.id) - 1], self.gender[len(self.id) - 1],
				self.age[len(self.id) - 1]))
				self.tree.update()
				messagebox.showinfo('提示！', '插入成功！')
			else:
				messagebox.showinfo('警告！', '请填写商品信息')
 
	def updata_row(self):
		res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
		if res == True:
			# 打开数据库连接
			db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
			cursor = db.cursor()  # 使用cursor()方法获取操作游标
			sql = "UPDATE t_goods SET id = '%s', name = '%s', gender = '%s', age = '%s' where id = '%s'" % (self.var_id.get(), self.var_name.get(), self.var_gender.get(), self.var_age.get(), self.id1)  # SQL 插入语句
			try:
				cursor.execute(sql)  # 执行sql语句
				db.commit()  # 提交到数据库执行
				messagebox.showinfo('提示！', '更新成功！')
			except:
				db.rollback()  # 发生错误时回滚
				messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
			db.close()  # 关闭数据库连接

			id_index = self.id.index(self.row_info[0])
			self.name[id_index] = self.var_name.get()
			self.gender[id_index] = self.var_gender.get()
			self.age[id_index] = self.var_age.get()

			self.tree.item(self.tree.selection()[0], values=(
				self.var_id.get(), self.var_name.get(), self.var_gender.get(),
				self.var_age.get()))  # 修改对于行信息

	# 删除行
	def del_row(self):
		res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
		if res == True:
			print(self.row_info[0])  # 鼠标选中的学号
			print(self.tree.selection()[0])  # 行号
			print(self.tree.get_children())  # 所有行
			# 打开数据库连接
			db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') 
			cursor = db.cursor()  # 使用cursor()方法获取操作游标
			sql = "use EMIS exec proc_delete '%s'" % (self.row_info[0]) # SQL 插入语句
			try:
				cursor.execute(sql)  # 执行sql语句
				db.commit()  # 提交到数据库执行
				messagebox.showinfo('提示！', '删除成功！')
			except:
				db.rollback()  # 发生错误时回滚
				messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
			db.close()  # 关闭数据库连接
 
			id_index = self.id.index(self.row_info[0])
			print(id_index)
			del self.id[id_index]
			del self.name[id_index]
			del self.gender[id_index]
			del self.age[id_index]
			print(self.id)
			self.tree.delete(self.tree.selection()[0])  # 删除所选行
			print(self.tree.get_children())

	def back(self):
		All_admin(self.window)   # 进入管理员子菜单操作界面 
 

# 买家信息操作界面
class User_AdminManage:
	def __init__(self, parent_window):
		parent_window.destroy() # 销毁主界面
 
		self.window = Tk()  # 初始框的声明
		self.window.title('管理员操作界面')
		self.window.geometry("650x685+300+30")	# 初始窗口在屏幕中的位置
		self.frame_left_top = tk.Frame(width=300, height=200)
		self.frame_right_top = tk.Frame(width=200, height=200)
		self.frame_center = tk.Frame(width=500, height=350)
		self.frame_bottom = tk.Frame(width=650, height=70)

		self.id1 = 0

		# 定义下方中心列表区域
		self.columns = ("订单id", "购买者姓名", "购买数量", "收货地址")
		self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
		self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
		# 定义树形结构与滚动条
		self.tree.configure(yscrollcommand=self.vbar.set)
 
		# 表格的标题
		self.tree.column("订单id", width=150, anchor='center')  # 表示列,不显示
		self.tree.column("购买者姓名", width=150, anchor='center')
		self.tree.column("购买数量", width=100, anchor='center')
		self.tree.column("收货地址", width=100, anchor='center')
 
		# 调用方法获取表格内容插入
		self.tree.grid(row=0, column=0, sticky=NSEW)
		self.vbar.grid(row=0, column=1, sticky=NS)
 
		self.id = []
		self.name = []
		self.gender = []
		self.age = []
		# 打开数据库连接
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "SELECT * FROM t_buyer"  # SQL 查询语句
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				self.id.append(row[0])
				self.name.append(row[1])
				self.gender.append(row[2])
				self.age.append(row[3])
		except:
			print("Error: unable to fetch data")
			messagebox.showinfo('警告！', '数据库连接失败！')
		db.close()# 关闭数据库连接
 
 
		print("test***********************")
		for i in range(min(len(self.id), len(self.name), len(self.gender), len(self.age))):  # 写入数据
			self.tree.insert('', i, values=(self.id[i], self.name[i], self.gender[i], self.age[i]))
 
		for col in self.columns:  # 绑定函数，使表头可排序
			self.tree.heading(col, text=col,
							  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
		self.top_title = Label(self.frame_left_top, text="商品信息:", font=('Verdana', 20))
		self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)
 
		self.left_top_frame = tk.Frame(self.frame_left_top)
		self.var_id = StringVar()  # 声明学号
		self.var_name = StringVar()  # 声明姓名
		self.var_gender = StringVar()  # 声明性别
		self.var_age = StringVar()  # 声明年龄
		# 学号
		self.right_top_id_label = Label(self.frame_left_top, text="订单id： ", font=('Verdana', 15))
		self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
		self.right_top_id_label.grid(row=1, column=0)  # 位置设置
		self.right_top_id_entry.grid(row=1, column=1)
		# 姓名
		self.right_top_name_label = Label(self.frame_left_top, text="购买者姓名：", font=('Verdana', 15))
		self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
		self.right_top_name_label.grid(row=2, column=0)  # 位置设置
		self.right_top_name_entry.grid(row=2, column=1)
		# 性别
		self.right_top_gender_label = Label(self.frame_left_top, text="购买数量：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_gender,
											font=('Verdana', 15))
		self.right_top_gender_label.grid(row=3, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=3, column=1)
		# 年龄
		self.right_top_gender_label = Label(self.frame_left_top, text="收货地址：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_age,
											font=('Verdana', 15))
		self.right_top_gender_label.grid(row=4, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=4, column=1)
 
		# 定义右上方区域
		self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))
 
		self.tree.bind('<Button-1>', self.click)  # 左键获取位置
		self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建商品信息', width=20, command=self.new_row)
		self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中商品信息', width=20,command=self.updata_row)
		self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中商品信息', width=20,command=self.del_row)

		# 定义下方区域
		self.chaxun = StringVar()
		self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
		self.right_bottom_button = ttk.Button(self.frame_bottom, text='买家姓名查询', width=20, command=self.put_data)
		self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
		self.right_bottom_gender_entry.grid(row=0, column=1)
 
		# 位置设置
		self.right_top_title.grid(row=1, column=0, pady=10)
		self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
		self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
		self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
 
		# 整体区域定位
		self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
		self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
		self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
		self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		self.frame_left_top.grid_propagate(0)
		self.frame_right_top.grid_propagate(0)
		self.frame_center.grid_propagate(0)
		self.frame_bottom.grid_propagate(0)
 
		self.frame_left_top.tkraise() # 开始显示主菜单
		self.frame_right_top.tkraise() # 开始显示主菜单
		self.frame_center.tkraise() # 开始显示主菜单
		self.frame_bottom.tkraise() # 开始显示主菜单
 
		self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
		self.window.mainloop()  # 进入消息循环

	# 将查到的信息放到中间的表格中
	def put_data(self):
		self.delButton()	# 先将表格内的内容全部清空

		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "SELECT * FROM t_buyer where NAME = '%s'"  % (self.chaxun.get())
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()

			# 再次进行初始化，进行首行数据的插入
			self.id = []
			self.name = []
			self.gender = []
			self.age = []
			# 向表格中插入数据
			for row in results:
				self.id.append(row[0])
				self.name.append(row[1])
				self.gender.append(row[2])
				self.age.append(row[3])

		except:
			print("Error: unable to fetch data")
			messagebox.showinfo('警告！', '数据库连接失败！')
			db.close()# 关闭数据库连接
		
		print("进行数据的插入")
		for i in range(min(len(self.id), len(self.name), len(self.gender), len(self.age))):  # 写入数据
			self.tree.insert('', i, values=(self.id[i], self.name[i], self.gender[i], self.age[i]))
 
		for col in self.columns:  # 绑定函数，使表头可排序
			self.tree.heading(col, text=col,
							  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))


	# 清空表格中的所有信息
	def delButton(self):
		x=self.tree.get_children()
		for item in x:
			self.tree.delete(item)



	def back(self):
		All_admin(self.window)   # 进入管理员子菜单操作界面 
 
	def click(self, event):
		self.col = self.tree.identify_column(event.x)  # 列
		self.row = self.tree.identify_row(event.y)  # 行
 
		print(self.col)
		print(self.row)
		self.row_info = self.tree.item(self.row, "values")
		self.var_id.set(self.row_info[0])
		self.id1 = self.var_id.get()
		print(self.id1)
		self.var_name.set(self.row_info[1])
		self.var_gender.set(self.row_info[2])
		self.var_age.set(self.row_info[3])
		self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id, font=('Verdana', 15))
 
	# 排序的方法
	def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
		l = [(tv.set(k, col), k) for k in tv.get_children('')]
		l.sort(reverse=reverse)  # 排序方式
		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l):  # 根据排序后索引移动
			tv.move(k, '', index)
		tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

	# 插入方法
	def new_row(self):
		if str(self.var_id.get()) in self.id:
			messagebox.showinfo('警告！', '该商品已存在！')
		else:
			if self.var_id.get() != '' and self.var_name.get() != '' and self.var_gender.get() != '' and self.var_age.get() != '':
				# 打开数据库连接
				db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
				cursor = db.cursor()  # 使用cursor()方法获取操作游标
				sql = "INSERT INTO t_buyer(SNO, NAME, NUMBER, dizhi) \
				       VALUES ('%s', '%s', '%s', '%s')" % \
					  (self.var_id.get(), self.var_name.get(), self.var_gender.get(), self.var_age.get())  # SQL 插入语句
				try:
					cursor.execute(sql)  # 执行sql语句
					db.commit()  # 提交到数据库执行
				except:
					db.rollback()  # 发生错误时回滚
					messagebox.showinfo('警告！', '数据库连接失败！')
				db.close()  # 关闭数据库连接
 
				# 将信息写入到表格中
				self.id.append(self.var_id.get())
				self.name.append(self.var_name.get())
				self.gender.append(self.var_gender.get())
				self.age.append(self.var_age.get())
				self.tree.insert('', len(self.id) - 1, values=(self.id[len(self.id) - 1], self.name[len(self.id) - 1], self.gender[len(self.id) - 1], self.age[len(self.id) - 1]))
				self.tree.update()
				messagebox.showinfo('提示！', '插入成功！')
			else:
				messagebox.showinfo('警告！', '请填写商品信息')
 
	# 更新数据及表格
	def updata_row(self):
		res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
		if res == True:
			# 打开数据库连接
			db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
			cursor = db.cursor()  # 使用cursor()方法获取操作游标
			sql = "UPDATE t_buyer SET SNO = '%s', NAME = '%s', NUMBER = '%s', dizhi = '%s' \
				where SNO = '%s'" % (self.var_id.get(), self.var_name.get(), self.var_gender.get(), self.var_age.get(), self.id1)  # SQL 插入语句
			try:
				cursor.execute(sql)  # 执行sql语句
				db.commit()  # 提交到数据库执行
				messagebox.showinfo('提示！', '更新成功！')
			except:
				db.rollback()  # 发生错误时回滚
				messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
			db.close()  # 关闭数据库连接

			id_index = self.id.index(self.row_info[0])
			self.name[id_index] = self.var_name.get()
			self.gender[id_index] = self.var_gender.get()
			self.age[id_index] = self.var_age.get()

			self.tree.item(self.tree.selection()[0], values=(
				self.var_id.get(), self.var_name.get(), self.var_gender.get(),
				self.var_age.get()))  # 修改对于行信息

	# 删除行
	def del_row(self):
		res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
		if res == True:
			print(self.row_info[0])  # 鼠标选中的学号
			print(self.tree.selection()[0])  # 行号
			print(self.tree.get_children())  # 所有行
			# 打开数据库连接
			db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') 
			cursor = db.cursor()  # 使用cursor()方法获取操作游标
			sql = "DELETE FROM t_buyer WHERE SNO = '%s'" % (self.row_info[0]) # SQL 插入语句
			try:
				cursor.execute(sql)  # 执行sql语句
				db.commit()  # 提交到数据库执行
				messagebox.showinfo('提示！', '删除成功！')
			except:
				db.rollback()  # 发生错误时回滚
				messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
			db.close()  # 关闭数据库连接
 
			id_index = self.id.index(self.row_info[0])
			print(id_index)
			del self.id[id_index]
			del self.name[id_index]
			del self.gender[id_index]
			del self.age[id_index]
			print(self.id)
			self.tree.delete(self.tree.selection()[0])  # 删除所选行
			print(self.tree.get_children())


# 订单信息操作界面
class Buy_AdminManage:
	def __init__(self, parent_window):
		parent_window.destroy() # 销毁主界面

		self.window = Tk()  # 初始框的声明
		self.window.geometry("650x720+300+30")	# 初始窗口在屏幕中的位置
		self.window.title('管理员操作界面')
 
		self.frame_left_top = tk.Frame(width=300, height=230)
		self.frame_right_top = tk.Frame(width=200, height=230)
		self.frame_center = tk.Frame(width=500, height=360)
		self.frame_bottom = tk.Frame(width=650, height=60)
 
		self.id1 = 0

		# 定义下方中心列表区域
		self.columns = ("商品id", "订单id", "订单创建时间", "是否成功交易", "交易金额")
		self.tree = ttk.Treeview(self.frame_center, show="headings", height=18, columns=self.columns)
		self.vbar = ttk.Scrollbar(self.frame_center, orient=VERTICAL, command=self.tree.yview)
		# 定义树形结构与滚动条
		self.tree.configure(yscrollcommand=self.vbar.set)
 
		# 表格的标题
		self.tree.column("商品id", width=100, anchor='center')  # 表示列,不显示
		self.tree.column("订单id", width=100, anchor='center')
		self.tree.column("订单创建时间", width=100, anchor='center')
		self.tree.column("是否成功交易", width=100, anchor='center')
		self.tree.column("交易金额", width=100, anchor='center')	
 
		# 调用方法获取表格内容插入
		self.tree.grid(row=0, column=0, sticky=NSEW)
		self.vbar.grid(row=0, column=1, sticky=NS)
 
		self.SNO = []
		self.SNAME = []
		self.SSEX = []
		self.AGE = []
		self.DEP = []
		# 打开数据库连接
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "SELECT * FROM t_order"  # SQL 查询语句
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()
			for row in results:
				self.SNO.append(row[0])
				self.SNAME.append(row[1])
				self.SSEX.append(row[2])
				self.AGE.append(row[3])
				self.DEP.append(row[4])			
		except:
			print("Error: unable to fetch data")
			messagebox.showinfo('警告！', '数据库连接失败！')
		db.close()# 关闭数据库连接
 
 
		print("test***********************")
		for i in range(min(len(self.SNO), len(self.SNAME), len(self.SSEX), len(self.AGE), len(self.DEP))):  # 写入数据
			self.tree.insert('', i, values=(self.SNO[i], self.SNAME[i], self.SSEX[i], self.AGE[i], self.DEP[i]))
 
		for col in self.columns:  # 绑定函数，使表头可排序
			self.tree.heading(col, text=col,
							  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))
 
		# 定义顶部区域
		# 定义左上方区域
		self.top_title = Label(self.frame_left_top, text="订单信息:", font=('Verdana', 20))
		self.top_title.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=50, pady=10)
 
		self.left_top_frame = tk.Frame(self.frame_left_top)
		self.var_id = StringVar()  # 声明商品id
		self.var_name = StringVar()  # 声明订单id
		self.var_gender = StringVar()  # 声明订单创建时间
		self.var_age = StringVar()  # 声明订单是否成功交易
		self.var_dep = StringVar()	# 声明交易金额
		

		self.right_top_id_label = Label(self.frame_left_top, text="商品id： ", font=('Verdana', 15))
		self.right_top_id_entry = Entry(self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
		self.right_top_id_label.grid(row=1, column=0)  # 位置设置
		self.right_top_id_entry.grid(row=1, column=1)

		self.right_top_name_label = Label(self.frame_left_top, text="订单id：", font=('Verdana', 15))
		self.right_top_name_entry = Entry(self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
		self.right_top_name_label.grid(row=2, column=0)  # 位置设置
		self.right_top_name_entry.grid(row=2, column=1)

		self.right_top_gender_label = Label(self.frame_left_top, text="创建时间：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_gender,font=('Verdana', 15))
		self.right_top_gender_label.grid(row=3, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=3, column=1)

		self.right_top_gender_label = Label(self.frame_left_top, text="是否成功交易：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_age,font=('Verdana', 15))
		self.right_top_gender_label.grid(row=4, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=4, column=1)

		self.right_top_gender_label = Label(self.frame_left_top, text="交易金额：", font=('Verdana', 15))
		self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_dep, font=('Verdana', 15))
		self.right_top_gender_label.grid(row=5, column=0)  # 位置设置
		self.right_top_gender_entry.grid(row=5, column=1)
 
		# 定义右上方区域
		self.right_top_title = Label(self.frame_right_top, text="操作：", font=('Verdana', 20))
 
		self.tree.bind('<Button-1>', self.click)  # 左键获取位置
		self.right_top_button1 = ttk.Button(self.frame_right_top, text='新建订单信息', width=20, command=self.new_row)
		self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中订单信息', width=20,command=self.updata_row)
		self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中订单信息', width=20,command=self.del_row)

		# 定义下方区域
		self.chaxun = StringVar()
		self.right_bottom_gender_entry = Entry(self.frame_bottom, textvariable=self.chaxun, font=('Verdana', 15))
		self.right_bottom_button = ttk.Button(self.frame_bottom, text='订单id查询', width=20, command=self.put_data)
		self.right_bottom_button.grid(row=0, column=0, padx=20, pady=20)  # 位置设置
		self.right_bottom_gender_entry.grid(row=0, column=1)
 
		# 位置设置
		self.right_top_title.grid(row=1, column=0, pady=10)
		self.right_top_button1.grid(row=2, column=0, padx=20, pady=10)
		self.right_top_button2.grid(row=3, column=0, padx=20, pady=10)
		self.right_top_button3.grid(row=4, column=0, padx=20, pady=10)
 
		# 整体区域定位
		self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
		self.frame_right_top.grid(row=0, column=1, padx=30, pady=30)
		self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
		self.frame_bottom.grid(row=2, column=0, columnspan=2)
 
		self.frame_left_top.grid_propagate(0)
		self.frame_right_top.grid_propagate(0)
		self.frame_center.grid_propagate(0)
		self.frame_bottom.grid_propagate(0)
 
		self.frame_left_top.tkraise() # 开始显示主菜单
		self.frame_right_top.tkraise() # 开始显示主菜单
		self.frame_center.tkraise() # 开始显示主菜单
		self.frame_bottom.tkraise() # 开始显示主菜单

		self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
		self.window.mainloop()  # 进入消息循环

	def back(self):
		All_admin(self.window)   # 进入管理员子菜单操作界面 

	# 将查到的信息放到中间的表格中
	def put_data(self):
		self.delButton()	# 先将表格内的内容全部清空

		# print(self.chaxun.get())	# 输入框内的内容	
		# 打开数据库连接，准备查找指定的信息
		db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
		cursor = db.cursor()  # 使用cursor()方法获取操作游标
		sql = "SELECT * FROM t_order where SNO = '%s'"  % (self.chaxun.get())
		try:
			# 执行SQL语句
			cursor.execute(sql)
			# 获取所有记录列表
			results = cursor.fetchall()

			# 再次进行初始化，进行首行数据的插入
			self.SNO = []
			self.SNAME = []
			self.SSEX = []
			self.AGE = []
			self.DEP = []
			# 向表格中插入数据
			for row in results:
				self.SNO.append(row[0])
				self.SNAME.append(row[1])
				self.SSEX.append(row[2])
				self.AGE.append(row[3])
				self.DEP.append(row[4])		

		except:
			print("Error: unable to fetch data")
			messagebox.showinfo('警告！', '数据库连接失败！')
			db.close()# 关闭数据库连接
		
		for i in range(min(len(self.SNO), len(self.SNAME), len(self.SSEX), len(self.AGE), len(self.DEP))):  # 写入数据
			self.tree.insert('', i, values=(self.SNO[i], self.SNAME[i], self.SSEX[i], self.AGE[i], self.DEP[i]))
 
		for col in self.columns:  # 绑定函数，使表头可排序
			self.tree.heading(col, text=col,
							  command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))


	# 清空表格中的所有信息
	def delButton(self):
		x=self.tree.get_children()
		for item in x:
			self.tree.delete(item)



	def click(self, event):
		self.col = self.tree.identify_column(event.x)  # 列
		self.row = self.tree.identify_row(event.y)  # 行
 
		print(self.col)
		print(self.row)
		self.row_info = self.tree.item(self.row, "values")
		self.var_id.set(self.row_info[0])
		self.id1 = self.var_id.get()
		print(self.id1)
		self.var_name.set(self.row_info[1])
		self.var_gender.set(self.row_info[2])
		self.var_age.set(self.row_info[3])
		self.var_dep.set(self.row_info[4])
		self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
										font=('Verdana', 15))
 
		print('')
 
	def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
		l = [(tv.set(k, col), k) for k in tv.get_children('')]
		l.sort(reverse=reverse)  # 排序方式
		# rearrange items in sorted positions
		for index, (val, k) in enumerate(l):  # 根据排序后索引移动
			tv.move(k, '', index)
		tv.heading(col, command=lambda: self.tree_sort_column(tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题
 
	def new_row(self):
		print(self.var_id.get())
		print(self.SNO)
		if str(self.var_id.get()) in self.SNO:
			messagebox.showinfo('警告！', '该商品已存在！')
		else:
			if self.var_id.get() != '' and self.var_name.get() != '' and self.var_gender.get() != '' and self.var_age.get() != '' and self.var_dep.get() != '':
				# 打开数据库连接
				db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
				cursor = db.cursor()  # 使用cursor()方法获取操作游标
				sql = "INSERT INTO t_order(id, SNO, buy_time, vic, buy_money) \
				       VALUES ('%s', '%s', '%s', '%s', '%s')" % \
					  (self.var_id.get(), self.var_name.get(), self.var_gender.get(), self.var_age.get(), self.var_dep.get())  # SQL 插入语句
				try:
					cursor.execute(sql)  # 执行sql语句
					db.commit()  # 提交到数据库执行
				except:
					db.rollback()  # 发生错误时回滚
					messagebox.showinfo('警告！', '数据库连接失败！')
				db.close()  # 关闭数据库连接
 
				self.SNO.append(self.var_id.get())
				self.SNAME.append(self.var_name.get())
				self.SSEX.append(self.var_gender.get())
				self.AGE.append(self.var_age.get())
				self.DEP.append(self.var_dep.get())
				self.tree.insert('', len(self.SNO) - 1, values=(
				self.SNO[len(self.SNO) - 1], self.SNAME[len(self.SNO) - 1], self.SSEX[len(self.SNO) - 1],
				self.AGE[len(self.SNO) - 1], self.DEP[len(self.SNO) - 1]))
				self.tree.update()
				messagebox.showinfo('提示！', '插入成功！')
			else:
				messagebox.showinfo('警告！', '请填写订单信息')
 
	def updata_row(self):
		res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
		if res == True:
			# 打开数据库连接
			db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS')
			cursor = db.cursor()  # 使用cursor()方法获取操作游标
			sql = "UPDATE t_order SET id = '%s', SNO = '%s', buy_time = '%s', vic = '%s', buy_money = '%s' \
				where id = '%s'" % (self.var_id.get(), self.var_name.get(), self.var_gender.get(), self.var_age.get(), self.var_dep.get(), self.id1)  # SQL 插入语句
			try:
				cursor.execute(sql)  # 执行sql语句
				db.commit()  # 提交到数据库执行
				messagebox.showinfo('提示！', '更新成功！')
			except:
				db.rollback()  # 发生错误时回滚
				messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
			db.close()  # 关闭数据库连接

			id_index = self.SNO.index(self.row_info[0])
			self.SNO[id_index] = self.var_name.get()
			self.SSEX[id_index] = self.var_gender.get()
			self.AGE[id_index] = self.var_age.get()
			self.DEP[id_index] = self.var_age.get()

			self.tree.item(self.tree.selection()[0], values=(
				self.var_id.get(), self.var_name.get(), self.var_gender.get(),
				self.var_age.get(), self.var_dep.get()))  # 修改对于行信息

	# 删除行
	def del_row(self):
		res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
		if res == True:
			print(self.row_info[0])  # 鼠标选中的学号
			print(self.tree.selection()[0])  # 行号
			print(self.tree.get_children())  # 所有行
			# 打开数据库连接
			db = pymssql.connect('TAF_MT', 'sa', '123456789', 'EMIS') 
			cursor = db.cursor()  # 使用cursor()方法获取操作游标
			sql = "DELETE FROM t_order WHERE id = '%s'" % (self.row_info[0]) # SQL 插入语句
			try:
				cursor.execute(sql)  # 执行sql语句
				db.commit()  # 提交到数据库执行
				messagebox.showinfo('提示！', '删除成功！')
			except:
				db.rollback()  # 发生错误时回滚
				messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
			db.close()  # 关闭数据库连接
 
			id_index = self.SNO.index(self.row_info[0])
			print(id_index)
			del self.SNO[id_index]
			del self.SNAME[id_index]
			del self.SSEX[id_index]
			del self.AGE[id_index]
			del self.DEP[id_index]
			print(self.SNO)
			self.tree.delete(self.tree.selection()[0])  # 删除所选行
			print(self.tree.get_children())


# About页面
class AboutPage:
	def __init__(self, parent_window):
		parent_window.destroy() # 销毁主界面
 
		self.window = tk.Tk()  # 初始框的声明
		self.window.title('关于')
		self.window.geometry('300x450')  # 这里的乘是小x
 
		label = tk.Label(self.window, text='商品信息管理系统', bg='green', font=('Verdana', 20), width=30, height=2)
		label.pack()
 
		Label(self.window, text='作者：TAF_MT', font=('Verdana', 18)).pack(pady=30)
		Label(self.window, text='联系：**********', font=('Verdana', 18)).pack(pady=5)
 
		Button(self.window, text="返回首页", width=8, font=tkFont.Font(size=12), command=self.back).pack(pady=100)
 
		self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
		self.window.mainloop()  # 进入消息循环
 
	def back(self):
		StartPage(self.window)  # 显示主窗口 销毁本窗口
 
 
if __name__ == '__main__':
	# 实例化Application
	window = tk.Tk()
	StartPage(window)