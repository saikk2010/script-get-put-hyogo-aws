# -*- coding: utf-8 -*-
import datetime,time
import os
import shutil
import sys
import paramiko
import scp
import smtplib


#============================
#定数設定
#============================
#データ受信間隔
interval_minu= datetime.timedelta(minutes=10)
#config
config_file="config.txt"

#ssh
ip_addr= '202.247.60.211'
user_name = 'hyogo_rri_user04'
private_key = 'id_rsa'

#データ格納場所
#home/hyogo_rri_data/hyogo_rri_user04 =>  cd ~
datatime_path= r"C:/data/datetime/jmbsc/"
rain_get_path= r"C:/prog/rri_run_Riv_hyogo/Rain/"
rain_put_path= r"/home/hyogo_rri_data/hyogo_rri_user04/rri/rain/"
image_get_path= r"/home/hyogo_rri_data/hyogo_rri_user04/rri/image/"
image_put_path= r"C:/prog/rri_run_Riv_hyogo/"

Area = ["4s_1_shinonsen","4s_2_toyooka-yabu","4s_3_koto","4s_4_himeji","4s_5_kakogawa","4s_6_kobe-hanshin","4s_7_takedagawa","4s_8_awaji"]

#実況雨量の更新時刻
# JIKYO_TIME='DateJmaJ.txt'
#予測雨量の更新時刻
YOSOKU_TIME="DateJmaY.txt"


#============================
#>>>config_fileを読み込む
#============================
""" with open  (config_file,'r') as cf:
    cl_start= cf.readline()
    cl_end= cf.readline()
#datetimeオブジェクトに変換
dt_time_start= datetime.datetime.strptime(cl_start[0:12], '%Y%m%d%H%M')
dt_time_end= datetime.datetime.strptime(cl_end[0:12], '%Y%m%d%H%M') """

#前に転送した雨量データ時刻（初期定義）
try: 
    shutil.copyfile(datatime_path+YOSOKU_TIME,"base_dt_get.txt")
except Exception:
    print("YOSOKU_TIME copy err")
with open  ("base_dt_get.txt",'r') as fy_time:
        time_y= fy_time.readline()
dt_time_y= datetime.datetime.strptime(time_y[0:12], '%Y%m%d%H%M')

while(True):
    
    #============================
    #>>>予測雨量の更新時刻を読み込む
    #============================
    #shutil.copyfile(datatime_path+YOSOKU_TIME,YOSOKU_TIME)

    # with open  (YOSOKU_TIME,'r') as fy_time:
    #     time_y= fy_time.readline()
    # print(time_y)

    #datetimeオブジェクトに変換
    dt_time_y= datetime.datetime.strptime(time_y[0:12], '%Y%m%d%H%M')
    st_yy=dt_time_y.strftime('%Y')
    st_mm=dt_time_y.strftime('%m')
    st_dd= dt_time_y.strftime('%d')
    st_HH=dt_time_y.strftime('%H')
    st_MM=dt_time_y.strftime('%M')

    #print( dt_time_start, dt_time_y, dt_time_end, dt_finished) 
    #設定期間の雨量データを転送する

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Next time:", (dt_time_y+interval_minu).strftime('%Y-%m-%d %H:%M:%S'))
    with open("get_image.scp",'w+') as f:
        f.write("option batch on \n")
        f.write("option confirm off\n")
        f.write("open hyogo_rri_user04@202.247.60.211:60151\n")

        f.write(r"cd "+image_get_path+"\n")
        image_path_scp=image_get_path+st_yy+r"/"+st_mm+r"/"+st_dd+r"/"
        for area_id in Area:
            #転送対象を1時間以内に更新ファイルに制限する。 転送方向　ログインサーバ　-> AWS(現在の端末）
            f.write("synchronize local "+'-filemask=" * > 1H " '+image_put_path+area_id+"/image/"+st_yy+r"/"+st_mm+r"/"+st_dd+r"/ "+ image_get_path+area_id+"/"+st_yy+r"/"+st_mm+r"/"+st_dd+r"/"+"\n")
            f.write("get "+image_get_path+area_id+"/datatime.txt "+os.path.join(image_put_path,area_id)+"\image\datatime.txt"+"\n")
            f.write("get "+image_get_path+area_id+"/datatimeY.txt "+os.path.join(image_put_path,area_id)+"\image\datatimeY.txt"+"\n")
            #
            f.write("get "+ r"/home/hyogo_rri_data/hyogo_rri_user04/rri/disk_info.log "+r"disk_info.log"+"\n")
            if os.path.exists(image_put_path+area_id+"/image/"+st_yy+r"/"+st_mm+r"/"+st_dd):
                pass
            else:
                os.makedirs(image_put_path+area_id+"/image/"+st_yy+r"/"+st_mm+r"/"+st_dd)
        f.write("close \n")
        f.write("exit \n")

    str_scp='winscp -script=get_image.scp /privatekey=hyogo_ssh.ppk'
    os.system(str_scp)
    dt_time_y=dt_time_y+interval_minu

    #待機時間
    time.sleep(10)

"""   if(dt_time_y == dt_time_end):
        break
"""
sys.exit( )
