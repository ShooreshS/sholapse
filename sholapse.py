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
folder_name =  picID + shoot_time
frame_name =  picID +  "{0:0=4d}".format(frame_counter) 
save_location = "/home/shooresh/sholapse/sholapse/images/" + folder_name

def kill_gphoto2_process():
    p = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.splite(none, 1)[0])
            os.kill(pid, signal.SIGKILL)

def create_save_folder():
    try:
        os.makedirs(save_location)
    except:
        print("save to:", folder_name, end=" \n")
    os.chdir(save_location)

def rename_files():
    for filename in os.listdir(save_location):
        if not (filename.startswith(picID)):
            global frame_counter
            frame_counter += 1
            frame_name = picID + "{0:0=4d}".format(frame_counter) # datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            #print("rename: ", filename, " to: ", frame_name, end="" )
            if filename.endswith(".JPG"):
                os.rename(filename, (frame_name + ".JPG"))
                #print(".JPG", end="")
            elif filename.endswith(".CR2"):
                os.rename(filename, (frame_name + ".CR2"))
                #print(".CR2 ", end="")
 
def capture_image():
# must handle exceptions such as;  Canon EOS Capture failed to release: Perhaps no focus?
    gp(triger_cmd)
    sleep(2) # depending on exposure time + 1 Sec 
    gp(download_cmd)
    rename_files()
    gp(clear_cmd)

# initial config
kill_gphoto2_process()
create_save_folder()
gp(clear_cmd)
frame_counter = 0
counter = 0
print(" Frame name                        F_count   Video length\n", "-"*60, "\n ", end="")
try:
    while True:
        capture_image()
        counter += 1
        print(row_format.format((frame_name+".JPG"), counter, counter/25), end="\r ")
        sleep(1) # +2 seconds for download each image
except KeyboardInterrupt:
    rename_files()
    print("\n", "-"*60, "\n", "Total frames: ", counter, "\nEstimated footage: ", counter/25) 


