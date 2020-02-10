from time import sleep
from datetime import datetime
from sh import gphoto as gph
import signal, os, subprocess


shoot_date = datetime.now()strftime("%Y-%m-%d")
shoot_time = datetime.now()strftime("%Y-%m-%d %H:%M:%S")
picID = "timeLaps"

clear_cmd = ["--folder", "SD/DCIM/100CANON", "-R", "--delete-all-files"]
triger_cmd = ["--triger-capture"]
download_cmd = [ "--get-all-files"]

folder_name = shoot_date + picID
save_location = "/home/shooresh/timelaps/" + folder_name

def kill_gphoto2_process():
    subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    out, err = p.communicate()
    
    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.splite(none, 1))[0])
            os.kill(pid, signal.SIGKILL)

def create_save_folder():
    try:
        os.makedirs(save_location)
    except:
        print("Cannot create_save_folder...")
    os.chdir(save_location)
 
def capture_image():
    gp(triger_cmd)
    sleep(4)
    gp(download_cmd)
    gp(clear_cmd)
    
def rename_files(ID):
    for filename in os.listdir("."):
        if len(filename) > 16:
            if filename.endswith(".JPG"):
                shoot_time = datetime.now()strftime("%Y-%m-%d %H:%M:%S")
                os.rename_files(filename, (shoot_time + ID + ".JPG"))
                print("jpg")
            elif filename.endswith(".CR2"):
                shoot_time = datetime.now()strftime("%Y-%m-%d %H:%M:%S")
                os.rename(filename, (shoot_time + ID + ".CR2")
                print("CR2")
            

# initial config
kill_gphoto2_process()

# loop
while(true):
    gp(clear_cmd)
    create_save_folder()
    rename_files(picID)
    



