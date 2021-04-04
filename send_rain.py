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
config_file="config.txt"

#ssh
ip_addr= '202.247.60.211'
user_name = 'hyogo_rri_user04'
private_key = 'id_rsa'

#?f?[?^?i?[??
datatime_path= r"C:/data/datetime/jmbsc/"
rain_get_path= r"C:/prog/rri_run_Riv_hyogo/Rain/"
rain_put_path= r"/home/hyogo_rri_data/hyogo_rri_user04/rri/rain/"
image_get_path= r"/home/hyogo_rri_data/hyogo_rri_user04/rri/image/"
image_put_path= r"C:/prog/rri_run_Riv_hyogo/"

#?????J???X?V????
JIKYO_TIME='DateJmaJ.txt'
#?\???J???X?V????
YOSOKU_TIME="DateJmaY.txt"


#============================
#>>>config_file???????
#============================
# with open  (config_file,'r') as cf:
#     cl_start= cf.readline()
#     cl_end= cf.readline()
# #datetime?I?u?W?F?N?g????
# dt_time_start= datetime.datetime.strptime(cl_start[0:12], '%Y%m%d%H%M')
# dt_time_end= datetime.datetime.strptime(cl_end[0:12], '%Y%m%d%H%M')


shutil.copyfile(datatime_path+YOSOKU_TIME,YOSOKU_TIME)
with open  (YOSOKU_TIME,'r') as fy_time:
    time_y= fy_time.readline()
#print(time_y)
#datetime?I?u?W?F?N?g????
dt_time_y= datetime.datetime.strptime(time_y[0:12], '%Y%m%d%H%M')

#print( dt_time_start, dt_time_y, dt_time_end, dt_target) 
#???????J??f?[?^??]??????
with open("datetime.txt",'r') as f:
    tmp= f.readline()
    dt_target= datetime.datetime.strptime(tmp[0:12], '%Y%m%d%H%M')

while True: 
    #print("copy YOSOKU_TIME")
    
    #?O??]???????J??f?[?^?????i??????`?j
    #============================
    #>>>?\???J???X?V???????????
    #============================
    #os.remove(YOSOKU_TIME)
    try: 
        shutil.copyfile(datatime_path+YOSOKU_TIME,YOSOKU_TIME)
        #print("YOSOKU_TIME > local")
    except Exception:
        print("copy YOSOKU_TIME err")
        continue

    with open  (YOSOKU_TIME,'r') as fy_time:
        time_y= fy_time.readline()
        
    try:
        dt_time_y= datetime.datetime.strptime(time_y[0:12], '%Y%m%d%H%M')
    except Exception:
        print("ex01")
        continue
  
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),":::dt_target:",dt_target.strftime('%Y-%m-%d %H:%M:%S'),"<=> dt_time_y:",dt_time_y.strftime('%Y-%m-%d %H:%M:%S'))
    #print(dt_time_y >= dt_target)
    if(dt_time_y >= dt_target ):

        st_yy=dt_target.strftime('%Y')
        st_mm=dt_target.strftime('%m')
        st_dd= dt_target.strftime('%d')
        st_HH=dt_target.strftime('%H')
        st_MM=dt_target.strftime('%M')

        rain_get_path2= rain_get_path+"/"+st_yy+"/"+st_mm+"/"+st_dd
        rain_file= rain_get_path2+r"/rain_"+st_yy+st_mm+st_dd+st_HH+st_MM+".txt"
        file_name="rain_"+st_yy+st_mm+st_dd+st_HH+st_MM+".txt"
        #print(rain_file)
        try:
            shutil.copyfile(rain_file,file_name)
            #print(int(os.path.getsize(file_name)) )
            if int(os.path.getsize(file_name))  < 1000000:
                dt_target= dt_target+datetime.timedelta(minutes=10)
                continue          
        except Exception:
            dt_target= dt_target+datetime.timedelta(minutes=10)
            print("ex02")
            continue
        #shutil.copyfile(rain_file)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try: 
            client.connect(hostname=ip_addr, port=60151, username=user_name, key_filename=private_key)
        except Exception :
            print("ex03")
            continue

        # create scp client object
    
        scp_client =  scp.SCPClient(client.get_transport())
        # Get &Put request to scp
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),"Transferred :",file_name)

        rain_put_path2 =rain_put_path+"/"+st_yy+"/"+st_mm+"/"+st_dd
        #make dir at remote server
        stdin, stdout, stderr = client.exec_command('mkdir -p '+rain_put_path2)
    
        try:
            #put rain file
            scp_client.put("rain_"+st_yy+st_mm+st_dd+st_HH+st_MM+".txt",rain_put_path2)

            #put rain datetimeY.txt
            scp_client.put(YOSOKU_TIME,rain_put_path)
        except Exception :
            scp_client.close()
            client.close()
            dt_target= dt_target+datetime.timedelta(minutes=10)
            print("ex04")
            continue
        #??
        os.remove("rain_"+st_yy+st_mm+st_dd+st_HH+st_MM+".txt")
        with open("log.txt",'w') as f:
            f.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+ ":"+"rain_"+st_yy+st_mm+st_dd+st_HH+st_MM+".txt")
        
        #??@ sleep
        dt_target= dt_target+datetime.timedelta(minutes=10)

        with open("datetime.txt",'w') as f:
            f.writelines(dt_target.strftime('%Y%m%d%H%M'))
        
    time.sleep(10)
sys.exit()

   