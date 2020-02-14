from time import sleep
from datetime import datetime
from sh import gphoto2 as gp
import signal, os, subprocess


#shoot_date = datetime.now().strftime("%Y-%m-%d")
shoot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
picID = "shol_"
frame_counter = 0
clear_cmd = ["--folder", "/store_00020001/DCIM/100CANON", "-R", "--delete-all-files"]
triger_cmd = ["--trigger-capture"]
download_cmd = [ "--get-all-files"]
row_format ="{:>33} {:>6} {:>15}" 
main_dir_name =  picID + shoot_time
frame_name =  picID +  "{0:0=4d}".format(frame_counter) 
save_location = "/home/shooresh/sholapse/sholapse/images/" + main_dir_name

lighting_time = 2  # cieling(actual lighting time on the camera) + 1
frame_interval_time = 10  # lighting_time + move_stack + move_stack back + move_frame + n = opperation_time < frame_interval_time, effective frame_interval_time -= opperation_time 


def kill_gphoto2_process():
    p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        print(line)
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split()[0])
            os.kill(pid, signal.SIGKILL)

def create_save_dir(save_loc):
    try:
        os.makedirs(save_loc)
    except:
        print("save to:", main_dir_name, end=" \n")
    os.chdir(save_loc)

def rename_files(pic_name, stack_dir):
    for filename in os.listdir(save_location + stack_dir):
        print(filename, " in ", (save_location + stack_dir))
        if not (filename.startswith("stk_f_")):
            #global frame_counter
            #frame_counter += 1
            frame_name = pic_name   # + "{0:0=4d}".format(frame_counter) # datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print("rename: ", filename, " to: ", frame_name, end="" )
            if filename.endswith(".JPG"):
                os.rename(filename, (frame_name + ".JPG"))
                #print(".JPG", end="")
            elif filename.endswith(".CR2"):
                os.rename(filename, (frame_name + ".CR2"))
                #print(".CR2 ", end="")
 
def capture_image(pic_name, stack_dir):
# must handle exceptions such as;  Canon EOS Capture failed to release: Perhaps no focus?
    gp(triger_cmd)
    sleep(lighting_time) # depending on exposure time + 1 Sec 
    gp(download_cmd)
    rename_files(pic_name, stack_dir)
    gp(clear_cmd)


def move_stack(step):
	print("[move_stack] ... ")
	if(step > 0):
		# move step forward
		print("[move_stack] step FORWARD ")
	else:
		print("[move_stack] move back ")
		# move |step| backward 

def move_plan(x, y, z):
	print("[move_plan] moveing forward by ", x, " ", y," ", z)


def capture_stack():
	total_frame_cnt = 10 # 1-9999
	stack_count = 4
	global frame_counter
	frame_counter += 1
	print("[capt_stk] ", )
	for i in range(total_frame_cnt):
		# TAKE A STACK NEEDED FOR ONE FINAL FRAME
		stack_dir = "/frm_" + "{0:0=4d}".format(i+1)
		create_save_dir(save_location + stack_dir)
		for j in range(stack_count):
			pic_name = "stk_f_" + "{0:0=2d}".format(j+1)
			# lights(1)
			capture_image(pic_name, stack_dir)  # 
			# lights(0)
			move_stack(1)
		move_stack(stack_count * -1)
		print("[capt_stk] stack_count ", stack_count)
		move_plan(1, 1, 1)
		print(" Waitng for ", frame_interval_time, " second...")
		sleep(frame_interval_time)
		
# initial config
kill_gphoto2_process()
create_save_dir(save_location)
gp(clear_cmd)
frame_counter = 0
counter = 0



print(" Frame name                        F_count   Video length\n", "-"*60, "\n ", end="")
try:
	capture_stack()
except KeyboardInterrupt:
    rename_files()
    kill_gphoto2_process()
    print("\n", "-"*60, "\n", "Total frames: ", counter, "\nEstimated footage: ", counter/25)


#    while True:
 #       capture_image()
  #      counter += 1
   #     frame_name
    #    print(row_format.format((frame_name+".JPG"), counter, counter/25), end="\r ")
     #   sleep(10) # +2 seconds for download each image


# timelapse_dir_datetime
# 	frm_001
#		stk_f_01.JPG   	
#		stk_f_02.JPG
#		stk_f_03.JPG   	
# 	frm_002
#		stk_f_01.JPG   	
#		stk_f_02.JPG
#		stk_f_03.JPG   	
# 	frm_n
#		stk_f_01.JPG   	
#		stk_f_02.JPG
#		stk_f_03.JPG   	



