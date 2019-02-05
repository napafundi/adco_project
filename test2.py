class Add_View(Toplevel):

    def __init__(self,master,sqlite_table,gui_table):
        self.window_height = 0
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Toplevel.__init__(self,master=master)
        for index,description in enumerate(self.gui_table.columns):
            if (description.lower() != 'type'):
                Label(self,text=description).grid(row=index,column=0)
                if decription.lower() == 'total':
                    self.total_text = StringVar()
                    self.total_entry = Entry(self,textvariable=self.total_entry)
                    self.total_entry.config(state="readonly")
                    self.total_entry.grid(row=index,column=1)
                elif (description.lower().find('age') != -1):
                    self.age_text = StringVar()
                    self.age_entry = Entry(self, textvariable=self.age_text)
                    self.age_entry.config(state="readonly")
                    self.age_entry.grid(row=index,column=1)
                else:
                    Entry(self).grid(row=index,column=1)
                self.window_height += 35
                if (description.lower().find('date') != -1):
                    self.date_index = index
                    self.date_entry = self.grid_slaves(row=self.date_index,column=1)[0]
                    self.date_entry.config(state="readonly")
                    def cal_button():
                        self.top = Toplevel(window)
                        self.cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                                       cursor="hand2")
                        self.cal.pack(fill="both", expand=True)
                        def retrieve_date():
                            self.date_entry.config(state=NORMAL)
                            self.date_entry.delete(0,END)
                            self.date_entry.insert(END,self.cal.selection_get().strftime("%Y-%m-%d"))
                            self.date_entry.config(state="readonly")
                            self.top.destroy()
                        Button(self.top, text="ok", command = retrieve_date).pack()
                        self.top.focus()
                    self.image = Image.open("calendar.png")
                    self.image.resize((22,22))
                    self.photo = ImageTk.PhotoImage(self.image)
                    self.cal_link = Button(self, image=self.photo, command = cal_button)
                    self.cal_link.image = self.photo
                    self.cal_link.grid(row=index,column=2)
                elif ((description.lower().find('total') != -1) or (description.lower().find('age') != -1)):
                    self.entries = [x for x in reversed(self.grid_slaves(column=0)) if (x.winfo_class() == 'Label' or x.winfo_class() == 'Menubutton')]
                    for entry in self.entries:
                        if entry.cget("text").lower() == "amount":
                            self.amount_row = entry.grid_info()['row']
                            self.amount_entry = self.grid_slaves(row=self.amount_row,column=1)[0]
                        if entry.cget("text").lower() == "price":
                            self.price_row = entry.grid_info()['row']
                            self.price_entry = self.grid_slaves(row=self.price_row,column=1)[0]
                        if entry.cget("text").find("date") != -1:
                            self.date_row = entry.grid_info()['row']
                            self.date_entry = self.grid_slaves(row=self.date_row,column=1)[0]
                    def total_after():
                        def total_update():
                            try:
                                self.price_num = self.price_entry.get()
                                self.amount_num = self.amount_entry.get()
                                self.total_string = "$%.2f" % (float(self.amount_num)*float(self.price_num))
                                self.total_text.set(self.total_string)
                                return
                            except:
                                self.total_string = "$"
                                self.total_text.set(self.total_string)
                            try:
                                self.date_value = datetime.strptime(self.date_entry.get(),'%Y-%m-%d')
                                self.date_diff = datetime.now() - self.date_value
                                self.barrel_age = "%d years, %d months" % (math.floor(self.date_diff.days/365.2425), (self.date_diff.days%365.2425)/30)
                                self.age_text.set(self.barrel_age)
                            except:
                                self.age_text.set("0 years, 0 months")
                        total_update()
                        self.after(150,total_after)
                    total_after()
            else:   #handle type case
                Label(self,text=description).grid(row=index,column=0)
                self.type_var = StringVar(master)
                self.type_var.set(type_options[sqlite_table][0])
                self.options = OptionMenu(self,self.type_var,*tuple(type_options[sqlite_table]))
                self.options.config(width=14, background="white")
                self.options.grid(row=index,column=1)
                self.window_height += 35
        self.grid_size = self.grid_size()[1]
        Button(self,text="Add Item").grid(row=self.grid_size+1,column=1,sticky=N+E+S+W)
        Button(self,text="Cancel").grid(row=self.grid_size+2,column=1,sticky=N+E+S+W)
        self.title("Add to" + self.sqlite_table.replace("_"," "))
        self.focus()
        self.x = (screen_width/2) - (500/2)
        self.y = (screen_height/2) - (500/2)
        self.geometry("%dx%d+%d+%d") % (300,window_height,self.x,self.y)
        self.resizable(0,0)
