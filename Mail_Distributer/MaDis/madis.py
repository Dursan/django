#ライブラリ
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from tkinter import filedialog
import codecs
import tkinter.messagebox as s_msg
import tkinter.font as f
import csv
import os
import pathlib
import ntpath
import smtplib
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.utils import formatdate
from email import encoders

#初期表示データ設定
md_index=0
to_ad=0
m_attachment= 0
m_data=['dum0','dum1','dum2','dum3',None]
m_data_num=0
send_chk=[]

#データ表示関数
def data_display():
    m_data_d=[]
    for md in m_data:
        m_data_d.append(md)
    for md in m_data_d:
        m_data_num=m_data_d[0]
        file0=m_data_d[1]
        file2=m_data_d[2]
        dir3=m_data_d[3]

    #表示データ選定
    if m_data_d and m_subject and m_testmail :
        #宛先データ取得・リスト化
        m_to_d=[]
        file00=open(file0,'r',encoding='utf-8')
        cont0_data=csv.reader(file00, quotechar='"')
        for i,row in enumerate(cont0_data):
            if i == md_index+1:
                m_to_group_l["text"]=row[0]                
                m_to_name_l["text"]=row[1]                
                m_to_address_l["text"]=row[2]
                m_to_d.extend([row[0],row[1],row[2]])   
        file00.close()
       
        # 添付ファイル名取得
        m_filelist = os.listdir(path=dir3)
        m_filename = 0
        for m_f in m_filelist:
            if m_to_d[0] in m_f:
                m_filename = m_f
                break
            
        m_file=ntpath.dirname(dir3)+'\\'+m_filename
       
        frame_m_file_2["text"]=m_file
        
        #本文取得
        contents2_d=open(file2,'r',encoding='utf-8')
        contents2 = contents2_d.read()
        contents2_mod = contents2.replace('[ReplaceTarget:宛名]',m_to_d[1]).replace('[ReplaceTarget:ファイル名]', m_filename)
        m_body_d.delete('1.0', 'end')
        m_body_d.insert(tk.END,contents2_mod) 

        return(m_data_d)

#宛先宛名リストUL
def button1_clicked():
    m_data_num=0
    file00 = filedialog.askopenfilename(initialdir='~/')

    if 'mail_address-data.csv' in file00:
        with open(file00,'r',encoding='utf-8') as contents00:
            cont00_data=csv.reader(contents00, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            for i in cont00_data:
                m_data_num += 1
                send_chk.append(None)
        m_data[0]=m_data_num-1
        m_data[1]=pathlib.Path(file00)
        label0_3['text']  = file00
    else:
        label0_3['text']  = "ファイルが違います。"

#本文UL
def button2_clicked():
    file22 = filedialog.askopenfilename(initialdir='~/')
    
    if 'body.txt' in file22:
            m_data[2]=pathlib.Path(file22)
            label2_3['text'] = file22
    else:
            label2_3['text']  = "ファイルが違います。"

#添付ファイルUL
def button3_clicked():
    dir33 = filedialog.askdirectory(initialdir='~/')
    m_data[3]=pathlib.Path(dir33)
    
    label4_3['text']=dir33

#まとめ
def button4_clicked():
    #変数
    m_subject=m_subject_entry.get()
    m_testmail=m_testmail_entry.get()
    m_data_d=[]
    for md in m_data:
        m_data_d.append(md)
    for md in m_data_d:
        m_data_num=m_data_d[0]
        file0=m_data_d[1]
        file2=m_data_d[2]
        dir3=m_data_d[3]

    #表示データ選定
    if m_data_d and m_subject and m_testmail :
        #宛先データ取得・リスト化
        #file00=open(m_data_d[1],'r',encoding='utf-8')
        m_to_d=[]
        file00=open(file0,'r',encoding='utf-8')
        cont0_data=csv.reader(file00, quotechar='"')
        for i,row in enumerate(cont0_data):
            if i == 1:
                m_to_group_l["text"]=row[0]                
                m_to_name_l["text"]=row[1]                
                m_to_address_l["text"]=row[2]
                m_to_d.extend([row[0],row[1],row[2]])   
        file00.close()

        #表題取得
        m_subject=m_subject_entry.get()        
        m_subject_d["text"] = m_subject
        
        # 添付ファイル名取得
        m_filelist = os.listdir(path=dir3)
        m_filename = 0
        for m_f in m_filelist:
            if m_to_d[0] in m_f:
                m_filename = m_f
                break
        
        m_file=ntpath.dirname(dir3)+'\\'+m_filename
       
        frame_m_file_2["text"]=m_file 
        
        #本文取得
        contents2_d=open(file2,'r',encoding='utf-8')
        contents2 = contents2_d.read()
        contents2_mod = contents2.replace('[ReplaceTarget:宛名]',m_to_d[1]).replace('[ReplaceTarget:ファイル名]', m_filename)

        m_body_d.insert(tk.END,contents2_mod)

        # テスト、BCC送信先
        m_testto_address_d["text"] = m_testmail

        #内容セレクト
        num_dp01=md_index+1
        num_dp_d=str(num_dp01)+' / '+str(m_data_num)
        data_num["text"]=num_dp_d

        #メール作成用プレイス開く
        frame_mailer.pack(side = tk.LEFT, fill = tk.X,pady=0,padx=0)
    else:
        v2="データが揃っていません"
        msg.showinfo(title="結果:", message=v2)

def button5_clicked():
    md_index=md_index_d.cget("text")    
    md_index=md_index-1
    md_index_d["text"]=md_index
    
    #データ表示
    #data_display()
    m_data_d=data_display()
    m_data_num=m_data_d[0]
        
    #送信済判定
    if send_chk[md_index]:
        s_chk=' （送信済）'
        num_dp01=md_index+1
        num_dp_d=str(num_dp01)+' / '+str(m_data_num)+s_chk
    else:
        num_dp01=md_index+1
        num_dp_d=str(num_dp01)+' / '+str(m_data_num)
        
    if  num_dp01 == 1 :
        data_num["text"]=num_dp_d
        m_prev_btn.pack_forget()
    elif num_dp01 == m_data_num-1: 
        m_next_btn.pack(side = tk.RIGHT)
        data_num["text"]=num_dp_d
    else:
        data_num["text"]=num_dp_d
        

def button6_clicked():
    md_index=md_index_d["text"]
    md_index=md_index+1
    md_index_d["text"]=md_index
    
    #データ表示
    #data_display()
    m_data_d=data_display()
    m_data_num=m_data_d[0]
    

    #送信済判定
    if send_chk[md_index]:
        s_chk=' （送信済）'
        num_dp01=md_index+1
        num_dp_d=str(num_dp01)+' / '+str(m_data_num)+s_chk
    else:
        num_dp01=md_index+1
        num_dp_d=str(num_dp01)+' / '+str(m_data_num)
        
    if md_index == 1 :
        data_num["text"]=num_dp_d
        m_prev_btn.pack(side = tk.LEFT)
    elif md_index == m_data_num-1: 
        m_next_btn.pack_forget()
        data_num["text"]=num_dp_d
    else:
        data_num["text"]=num_dp_d


def button7_clicked():
    mailto = []
    subject = m_subject_d["text"]
    mailto = m_to_address_l["text"]
    testto = m_testto_address_d["text"]
    body = m_body_d.get( "1.0", "end")

    msg = MIMEMultipart()
    
#テストメール用（添付ファイル）
    m_data_d=[]
    for md in m_data:
        m_data_d.append(md)
    for md in m_data_d:
        dir3=m_data_d[3]
    
    m_filelist = os.listdir(path=dir3)
    attach_file = 0
    for m_f in m_filelist:
        if 'テスト送信用' in m_f:
            ath_file_name = m_f
            break
    ath_file_path=pathlib.Path(dir3)/ath_file_name

#メール構築
    msg['Subject'] = subject+'：テスト送信'
    msg['To'] = testto
    msg['From'] = testto
    msg['Bcc'] = testto
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    #添付ファイル添付
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(ath_file_path, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=ath_file_name)
    msg.attach(part)

    #SMTPログイン
    obj_smtp= smtplib.SMTP('smtxa.gemini.oneoffice.jp', 587)
    #obj_smtp.starttls()
    obj_smtp.login('i_sugiyama@tomoe-corporation.co.jp', 'ikunao1970')
    #obj_smtp.set_debuglevel(True)

    #メール送信
    try:
        obj_smtp.send_message(msg)
        obj_smtp.quit()
        v2='テストメール送信完了'
        s_msg.showinfo(title="送信結果:", message=v2)
        
    except Exception as E:
        v2='テストメール送信 失敗'
        s_msg.showinfo(title="送信結果:", message=v2)       
    
def button8_clicked():
    md_index=md_index_d["text"]
    subject = m_subject_d["text"]
    mailto = m_to_address_l["text"]
    testto = m_testto_address_d["text"]
    body = m_body_d.get( "1.0", "end")
    attach_file_name01=ntpath.basename(frame_m_file_2["text"])

    msg = MIMEMultipart()
    
    #テストメール用（添付ファイル）
    m_data_d=[]
    for md in m_data:
        m_data_d.append(md)
    for md in m_data_d:
        dir3=m_data_d[3]
    
    m_filelist = os.listdir(path=dir3)
    attach_file = 0
    for m_f in m_filelist:
        if attach_file_name01 in m_f:
            ath_file_name = m_f
            break
    ath_file_path=pathlib.Path(dir3)/ath_file_name

    #メール構築
    msg['Subject'] = subject
    msg['To'] = mailto
    #msg['To'] = ",".join(mailto)
    msg['From'] = testto
    msg['Bcc'] = testto
    msg['Date'] = formatdate(localtime=True)
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    #添付ファイル添付
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(ath_file_path, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename=ath_file_name)
    msg.attach(part)

    #SMTPログイン
    obj_smtp= smtplib.SMTP('smtxa.gemini.oneoffice.jp', 587)
    obj_smtp.login('i_sugiyama@tomoe-corporation.co.jp', 'ikunao1970')
    #obj_smtp.set_debuglevel(True)

    #メール送信
    try:
        obj_smtp.send_message(msg)
        obj_smtp.quit()
        v2='メール送信完了'
        s_msg.showinfo(title="送信結果:", message=v2)
        send_chk[md_index]=1
        data_num_t=data_num["text"]
        data_num["text"]=data_num_t+' （送信済）'
    except Exception as E:
        v2='メール送信 失敗'
        s_msg.showinfo(title="送信結果:", message=v2)
        print(E)

#データ入力ウインドウ
root0 = Tk()
root0.title('メール送信システム データ選択')
root0.minsize(width=960, height=360)
root0.columnconfigure(0, weight=1)
root0.rowconfigure(0, weight=1)


#体裁初期値
font_label = f.Font(weight="bold", size=10)
font_num = f.Font(weight="bold", size=14)
font_body = f.Font(size=10)
style = ttk.Style()
style.configure('mf_btn.TButton', font =("",10,"bold"))

#WrapperFrame
frame_wrapper = tk.Frame(root0)
frame_wrapper.pack(side = tk.TOP,fill = tk.BOTH,pady=20)

frame_wrapper.columnconfigure(0, weight=1)
frame_wrapper.rowconfigure(0, weight=1)

# 宛先・宛名リストファイル
frame0 = tk.Frame(frame_wrapper)
frame0.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame0_1 = tk.Frame(frame0,width=200,height=30)
frame0_1.pack_propagate(0)
frame0_1.pack(side = tk.LEFT)
frame0_2 = tk.Frame(frame0,width=150,height=30)
frame0_2.pack_propagate(0)
frame0_2.pack(side = tk.LEFT)
frame0_3 = tk.Frame(frame0,width=590,height=30)
frame0_3.pack_propagate(0)
frame0_3.pack(side = tk.LEFT,padx=(15,0))

label0_1 = tk.Label(frame0_1, text='宛先・宛名：',font=font_label)
name_list_btn = tk.Button(frame0_2, text='ファイル選択', width=20,command=button1_clicked)
label0_3 = tk.Label(frame0_3, text='',font=f.Font(size=11),wraplength=580,justify="left")

label0_1.pack(side = tk.RIGHT)
name_list_btn.pack(side = tk.LEFT)
label0_3.pack(side = tk.LEFT,anchor=tk.W)

# 表題入力
frame1 = tk.Frame(frame_wrapper)
frame1.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame1_1 = tk.Frame(frame1,width=200,height=30)
frame1_1.pack_propagate(0)
frame1_1.pack(side = tk.LEFT)
frame1_2 = tk.Frame(frame1,width=550,height=30)
frame1_2.pack_propagate(0)
frame1_2.pack(side = tk.LEFT)


label1 = tk.Label(frame1_1, text='表題：',font=font_label)
m_subject_entry = StringVar()
m_subject = tk.Entry(frame1_2,textvariable=m_subject_entry,width=80,font=("", 11))

label1.pack(side = tk.RIGHT, fill = tk.X)
m_subject.pack(side = tk.LEFT, fill = tk.X)

# 本文ファイル
frame2 = tk.Frame(frame_wrapper)
frame2.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame2_1 = tk.Frame(frame2,width=200,height=30)
frame2_1.pack_propagate(0)
frame2_1.pack(side = tk.LEFT)
frame2_2 = tk.Frame(frame2,width=150,height=30)
frame2_2.pack_propagate(0)
frame2_2.pack(side = tk.LEFT)
frame2_3 = tk.Frame(frame2,width=590,height=60)
frame2_3.pack_propagate(0)
frame2_3.pack(side = tk.LEFT,padx=(15,0))

label2_1 = tk.Label(frame2_1, text='本文ファイル：',font=font_label)

m_body_btn = tk.Button(frame2_2, text='ファイル選択', width=20,command=button2_clicked)
label2_3 = tk.Label(frame2_3, text='',font=f.Font(size=11),wraplength=580,justify="left")

label2_1.pack(side = tk.RIGHT, fill = tk.X)
m_body_btn.pack(side = tk.LEFT)
label2_3.pack(side = tk.LEFT,anchor=tk.W)

# テスト、BCC送り先入力
frame3 = tk.Frame(frame_wrapper)
frame3.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame3_1 = tk.Frame(frame3,width=200,height=30)
frame3_1.pack_propagate(0)
frame3_1.pack(side = tk.LEFT)
frame3_2 = tk.Frame(frame3,width=550,height=30)
frame3_2.pack_propagate(0)
frame3_2.pack(side = tk.LEFT)

label3_1 = tk.Label(frame3_1, text='テスト送信、BCC、送信元：',font=font_label)

m_testmail_entry = StringVar()
m_testmail = tk.Entry(frame3_2,textvariable=m_testmail_entry,width=80,font=("", 11))

label3_1.pack(side = tk.RIGHT, fill = tk.X)
m_testmail.pack(side = tk.LEFT, fill = tk.X)
m_testmail.update()


# 添付ファイルフォルダ
frame4 = tk.Frame(frame_wrapper)
frame4.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame4_1 = tk.Frame(frame4,width=200,height=30)
frame4_1.pack_propagate(0)
frame4_1.pack(side = tk.LEFT)
frame4_2 = tk.Frame(frame4,width=150,height=30)
frame4_2.pack_propagate(0)
frame4_2.pack(side = tk.LEFT)
frame4_3 = tk.Frame(frame4,width=590,height=60)
frame4_3.pack_propagate(0)
frame4_3.pack(side = tk.LEFT, fill = tk.X,padx=(15,0))

label4_1 = tk.Label(frame4_1, text='添付ファイルフォルダ：',font=font_label)

m_append_btn = tk.Button(frame4_2, text='フォルダ選択', width=20,command=button3_clicked)
label4_3 = tk.Label(frame4_3, text='',font=f.Font(size=10),wraplength=580,justify="left")

label4_1.pack(side = tk.RIGHT)
m_append_btn.pack(side = tk.LEFT)
label4_3.pack(side = tk.LEFT,anchor=tk.W)


# 準備ボタン
frame5 = tk.Frame(frame_wrapper)
frame5.pack(side = tk.TOP, fill = tk.X,pady=(10,0),padx=10)

m_fix_btn = ttk.Button(frame5, text='メール作成準備',style='mf_btn.TButton', width=40,command=button4_clicked)
m_fix_btn.pack(side = tk.TOP)

##メール生成プレイス
frame_mailer = tk.Frame(frame_wrapper)
#frame_mailer.pack(side = tk.LEFT, fill = tk.X,pady=0,padx=10)
frame_mailer.columnconfigure(0, weight=1)
frame_mailer.rowconfigure(0, weight=1)
frame_mailer.pack_forget()

#分割線
style.configure("gray.TSeparator", background="gray90")
separator = ttk.Separator(frame_mailer, orient="horizontal", style="gray.TSeparator")
separator.pack(side = tk.TOP, fill = tk.X,padx=10,pady=10)

#内容セレクト
frame_mailer_1 = tk.Frame(frame_mailer)
frame_mailer_1.pack(side = tk.TOP, fill = tk.X)

frame_m_prev = tk.Frame(frame_mailer_1)
frame_m_prev.pack(side = tk.LEFT, fill = tk.X,anchor = tk.W,padx=30)
frame_m_next = tk.Frame(frame_mailer_1)
frame_m_next.pack(side = tk.RIGHT, fill = tk.X,anchor = tk.E,padx=30)
data_num_dp = tk.Frame(frame_mailer_1)
data_num_dp.pack(side = tk.TOP, fill = tk.X,anchor = tk.N,padx=30)

num_dp_d=str(md_index)+' ／ '+str(m_data_num)

m_prev_btn = tk.Button(frame_m_prev, text='←前へ', width=10,command=button5_clicked)
m_prev_btn.pack_forget()
data_num = tk.Label(data_num_dp, text=num_dp_d, width=30,font=font_num)
data_num.pack(side = tk.TOP)
m_next_btn = tk.Button(frame_m_next, text='次へ→', width=10,command=button6_clicked)
m_next_btn.pack(side = tk.TOP)


#表題
frame_mailer_2 = tk.Frame(frame_mailer)
frame_mailer_2.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame_mailer_2_1 = tk.Frame(frame_mailer_2,width=180,height=30)
frame_mailer_2_1.pack_propagate(0)
frame_mailer_2_1.pack(side = tk.LEFT)
frame_mailer_2_2 = tk.Frame(frame_mailer_2,width=500,height=30)
frame_mailer_2_2.pack_propagate(0)
frame_mailer_2_2.pack(side = tk.LEFT,padx=10,expand=1,anchor=tk.W)

frame_m_subject_l = tk.Label(frame_mailer_2_1, text='表題：',font=font_label)
frame_m_subject_l.pack(side = tk.RIGHT)

m_subject_d = tk.Label(frame_mailer_2_2, text="",font=font_label)
m_subject_d.pack(side = tk.LEFT, fill = tk.X)

#送り先名
frame_mailer_3 = tk.Frame(frame_mailer)
frame_mailer_3.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

md_index_d = tk.Label(frame_mailer_3, text=md_index)
frame_mailer_3_1 = tk.Frame(frame_mailer_3,width=180,height=30)
frame_mailer_3_1.pack_propagate(0)
frame_mailer_3_1.pack(side = tk.LEFT)

frame_m_to_group_l = tk.Label(frame_mailer_3_1, text='送り先名：',font=font_label)
frame_m_to_group_l.pack(side = tk.RIGHT, fill = tk.X)

frame_mailer_3_2 = tk.Frame(frame_mailer_3,width=500,height=30)
frame_mailer_3_2.pack_propagate(0)
frame_mailer_3_2.pack(side = tk.LEFT,padx=10,expand=1,anchor=tk.W)

m_to_group_l = tk.Label(frame_mailer_3_2, text="",font=font_label)
m_to_group_l.pack(side = tk.LEFT, fill = tk.X)

#宛名
frame_mailer_4 = tk.Frame(frame_mailer)
frame_mailer_4.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame_mailer_4_1 = tk.Frame(frame_mailer_4,width=180,height=30)
frame_mailer_4_1.pack_propagate(0)
frame_mailer_4_1.pack(side = tk.LEFT)

frame_m_to_name_l = tk.Label(frame_mailer_4_1, text='宛名：',font=font_label)
frame_m_to_name_l.pack(side = tk.RIGHT, fill = tk.X)

frame_mailer_4_2 = tk.Frame(frame_mailer_4,width=500,height=30)
frame_mailer_4_2.pack_propagate(0)
frame_mailer_4_2.pack(side = tk.LEFT,padx=10)

m_to_name_l = tk.Label(frame_mailer_4_2, text="",font=font_label)
m_to_name_l.pack(side = tk.LEFT, fill = tk.X)

#送り先メールアドレス
frame_mailer_5 = tk.Frame(frame_mailer)
frame_mailer_5.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10,expand=1)

frame_mailer_5_1 = tk.Frame(frame_mailer_5,width=180,height=30)
frame_mailer_5_1.pack_propagate(0)
frame_mailer_5_1.pack(side = tk.LEFT)

frame_m_to_address_l = tk.Label(frame_mailer_5_1, text='送り先アドレス：',font=font_label,justify="left")
frame_m_to_address_l.pack(side = tk.RIGHT, fill = tk.X)

frame_mailer_5_2 = tk.Frame(frame_mailer_5,width=750,height=30)
frame_mailer_5_2.pack_propagate(0)
frame_mailer_5_2.pack(side = tk.LEFT,padx=10)

m_to_address_l = tk.Label(frame_mailer_5_2, text="",font=font_label,wraplength=750,justify="left")
m_to_address_l.pack(side = tk.LEFT, fill = tk.X,anchor=tk.W)

#添付ファイル
frame_mailer_6 = tk.Frame(frame_mailer)
frame_mailer_6.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame_mailer_6_1 = tk.Frame(frame_mailer_6,width=180,height=30)
frame_mailer_6_1.pack_propagate(0)
frame_mailer_6_1.pack(side = tk.LEFT)

frame_m_file_l = tk.Label(frame_mailer_6_1, text='添付ファイル ：',font=font_label)
frame_m_file_l.pack(side = tk.RIGHT, fill = tk.X)

frame_mailer_6_2 = tk.Frame(frame_mailer_6,width=500,height=60)
frame_mailer_6_2.pack_propagate(0)
frame_mailer_6_2.pack(side = tk.LEFT,padx=10)

frame_m_file_2 = tk.Label(frame_mailer_6_2, text="" ,font=font_label,wraplength=750,justify="left")
frame_m_file_2.pack(side = tk.LEFT, fill = tk.X)

#テスト、BCC送信先
frame_mailer_7 = tk.Frame(frame_mailer)
frame_mailer_7.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame_mailer_7_1 = tk.Frame(frame_mailer_7,width=180,height=30)
frame_mailer_7_1.pack_propagate(0)
frame_mailer_7_1.pack(side = tk.LEFT, fill = tk.X)

m_testto_address_l = tk.Label(frame_mailer_7_1, text='テスト、BCC送信先：',font=font_label)
m_testto_address_l.pack(side = tk.RIGHT, fill = tk.X)

frame_mailer_7_2 = tk.Frame(frame_mailer_7,width=500,height=30)
frame_mailer_7_2.pack_propagate(0)
frame_mailer_7_2.pack(side = tk.LEFT,padx=10)

m_testto_address_d = tk.Label(frame_mailer_7_2, text='',font=font_label)
m_testto_address_d.pack(side = tk.LEFT, fill = tk.X)

#本文
frame_mailer_8 = tk.Frame(frame_mailer)
frame_mailer_8.pack(side = tk.TOP, fill = tk.X,pady=5,padx=10)

frame_m_body_l = tk.Label(frame_mailer_8, text='本文：',font=font_label)
frame_m_body_l.pack(side = tk.LEFT,padx=10)

m_body_d = tk.Text(frame_mailer_8,font=font_body,width=120,height=20, padx=10, pady=10)
m_body_d.pack(side = tk.LEFT,padx=10,ipadx=5)
scroll_y = tk.Scrollbar(frame_mailer_8, orient="vertical", command=m_body_d.yview)
scroll_y.pack(side="left", expand=True, fill="y")
m_body_d.configure(yscrollcommand=scroll_y.set)
m_body_d.columnconfigure(0, weight=1)
m_body_d.rowconfigure(0, weight=1)


#送信ボタン
frame_mailer_9 = tk.Frame(frame_mailer)
frame_mailer_9.pack(side = tk.TOP, fill = tk.BOTH,pady=(10,10))

frame_mailer_9_1 = tk.Frame(frame_mailer)
frame_mailer_9_1.pack(side = tk.RIGHT, fill = tk.X)

frame_mailer_9_2 = tk.Frame(frame_mailer)
frame_mailer_9_2.pack(side = tk.RIGHT, fill = tk.X)

frame_m_realsendbtn = ttk.Button(frame_mailer_9_1, text='本番メール送信',style='mf_btn.TButton', width=30,command=button8_clicked)
frame_m_realsendbtn.pack(side = tk.TOP, fill = tk.X,padx=20,pady=5)

frame_m_testsendbtn = ttk.Button(frame_mailer_9_2, text='テストメール送信',style='mf_btn.TButton', width=30,command=button7_clicked)
frame_m_testsendbtn.pack(side = tk.TOP, fill = tk.X,padx=10,pady=5)


root0.mainloop()

