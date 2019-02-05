class Add_View(Toplevel):

    def __init__(self,master,sqlite_table,gui_table):
        self.window_height = 0
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Toplevel.__init__(self,master=master)
        for index,description in enumerate(self.gui_tables.columns):
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
                    def cal_button()
            else:   #handle type case
                continue
