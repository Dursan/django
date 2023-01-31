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
#import random, string
import datetime
import pandas as pd

#関数

##貸出内容個別表示関数
def rent_deail(data_col_num,data):
  if data_col_num>0:
    for index, row in data.iterrows():
      if row['rent_return_check']!=2 and pd.notnull(row['rent_return_check']):

            frame_name = tk.Frame(rent_state_wrapper,bg='#333',width=frame_wrapper_out.winfo_width())
            frame_name.pack(side = tk.TOP,fill = tk.X,expand=1)

            btn_id = tk.StringVar(value="返却",name=str(row['rent_id']))
            rent_rbtn = tk.Button(frame_name, textvariable=btn_id, text=row['rent_id'],font=("",12,'bold'),width=10)
            rent_rbtn.pack(side = tk.RIGHT,fill = tk.X,padx=(40,20))
            rent_rbtn.bind("<ButtonPress>", button_rent_return)


            frame_name_u = tk.Frame(frame_name,bg='#333',width=frame_wrapper_out.winfo_width())
            frame_name_u.pack(side = tk.TOP,fill = tk.X,pady=(10,10),expand=1)

            frame_name_l = tk.Frame(frame_name,bg='#333',width=frame_wrapper_out.winfo_width())
            frame_name_l.pack(side = tk.TOP,fill = tk.X,pady=(0,10),expand=1)

            frame_name_o = tk.Frame(frame_name,bg='#333',width=frame_wrapper_out.winfo_width())
            frame_name_o.pack(side = tk.TOP,fill = tk.X,pady=(0,10),expand=1)
              
            rent_eqp_t = tk.Label(frame_name_u, text="品目",font=("",16),fg='#fff',bg='#333')
            rent_eqp_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

            rent_eqp_d = tk.Label(frame_name_u, text=row['rent_equipment'] ,font=("",16,'bold'),fg='#fff',bg='#333')
            rent_eqp_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(20,0))

            rent_name_t = tk.Label(frame_name_l, text="名前",font=("",12,'bold'),fg='#fff',bg='#333')
            rent_name_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

            rent_name_d = tk.Label(frame_name_l, text=str(row['rent_name']) ,font=("",12),fg='#fff',bg='#333')
            rent_name_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

            rent_time_t = tk.Label(frame_name_l, text="日付",font=("",12,'bold'),fg='#fff',bg='#333')
            rent_time_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

            rent_time_d = tk.Label(frame_name_l, text=row['rent_time'],font=("",12),fg='#fff',bg='#333')
            rent_time_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

            if row['rent_return_check']==0:

              rent_prt_t = tk.Label(frame_name_l, text="返却予定日",font=("",12,'bold'),fg='#fff',bg='#333')
              rent_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

              rent_prt_d = tk.Label(frame_name_l, text=row['rent_pre_return_time'] ,font=("",12),fg='#fff',bg='#333')
              rent_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

            elif row['rent_return_check']==1:

              rent_prt_t = tk.Label(frame_name_l, text="返却日",font=("",12,'bold'),fg='#ffa500',bg='#333')
              rent_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

              rent_prt_d = tk.Label(frame_name_l, text=row['rent_pre_return_time'] ,font=("",12,'bold'),fg='#ffa500',bg='#333')
              rent_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

            else:
              separator_rent.pack_forget()
              frame_name.pack_forget()

            
            if pd.isnull(row['rent_other']):
              rent_prt_t = tk.Label(frame_name_o, text="その他",font=("",11,'bold'),fg='#fff',bg='#333')
              rent_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

              rent_prt_d = tk.Label(frame_name_o, text='ありません' ,font=("",11),fg='#fff',bg='#333')
              rent_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)
              
            else:
              
              rent_prt_t = tk.Label(frame_name_o, text="その他",font=("",11,'bold'),fg='#fff',bg='#333')
              rent_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))

              rent_prt_d = tk.Label(frame_name_o, text=row['rent_other'] ,font=("",11),fg='#fff',bg='#333')
              rent_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)
              
            separator_rent = ttk.Separator(rent_state_wrapper, orient="horizontal")
            separator_rent.pack(side = tk.TOP, fill = tk.X,padx=10,expand=1)

  else:

    frame_name = tk.Frame(rent_state_wrapper,bg='#333',width=frame_wrapper_out.winfo_width())
    frame_name.pack(side = tk.TOP,fill = tk.X)

    rent_empty_t = tk.Label(frame_name, text="現在、貸出中のデータはありません",font=("",16),fg='#fff',bg='#333')
    rent_empty_t.pack(side = tk.TOP,fill = tk.X,padx=(30,0),pady=20,expand=1)

##貸出状況表示関数(降順)
def rent_info_desc():
  ##データをID降順に並べ替える
  data = pd.read_csv('../data/rent_list.csv', sep=',',encoding='utf-8', quotechar='"', lineterminator='\r',header=0)
  data.sort_values(by = 'rent_id', ascending = False, inplace = True)
  data_col_num=0
  for index, row in data.iterrows():
    if row['rent_return_check']!=2 and pd.notnull(row['rent_return_check']):
      data_col_num+=1
  rent_deail(data_col_num,data)
  
##貸出状況表示関数(昇順)            
def rent_info_asc():
  ##データをID昇順に並べ替える
  data = pd.read_csv('../data/rent_list.csv', sep=',',encoding='utf-8', quotechar='"', lineterminator='\r',header=0)
  data.sort_values(by = 'rent_id', ascending=True, inplace = True)
  data_col_num=0
  for index, row in data.iterrows():
    if row['rent_return_check']!=2 and pd.notnull(row['rent_return_check']):
      data_col_num+=1
  rent_deail(data_col_num,data)

##データ並べ替え
def button_sort():
  children = rent_state_wrapper.winfo_children()
  for child in children:
    child.destroy()
  
  if rent_sort_state.cget("text")=='desc':
    rent_info_asc()
    rent_sort_state['text']='asc'
    rent_state_title02['text']='貸出が早い順'
  elif rent_sort_state.cget("text")=='asc':
    rent_info_desc()
    rent_sort_state['text']='desc'
    rent_state_title02['text']='貸出が遅い順'
  else:
    rent_info_desc()
    rent_sort_state['text']='desc'
    rent_state_title02['text']='貸出が遅い順'

##貸出項目保存
def button_rent_input():
###フォーム入力値取得
  rent_equipment=var_material_eqp.get()
  rent_pre_return_time=combo_return.get_date()
  rent_pre_return_time=str(rent_pre_return_time).replace('-','/')
  rent_dpt=var_material_dpt.get()
  rent_name=var_material_name.get()
  rent_other =rent_other_entry.get()

###フォーム入力以外の値取得
  rent_time= datetime.date.today()
  rent_time=str(rent_time).replace('-','/')
  #csv_header = ["rent_id","rent_dpt","rent_name","rent_equipment","rent_other","rent_time","rent_pre_return_time","rent_return_time","rent_return_check_name","rent_return_check"]
  df = pd.read_csv('../data/rent_list.csv')
  data_col_num=0
  for index, row in df.iterrows():
    if row['rent_return_check']!=2 and pd.notnull(row['rent_return_check']):
      data_col_num+=1
  
  if data_col_num>1:
    newest_id=int(df['rent_id']).max()
    rent_id = int(newest_id)+1
  else: 
    rent_id = 1

###仮の値設定 
  rent_return_time=None
  rent_return_check_name=None
  rent_return_check=0

###貸出データ書き込み
  with open("../data/rent_list.csv", mode="a", newline="",encoding='utf-8') as file:
    writer = csv.writer(file,quoting=csv.QUOTE_ALL)
    writer.writerow([rent_id,rent_dpt,rent_name,rent_equipment,rent_other,rent_time,rent_pre_return_time,rent_return_time,rent_return_check_name,rent_return_check])
    #writer.writerow(header)
    file.close()

###貸出データ再表示
  children = rent_state_wrapper.winfo_children()
  for child in children:
    child.destroy()

  rent_info_desc()
            
  
      
  '''
#確認用サブウインドウ
  
  sub_win01 = tk.Toplevel()
  sub_win01.title('保存データ確認')
  sub_win01.minsize(width=640, height=360)
  sub_win01.columnconfigure(0, weight=1)
  sub_win01.rowconfigure(0, weight=1)

  frame_wrapper_sub = tk.Frame(sub_win01)
  frame_wrapper_sub.pack(fill = tk.BOTH,pady=15)
  
  frame_wrapper_sub01 = tk.Frame(frame_wrapper_sub)
  frame_wrapper_sub01.pack(side = tk.TOP,fill = tk.X,pady=5)
  sub_eqp_t = tk.Label(frame_wrapper_sub01, text="品目",font=("",12))
  sub_eqp_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))       
  sub_eqp_d = tk.Label(frame_wrapper_sub01, text=rent_equipment,font=("",12,'bold'),fg='#fff',bg='#333')
  sub_eqp_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

  frame_wrapper_sub02 = tk.Frame(frame_wrapper_sub)
  frame_wrapper_sub02.pack(side = tk.TOP,fill = tk.X,pady=5)
  sub_name_t = tk.Label(frame_wrapper_sub02, text="部署",font=("",12,'bold'))
  sub_name_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))
  sub_name_d = tk.Label(frame_wrapper_sub02, text=rent_dpt ,font=("",12),fg='#fff',bg='#333')
  sub_name_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

  frame_wrapper_sub03 = tk.Frame(frame_wrapper_sub)
  frame_wrapper_sub03.pack(side = tk.TOP,fill = tk.X,pady=5)
  sub_name_t = tk.Label(frame_wrapper_sub03, text="名前",font=("",12,'bold'))
  sub_name_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))
  sub_name_d = tk.Label(frame_wrapper_sub03, text=rent_name ,font=("",12),fg='#fff',bg='#333')
  sub_name_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

  frame_wrapper_sub04 = tk.Frame(frame_wrapper_sub)
  frame_wrapper_sub04.pack(side = tk.TOP,fill = tk.X,pady=5)
  sub_time_t = tk.Label(frame_wrapper_sub04, text="日付",font=("",12,'bold'),fg='#fff',bg='#333')
  sub_time_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))
  sub_time_d = tk.Label(frame_wrapper_sub04, text=rent_time,font=("",12),fg='#fff',bg='#333')
  sub_time_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

  frame_wrapper_sub05 = tk.Frame(frame_wrapper_sub)
  frame_wrapper_sub05.pack(side = tk.TOP,fill = tk.X,pady=5)
  sub_prt_t = tk.Label(frame_wrapper_sub05, text="返却予定日",font=("",12,'bold'),fg='#fff',bg='#333')
  sub_prt_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))
  sub_prt_d = tk.Label(frame_wrapper_sub05, text=rent_pre_return_time ,font=("",12),fg='#fff',bg='#333')
  sub_prt_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)

  frame_wrapper_sub06 = tk.Frame(frame_wrapper_sub)
  frame_wrapper_sub06.pack(side = tk.TOP,fill = tk.X,pady=5)
  sub_hidden_id_t = tk.Label(frame_wrapper_sub06, text="案件ID",font=("",12,'bold'),fg='#fff',bg='#333')
  sub_hidden_id_t.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W,padx=(30,0))
  sub_hidden_id_d = tk.Label(frame_wrapper_sub06, text=rent_id,font=("",12),fg='#fff',bg='#333')
  sub_hidden_id_d.pack(side = tk.LEFT,fill = tk.X,anchor=tk.W)
'''

##返却時処理関数
def button_rent_return(event):
  #print(event.widget["textvariable"])
  rent_id00=str(event.widget["textvariable"])
  rent_id=int(rent_id00.replace('\n','').replace('\"',''))
  list=[]
  df00=pd.read_csv("../data/rent_list.csv")
  for i, row in df00.iterrows():
    if row[0]==int(rent_id):
        for j in row:
          list.append(j)
  rent_return_time0 = datetime.date.today()
  rent_return_time=str(rent_return_time0).replace('-','/')
  list[7]=rent_return_time
  list[9]=1
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
  children = rent_state_wrapper.winfo_children()
  for child in children:
    child.destroy()

  rent_info_desc()

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


    if self.data_col_num>0:
      for index, row in self.data.iterrows():
        if row['rent_return_check']==1:

          self.chk_frame = tk.Frame(self.chk_state_wrapper,width=self.chk_state_canvas.winfo_width())
          self.chk_frame.pack(side = tk.TOP,fill = tk.X,expand=1)
          
          btn_id = tk.StringVar(value="検収",name=str(row['rent_id']))
          self.chk_rbtn = tk.Button(self.chk_frame, textvariable=btn_id, text=row['rent_id'],font=("",12,'bold'),width=10)
          self.chk_rbtn.pack(side = tk.RIGHT,fill = tk.X,padx=(40,20))
          self.chk_rbtn.bind("<ButtonPress>", self.button_return_check)
          
          self.chk_frame_u = tk.Frame(self.chk_frame,width=self.chk_state_canvas.winfo_width())
          self.chk_frame_u.pack(side = tk.TOP,fill = tk.X,pady=(10,10),expand=1)

          self.chk_frame_l = tk.Frame(self.chk_frame,width=self.chk_state_canvas.winfo_width())
          self.chk_frame_l.pack(side = tk.TOP,fill = tk.X,pady=(0,10),expand=1)

          self.chk_frame_o = tk.Frame(self.chk_frame,width=self.chk_state_canvas.winfo_width())
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
    mng={"dx7621is":"杉山", "dx7621af":"福澤", "dx7621ra":"新井","dx7621ts":"斉藤","dx7621ky":"屋敷","dx7621yf":"伏見"}
    
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
    sub_win01.minsize(width=830, height=360)
    sub_win01.columnconfigure(0, weight=1)
    sub_win01.rowconfigure(0, weight=1)

    sub_win01.update_idletasks()

    self.frame_wrapper_sub = tk.Frame(sub_win01)
    self.frame_wrapper_sub.pack(fill = tk.BOTH,padx=10,pady=15)

    ##検収ウインドウタイトル
    self.return_check_f01 = tk.Frame(self.frame_wrapper_sub)
    self.return_check_f01.pack(fill = tk.X,side = tk.TOP)
    self.return_check_f02 = tk.Frame(self.frame_wrapper_sub)
    self.return_check_f02.pack(fill = tk.X,side = tk.TOP)

    self.return_check_title01 = tk.Label(self.return_check_f01, text='返却状況  検収者：',font=("",16,"bold"))
    self.return_check_title01.pack(side = tk.LEFT,fill = tk.X)
    self.return_check_title02 = tk.Label(self.return_check_f01, text=self.chk_name,font=("",16,"bold"))
    self.return_check_title02.pack(side = tk.LEFT,fill = tk.X)
    self.separator_chk = ttk.Separator(self.frame_wrapper_sub, orient="horizontal")
    self.separator_chk.pack(side = tk.TOP, fill = tk.X,padx=10)

    ##貸出状況大枠
    self.chk_state_canvas = tk.Canvas(self.frame_wrapper_sub,height=360,highlightthickness=0)

    df = pd.read_csv('../data/rent_list.csv')
    self.chk_data_num=0
    for index, row in df.iterrows():
      if row['rent_return_check']==1:
        self.chk_data_num +=1 
    self.cs_height=(120*self.chk_data_num)

    y_s_bar = tk.Scrollbar(self.frame_wrapper_sub, orient=tk.VERTICAL)
    y_s_bar.pack(side=tk.RIGHT, fill=tk.Y)
    y_s_bar.config(command=self.chk_state_canvas.yview)
    self.chk_state_canvas.config(scrollregion=(0,0,self.chk_state_canvas.winfo_width(),self.cs_height))
    self.chk_state_canvas.config(yscrollcommand=y_s_bar.set)
    self.chk_state_canvas.pack(fill=tk.BOTH,padx=(20,10))

    self.chk_state_wrapper = tk.Frame(self.chk_state_canvas,width=self.chk_state_canvas.winfo_width())
    self.chk_state_wrapper.pack(side = tk.TOP,fill = tk.X,pady=(0,10))
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
    ###変更する行データ抽出
    rent_id00=str(event.widget["textvariable"])
    rent_id=int(rent_id00.replace('\n','').replace('\"',''))
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
    children = rent_state_wrapper.winfo_children()
    for child in children:
      child.destroy()
    rent_sort_state['text']='desc'
    rent_state_title02['text']='貸出が遅い順'
    rent_info_desc()    
    self._sub_win01.destroy()


#メインウインドウ開く
root0 = Tk()
root0.title('DX推進部 備品貸出')
root0.minsize(width=860, height=480)
root0.configure(bg='#ccc')
root0.columnconfigure(0, weight=1)
root0.rowconfigure(0, weight=1)

root0.update_idletasks()

##借出入力フレーム
frame_wrapper_in = tk.Frame(root0,bg='#ccc')
frame_wrapper_in.pack(side=tk.TOP,fill = tk.BOTH,padx=20,pady=10)


##借出入力タイトル
rent_state_title_f = tk.Frame(frame_wrapper_in,bg='#ccc')
rent_state_title_f.pack(fill = tk.X,side = tk.TOP,pady=(10,15))

rent_state_title01 = tk.Label(rent_state_title_f, text='貸出入力：',font=("",16,"bold"),bg='#ccc')
rent_state_title01.pack(side = tk.LEFT,fill = tk.X)


##品名・日付
frame_eqp_day = tk.Frame(frame_wrapper_in,bg='#ccc')
frame_eqp_day.pack(fill = tk.X,side = tk.TOP,pady=(0,20))

rent_equipment_l = tk.Label(frame_eqp_day, text=' 品目 ：',font=("",12,"bold"),bg='#ccc')
rent_equipment_l.pack(side = tk.LEFT,fill = tk.X)


###品名
eqp_list=[]
file01=open('../data/rent_equipment.csv','r',encoding='utf-8')
cont01_data=csv.DictReader(file01, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
for c01 in cont01_data:
  eqp_list.append(c01['rent_equipment'])
file01.close()

var_material_eqp = tk.StringVar()
combo_eqp = ttk.Combobox(frame_eqp_day, values=eqp_list , textvariable=var_material_eqp, width = 40,font=("",12))
combo_eqp.current(0)
combo_eqp.option_add("*TCombobox*Listbox.Font", 12)
combo_eqp.pack(fill = tk.X,side = tk.LEFT,padx=(5,30),ipadx=5,ipady=2)

###返却予定日
rent_return_l = tk.Label(frame_eqp_day, text='返却予定日：',font=("",12,"bold"),bg='#ccc')
rent_return_l.pack(side = tk.LEFT,fill = tk.X,padx=(30,0))

combo_return = DateEntry(frame_eqp_day, selectmode='day',date_pattern='yyyy/MM/dd',font=("",12))
combo_return.pack(fill = tk.X,side = tk.LEFT,padx=(5,30),ipadx=5,ipady=2)

##部署、氏名
frame_name = tk.Frame(frame_wrapper_in,bg='#ccc')
frame_name.pack(fill = tk.X,side = tk.TOP,pady=(0,20))

###部署処理
dict01 = {}
dpt_id_list=[]
mem_list_t=[]
file01=open('../data/rent_member_dpt.csv','r',encoding='utf-8')
cont01_data=csv.DictReader(file01, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
for c01 in cont01_data:
  dict01[c01['rent_dpt']]=[]
  dpt_id_list.append(c01['id'])
L_dpt_id_list=len(dpt_id_list)
for dil01 in dpt_id_list:
  if int(dil01)<10:
    f_n='mem_list0'+dil01
    mem_list_t.append(f_n)
  else:    
    f_n='mem_list'+dil01
    mem_list_t.append(f_n)

for mlt in mem_list_t:
   globals()[mlt] =[]

###氏名処理    
file02=open('../data/rent_member.csv','r',encoding='utf-8')
cont02_data=csv.DictReader(file02, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

cnt=0
count=0
while cnt < L_dpt_id_list:
  chk=cnt+1
  for c02 in cont02_data:
    if int(c02['rent_dpt'])<10:
      dpt_str='0'+str(c02['rent_dpt'])
      exec01='mem_list'+dpt_str+'.append(c02["rent_name"])'
      exec(exec01)
    else:
      dpt_str=str(c02['rent_dpt'])
      exec01='mem_list'+dpt_str+'.append(c02["rent_name"])'
      exec(exec01)    
  cnt+=1

for i,d01 in enumerate(dict01.keys(),start=1):
  if i==0:
    continue
  elif i<10:
    str_i='0' + str(i)
    exec01='dict01["'+d01+'"] = mem_list'+str_i
    exec(exec01)
  else:
    str_i=str(i)
    exec01='dict01["'+d01+'"] = mem_list'+str_i
    exec(exec01)

file01.close()
file02.close()


###部署、氏名の表示
rent_name_l = tk.Label(frame_name, text='使用者：',font=("",12,"bold"),bg='#ccc')
rent_name_l.pack(side = tk.LEFT,fill = tk.X)

var_material_dpt = tk.StringVar()
combo_dpt = ttk.Combobox(frame_name, values=list(dict01.keys()) , textvariable=var_material_dpt, width = 45,font=("",12))
combo_dpt.bind('<<ComboboxSelected>>', lambda event:combo_name.config(values=dict01[var_material_dpt.get()]))
combo_dpt.option_add("*TCombobox*Listbox.Font", 12)
combo_dpt.pack(fill = tk.X,side = tk.LEFT,padx=(5,30),ipadx=5,ipady=2)
combo_dpt.current(0)

var_material_name = tk.StringVar()
combo_name = ttk.Combobox(frame_name, values=list(dict01[var_material_dpt.get()]), textvariable=var_material_name, width = 16,font=("",12))
combo_name.option_add("*TCombobox*Listbox.Font", 12)
combo_name.pack(fill = tk.X,side = tk.LEFT,ipadx=5,ipady=2)

###その他
rent_other_f = tk.Frame(frame_wrapper_in,bg='#ccc')
rent_other_f.pack(fill = tk.X,side = tk.TOP,pady=(0,10))

rent_other_l = tk.Label(rent_other_f, text='その他：',font=("",12,"bold"),bg='#ccc')
rent_other_l.pack(side = tk.LEFT,fill = tk.X)

rent_other_entry = StringVar()
rent_other = tk.Entry(rent_other_f,textvariable=rent_other_entry,width=80,font=("", 12))
rent_other.pack(fill = tk.X,side = tk.LEFT,ipadx=5,ipady=2)


##登録ボタン
frame_btn_in = tk.Frame(frame_wrapper_in,bg='#ccc')
frame_btn_in.pack(fill = tk.X,side = tk.TOP,pady=(10,10))

m_fix_btn = tk.Button(frame_btn_in, text='貸出', width=20,font=("",12,'bold'),command=button_rent_input)
m_fix_btn.pack(side = tk.RIGHT)

#貸出状況

##貸出状況タイトル
rent_state_title_f01 = tk.Frame(root0,bg='#333')
rent_state_title_f01.pack(fill = tk.X,side = tk.TOP,padx=10,pady=(20,0))
rent_state_title_f02 = tk.Frame(rent_state_title_f01,bg='#333')
rent_state_title_f02.pack(fill = tk.X,side = tk.TOP,padx=10,pady=(20,20))

rent_sort_state = tk.Label(rent_state_title_f02, text='desc')

rent_state_title01 = tk.Label(rent_state_title_f02, text='貸出状況：',font=("",20,"bold"),fg='#fff',bg='#333')
rent_state_title01.pack(side = tk.LEFT,fill = tk.X)
rent_state_title02 = tk.Label(rent_state_title_f02, text='貸出が遅い順',font=("",16,"bold"),fg='#fff',bg='#333')
rent_state_title02.pack(side = tk.LEFT,fill = tk.X)
rent_state_title02_st = tk.Label(rent_state_title_f02, text='desc',font=("",16,"bold"),fg='#fff',bg='#333')
rent_sort_btn = tk.Button(rent_state_title_f02, text='順序入替', width=12,font=("",12,'bold'),command=button_sort)
rent_sort_btn.pack(side = tk.LEFT,fill = tk.X,padx=(50,0))
separator_rent = ttk.Separator(root0, orient="horizontal")
separator_rent.pack(side = tk.TOP, fill = tk.X,padx=10)

##借出出力フレーム
frame_wrapper_out = tk.Frame(root0,bg='#333',width=root0.winfo_width())
frame_wrapper_out.pack(side=tk.TOP,fill = tk.BOTH,padx=10,pady=(0,20),expand=1)

##貸出状況大枠
rent_state_canvas = tk.Canvas(frame_wrapper_out,height=360,bg='#333',highlightthickness=0)

df = pd.read_csv('../data/rent_list.csv')
rent_data_num=0
for index, row in df.iterrows():
 if row['rent_return_check']!=2:
      rent_data_num +=1 
s_height=(120*rent_data_num)

y_s_bar = tk.Scrollbar(frame_wrapper_out, orient=tk.VERTICAL)
y_s_bar.pack(side=tk.RIGHT, fill=tk.Y)
y_s_bar.config(command=rent_state_canvas.yview)
rent_state_canvas.config(scrollregion=(0,0,rent_state_canvas.winfo_width(),s_height))
rent_state_canvas.config(yscrollcommand=y_s_bar.set)
rent_state_canvas.pack(fill=tk.BOTH,expand=1,padx=(20,10))

rent_state_wrapper = tk.Frame(rent_state_canvas)
rent_state_wrapper.pack(side = tk.TOP,fill = tk.X,pady=(0,10),expand=1)
rent_state_canvas.create_window((0,0), window=rent_state_wrapper, anchor=tk.NW)

##貸出状況データ表示

rent_info_desc()

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
