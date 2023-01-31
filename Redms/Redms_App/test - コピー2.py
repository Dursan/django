from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkcalendar import Calendar, DateEntry
import codecs
import tkinter.messagebox as s_msg
import tkinter.font as f
import csv
import os
import math
import pathlib
import ntpath
import random, string
import datetime
import pandas as pd

#事前設定変数
mng={"dx7621is":"杉山", "dx7621af":"福澤", "dx7621ra":"新井","dx7621ts":"斉藤","dx7621ky":"屋敷","dx7621yf":"伏見"}
#関数


#検収
class RentChk:
  
  ##検収データ表示
  def chk_data_display(self):
    ##データをID降順に並べ替える
    self.data = pd.read_csv('../data/rent_list.csv', sep=',',encoding='utf-8', quotechar='"', lineterminator='\r',header=0)
    self.data.sort_values(by = 'rent_id', ascending = False, inplace = True)
    self.data_col_num=0
    for index, row in self.data.iterrows():
      if row['rent_return_check']==1:
        self.data_col_num+=1


    if self.data_col_num>1:
      for index, row in self.data.iterrows():
        if row['rent_return_check']==1:

          self.chk_frame = tk.Frame(self.chk_state_wrapper,width=self.chk_state_wrapper.winfo_width())
          self.chk_frame.pack(side = tk.TOP,fill = tk.X,expand=1)

          btn_id = tk.StringVar(value="検収",name=str(row['rent_id']))
          self.chk_rbtn = tk.Button(self.chk_frame, textvariable=btn_id, text=row['rent_id'],font=("",12,'bold'),width=10)
          self.chk_rbtn.pack(side = tk.RIGHT,fill = tk.X,padx=(40,20))
          self.chk_rbtn.bind("<ButtonPress>", self.button_return_check)
          
          self.chk_frame_u = tk.Frame(self.chk_frame,width=self.chk_state_wrapper.winfo_width())
          self.chk_frame_u.pack(side = tk.TOP,fill = tk.X,expand=1,pady=(10,10))

          self.chk_frame_l = tk.Frame(self.chk_frame,width=self.chk_state_wrapper.winfo_width())
          self.chk_frame_l.pack(side = tk.TOP,fill = tk.X,pady=(0,10),expand=1)

          self.chk_frame_o = tk.Frame(self.chk_frame,width=self.chk_state_wrapper.winfo_width())
          self.chk_frame_o.pack(side = tk.TOP,fill = tk.X,pady=(0,10),expand=1)

          self.chk_eqp_t = tk.Label(self.chk_frame_u, text="品目",font=("",16))
          self.chk_eqp_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

          self.chk_eqp_d = tk.Label(self.chk_frame_u, text=row['rent_equipment'] ,font=("",16,'bold'))
          self.chk_eqp_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(20,0))

          self.chk_name_t = tk.Label(self.chk_frame_l, text="名前",font=("",12,'bold'))
          self.chk_name_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

          self.chk_name_d = tk.Label(self.chk_frame_l, text=str(row['rent_name']) ,font=("",12))
          self.chk_name_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

          self.chk_time_t = tk.Label(self.chk_frame_l, text="日付",font=("",12,'bold'))
          self.chk_time_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

          self.chk_time_d = tk.Label(self.chk_frame_l, text=row['rent_time'],font=("",12))
          self.chk_time_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

          self.chk_prt_t = tk.Label(self.chk_frame_l, text="返却日",font=("",12,'bold'))
          self.chk_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

          self.chk_prt_d = tk.Label(self.chk_frame_l, text=row['rent_pre_return_time'] ,font=("",12,'bold'))
          self.chk_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

          if pd.isnull(row['rent_other']):
            self.chk_prt_t = tk.Label(self.chk_frame_o, text="その他",font=("",11,'bold'))
            self.chk_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

            self.chk_prt_d = tk.Label(self.chk_frame_o, text='ありません' ,font=("",11))
            self.chk_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

          else:

            self.chk_prt_t = tk.Label(self.chk_frame_o, text="その他",font=("",11,'bold'))
            self.chk_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

            self.chk_prt_d = tk.Label(self.chk_frame_o, text=row['rent_other'] ,font=("",11))
            self.chk_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

          separator_chk = ttk.Separator(self.chk_state_wrapper, orient="horizontal")
          separator_chk.pack(side = tk.TOP, fill = tk.X,padx=10,expand=1)
        else:
          continue
    else:

      self.chk_name = tk.Frame(self.chk_state_wrapper)
      self.chk_name.pack(side = tk.TOP,fill = tk.X,expand=1)

      self.chk_empty_t = tk.Label(self.chk_name, text="現在、貸出中のデータはありません",font=("",16))
      self.chk_empty_t.pack(side = tk.TOP,fill = tk.X,anchor=tk.W,padx=(30,0),pady=20,expand=1)
  
  def button_rent_confirm_in(self):
    rent_entry=rent_confirming_entry.get()
    cnt=1
    for i in mng.items():
      if i[0]== rent_entry:
        self.chk_name=i[1]
        rent_confirming.delete(0, tk.END)
        self.button_rent_confirm_op()
        break
      elif cnt<len(mng):
        cnt+=1
        continue
      else:
        rent_confirming.delete(0, tk.END)
        v2="入力情報が見当たりません"
        s_msg.showinfo(title="結果:", message=v2)

  #検収ウインドウ開く
  def button_rent_confirm_op(self):
    sub_win01 = tk.Toplevel()
    self._sub_win01 = sub_win01
    sub_win01.title('検収ウインドウ')
    sub_win01.minsize(width=760, height=360)
    sub_win01.columnconfigure(0, weight=1)
    sub_win01.rowconfigure(0, weight=1)

    frame_wrapper_sub = tk.Frame(sub_win01)
    frame_wrapper_sub.pack(fill = tk.BOTH,padx=10,pady=15)

    ##検収ウインドウタイトル
    return_check_f01 = tk.Frame(frame_wrapper_sub)
    return_check_f01.pack(fill = tk.X,side = tk.TOP)
    return_check_f02 = tk.Frame(frame_wrapper_sub)
    return_check_f02.pack(fill = tk.X,side = tk.TOP)

    return_check_title01 = tk.Label(return_check_f01, text='返却状況  検収者：',font=("",16,"bold"))
    return_check_title01.pack(side = tk.LEFT,fill = tk.X)
    return_check_title02 = tk.Label(return_check_f01, text=self.chk_name,font=("",16,"bold"))
    return_check_title02.pack(side = tk.LEFT,fill = tk.X)
    separator_chk = ttk.Separator(frame_wrapper_sub, orient="horizontal")
    separator_chk.pack(side = tk.TOP, fill = tk.X,padx=10)

    ##貸出状況大枠
    self.chk_state_canvas = tk.Canvas(frame_wrapper_sub,height=360,highlightthickness=0)

    df = pd.read_csv('../data/rent_list.csv')
    self.chk_data_num=0
    for index, row in df.iterrows():
      if row['rent_return_check']==1:
        self.chk_data_num +=1 
    self.cs_height=(120*self.chk_data_num)

    y_s_bar = tk.Scrollbar(frame_wrapper_sub, orient=tk.VERTICAL)
    y_s_bar.pack(side=tk.RIGHT, fill=tk.Y)
    y_s_bar.config(command=self.chk_state_canvas.yview)
    self.chk_state_canvas.config(scrollregion=(0,0,self.chk_state_canvas.winfo_width(),self.cs_height))
    self.chk_state_canvas.config(yscrollcommand=y_s_bar.set)
    self.chk_state_canvas.pack(fill=tk.BOTH,expand=1,padx=(20,10))

    self.chk_state_wrapper = tk.Frame(self.chk_state_canvas)
    self.chk_state_wrapper.pack(side = tk.TOP,fill = tk.X,expand=1)
    self.chk_state_canvas.create_window((0,0), window=self.chk_state_wrapper, anchor=tk.NW)

    self.chk_data_display()
    
    ##検収画面終了ボタン
    separator_chk = ttk.Separator(sub_win01, orient="horizontal")
    separator_chk.pack(side = tk.TOP, fill = tk.X,padx=10)
    self.chk_closing_f = tk.Frame(sub_win01)
    self.chk_closing_f.pack(fill = tk.X,side = tk.TOP,padx=10,pady=(10,20))

    self.chk_closing_btn = tk.Button(self.chk_closing_f, text='閉じる', width=10,font=("",10,'bold'),bg='#ccc',command=self.button_return_check_close)
    #self.chk_closing_btn.bind()
    self.chk_closing_btn.pack(side = tk.RIGHT)
    
  #検収動作
  def button_return_check(self,event):
    print(str(event.widget.cget("textvariable")).replace('\n',''))
    ###変更する行データ抽出
    rent_id=int(event.widget.cget("textvariable").replace('\n','').replace('\"',''))
    list=[]
    df00=pd.read_csv("../data/rent_list.csv")
    for i, row in df00.iterrows():
      if row[0]==int(rent_id):
        for j in row:
          list.append(j)

    ###抽出行データ変更
    list[8]=self.chk_name
    list[9]=2
    new_data=[]
    writing_data=[]
    file_r = open("../data/rent_list.csv", mode="r", newline="",encoding='utf-8')
    reader = csv.reader(file_r,delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    for data in reader:
      if data[0]==str(list[0]):
        for i,dt in enumerate(data):
          dt=list[i]
          if isinstance(list[i], int):
            list[i]=str(list[i])
            new_data.append(list[i])
          elif pd.isnull(list[i]):
            new_data.append('')
          else:
            new_data.append(list[i])
        writing_data.append(new_data)
      else:
        writing_data.append(data)
    file_r.close()
    with open("../data/rent_list.csv", mode="w", newline="",encoding='utf-8') as file_w:
      writer = csv.writer(file_w,quoting=csv.QUOTE_NONNUMERIC)
      writer.writerows(writing_data)
      file_w.close()  
   
  ###貸出データ再表示
    children = self.chk_state_wrapper.winfo_children()
    for child in children:
      child.destroy()

    self.chk_data_display() 

  #検収画面閉じる
  def button_return_check_close(self):
    root0.update_idletasks()
    self._sub_win01.destroy()
 
#メインウインドウ開く
root0 = Tk()
root0.title('DX推進部 備品貸出')
root0.minsize(width=760, height=480)
root0.configure(bg='#ccc')
root0.columnconfigure(0, weight=1)
root0.rowconfigure(0, weight=1)

root0.update_idletasks()

##検収画面移行キー入力
rent_confirming_f = tk.Frame(root0,bg='#ccc')
rent_confirming_f.pack(fill = tk.X,side = tk.TOP,padx=10,pady=(10,20))

rent_confirming_btn = tk.Button(rent_confirming_f, text='検収', width=10,font=("",10,'bold'),command=RentChk().button_rent_confirm_in)
rent_confirming_btn.pack(side = tk.RIGHT) 

rent_confirming_entry = tk.StringVar()
rent_confirming = tk.Entry(rent_confirming_f,textvariable=rent_confirming_entry,width=15,font=("", 10), show="*")
rent_confirming.pack(fill = tk.X,side = tk.RIGHT,padx=(0,15),ipadx=5,ipady=5)

        
#メインウインドウ締め
root0.mainloop()
