# -*- coding: utf-8 -*-
import datetime,time
import os
import shutil
import sys
import paramiko
import scp
import smtplib


#============================
#?????
#============================
#?f?[?^??M??u
interval_minu= datetime.timedelta(minutes=10)
#config
#config_file="config.txt"

#ssh
#ip_addr= '202.247.60.211'
#user_name = 'hyogo_rri_user04'
#private_key = 'id_rsa'

#?f?[?^?i?[??
#home/hyogo_rri_data/hyogo_rri_user04 =>  cd ~
datatime_get_path= r"/data/datetime/jmbsc/"
datatime_put_path= r"C:\\data\\datetime\\jmbsc\\"
rain_get_path= r"/prog/rri_run_Riv_hyogo/Rain/"
rain_put_path= r"C:\\prog\\rri_run_Riv_hyogo\\Rain\\"
image_get_path= "C:\\prog\\rri_run_Riv_hyogo\\"
image_put_path= r"/prog/rri_run_Riv_hyogo/"

Area = ["4s_1_shinonsen","4s_2_toyooka-yabu","4s_3_koto","4s_4_himeji","4s_5_kakogawa","4s_6_kobe-hanshin","4s_7_takedagawa","4s_8_awaji"]
#Area = ["4s_1_shinonsen"]


YOSOKU_TIME="DateJmaY.txt"

#?O??]???????J??f?[?^?????i??????`?j
try: 
    shutil.copyfile(datatime_put_path+YOSOKU_TIME,"base_dt_put.txt")
except Exception:
    print("YOSOKU_TIME copy err")


with open  ("base_dt_put.txt",'r') as fy_time:
    time_y= fy_time.readline()
dt_time_y= datetime.datetime.strptime(time_y[0:12], '%Y%m%d%H%M')

while(True):
    #datetime?I?u?W?F?N?g????
    dt_time_y= datetime.datetime.strptime(time_y[0:12], '%Y%m%d%H%M')
    st_yy=dt_time_y.strftime('%Y')
    st_mm=dt_time_y.strftime('%m')
    st_dd= dt_time_y.strftime('%d')
    st_HH=dt_time_y.strftime('%H')
    st_MM=dt_time_y.strftime('%M')

    #print( dt_time_start, dt_time_y, dt_time_end, dt_finished) 
    #???????J??f?[?^??]??????

    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Next time:", (dt_time_y+interval_minu).strftime('%Y-%m-%d %H:%M:%S'))
    img_dt=dt_time_y.strftime('%Y%m%d%H%M')
    with open("put_image.scp",'w+') as f:
        f.write("option batch on \n")
        f.write("option confirm off\n")
        f.write("open  ftp://ftp-user:ftp-user@52.69.140.64\n")
        
		

        for area_id in Area:
            #?]??????1???????X?V?t?@?C???????????B ?]???????@???O?C???T?[?o?@-> AWS(?????[???j
            f.write("mkdir "+image_put_path+area_id+"/image/"+st_yy+r"/"+st_mm+r"/"+st_dd+"\n")
            f.write("synchronize remote "+'-filemask=" * > 1H " '+ image_get_path+area_id+"\\image\\"+st_yy+"\\"+st_mm+"\\"+st_dd+"\\ "+ image_put_path+area_id+"/image/"+st_yy+r"/"+st_mm+r"/"+st_dd+r"/"+"\n")
            # for type_img in ["hr","hs","qr"]:
            #     print(type_img)
            #     f.write("put "+image_get_path+area_id+"\\image\\"+st_yy+"\\"+st_mm+"\\"+st_dd+"\\"+type_img+"\\"+type_img+"_"+img_dt+"*  " +image_put_path+area_id+"/"+st_yy+r"/"+st_mm+r"/"+st_dd+r"/"+type_img+"/"+"\n")
                       
				
            f.write("put "+image_get_path+area_id+"\\image\\datatime.txt "+os.path.join(image_put_path,area_id)+"/image/datatime.txt"+"\n")
            f.write("put "+image_get_path+area_id+"\\image\\datatimeY.txt "+os.path.join(image_put_path,area_id)+"/image/datatimeY.txt"+"\n")

            #rain block
                # datatime_get_path= r"/data/datetime/jmbsc/"
                # datatime_put_path= r"C:\\data\\datetime\\jmbsc\\"
                # rain_get_path= r"/prog/rri_run_Riv_hyogo/Rain/"
                # rain_put_path= r"C:\\prog\\rri_run_Riv_hyogo\\Rain\\"
            f.write("get "+datatime_get_path+YOSOKU_TIME+" "+datatime_put_path+YOSOKU_TIME+"\n")
            f.write("synchronize local "+'-filemask=" * > 1H " '+rain_put_path+st_yy+"\\"+st_mm+r"\\"+st_dd+r"\\ "+ rain_get_path+st_yy+r"/"+st_mm+r"/"+st_dd+r"/"+"\n")
            #rain block

        f.write("close \n")
        f.write("exit \n")

    str_scp='winscp -script=put_image.scp'
    try:
        os.system(str_scp)
    except Exception:
        print("os.system(str_scp)")
        continue
    
    dt_time_y=dt_time_y+interval_minu

    #??@????
    time.sleep(10)
