import shutil
import socket
import commonlib
reload(commonlib)
from commonlib import *

# Variables
logiEasyaVTest_daemon = "EasyAVTest.exe"
duration_time = "0"
tolerance_rate_rgbl = 4 # Tolerance rate = 1.57%(255 x 1.57% = 4.0035)
tolerance_rate_fps = 2
test_report_dir = r"C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results"
test_report_file = r"Stress_AWB_TestReport.txt"
test_report_path = os.path.join(test_report_dir, test_report_file)
stress_times = int(sys.argv[1])
video_format = sys.argv[2]
video_resolution = sys.argv[3]
video_framerate = sys.argv[4]

# Variables # EasyAVTest process state file(psf)
logieasyAVTest_psf = r"C:\EasyAVEngine\EasyAVTest\%s\ProcessState.ini" %(socket.gethostname())
print(logieasyAVTest_psf)

# Variables    ## Organize the EasyaVTestCmd.exe CLI (Launch EasyAVTest GUI)
logiEasyaVTest_cmd_launch = r"C:\EasyAvEngine\EasyAVTest\EasyaVTestCmd.exe /Option:TestVideo /VideoFormat:%s /VideoResolution:%s /VideoFrameRate:%s /DurationTime:%s /ShowControl:1 /InValue:EasyaVTest" %(video_format, video_resolution, video_framerate, duration_time)
print(logiEasyaVTest_cmd_launch)

# Variables    ## Organize the EasyaVTestCmd.exe CLI (analyze captured image)
logiEasyaVTest_cmd_analyze_A_head = r"C:\EasyAVEngine\EasyAVTest\EasyAVTestCmd.exe /Option:PlayImage /BMPFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_A_head.bmp /OutputFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_A_head.txt" %(video_format, video_resolution, video_framerate, video_format, video_resolution, video_framerate)
logiEasyaVTest_cmd_analyze_B_head = r"C:\EasyAVEngine\EasyAVTest\EasyAVTestCmd.exe /Option:PlayImage /BMPFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_B_head.bmp /OutputFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_B_head.txt" %(video_format, video_resolution, video_framerate, video_format, video_resolution, video_framerate)
logiEasyaVTest_cmd_analyze_A_rear = r"C:\EasyAVEngine\EasyAVTest\EasyAVTestCmd.exe /Option:PlayImage /BMPFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_A_rear.bmp /OutputFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_A_rear.txt" %(video_format, video_resolution, video_framerate, video_format, video_resolution, video_framerate)
logiEasyaVTest_cmd_analyze_B_rear = r"C:\EasyAVEngine\EasyAVTest\EasyAVTestCmd.exe /Option:PlayImage /BMPFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_B_rear.bmp /OutputFile=C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_B_rear.txt" %(video_format, video_resolution, video_framerate, video_format, video_resolution, video_framerate)

# Subroutines
def save_and_rename_img(video_format,video_resolution,video_framerate,term):
    save_an_img = find("1493197341428.png")
    click(save_an_img)
    wait(2)
    old_file = r"C:\EasyAVEngine\EasyAVTest\ManualSaveFrame.bmp"
    new_file = r"C:\Sikuli_Project\Sikuli_TestReport\Stress_AWB\Results\ManualSaveFrame_%s_%s_%s_%s.bmp" %(video_format, video_resolution, video_framerate, term)
    
    if os.path.exists(old_file):
        shutil.move(old_file,new_file)    
    else:
        print("ManualSaveFrame doesn't exist when preview in %s_%s_%s mode !" %(video_format, video_resolution, video_framerate))
    wait(2)

def analyze_img_and_return_rgbl(cmdlist):
    result = []
    out = run(cmdlist)
    for line in out.splitlines():
        pattern = line.find("Values=")
        #print(pattern) # if find the line with certain keyword(Ex : Values=) then return 0, if not then return -1
        if pattern >=0:
            #print("%s" %line) # Values=1.27, 5.08, 8.63, 4.53
            line = line.split("=")[1]
            #print("%s" %line) # 1.27, 5.08, 8.63, 4.53
            r_value = float(line.split(",")[0])   # R = 1.27
            g_value = float(line.split(",")[1])   # G = 5.08
            b_value = float(line.split(",")[2])   # B = 8.63 
            l_value = float(line.split(",")[3])   # Lux = 4.53 
            break
    result.append(r_value)
    result.append(g_value)
    result.append(b_value)
    result.append(l_value)
    return result

def read_file_and_return_fps(psf_path):
    file = open(logieasyAVTest_psf)
    for line in file:
        pattern = line.find("VideoFrameRate")
        if pattern >= 0:
            #print repr(line)     
            # Commen error when reading file line by line, delete '\n' before doing any math convertion
            line = line.strip("\n")
            line = line.split("=")[1]
            fps = float(line.split(";")[0])
            return fps
            break
    file.close()

def read_file_and_return_is_preview_successful(psf_path):
    file = open(logieasyAVTest_psf)
    for line in file:
        pattern = line.find("PreviiewStartStatus")
        if pattern >= 0:
            #print repr(line)     
            # Commen error when reading file line by line, delete '\n' before doing any math convertion
            line = line.strip("\n")
            line = line.split("=")[1]
            is_preview_successful = int(line.split(";")[0])
            return is_preview_successful
            break
    file.close()

def generate_test_report(file_path, result):
    f = open(file_path,'a')
    f.write(result + '\n')
    f.close()

def config_whitebalance(wb_value):
    wb_cli = r"C:\Program Files (x86)\Common Files\Logitech\EasyAVRuntimeEngine\EasyVideoCmd.exe /option:set /property:WHITEBALANCE /Cur:%s" %wb_value
    run(wb_cli)


# Main Function
try:

    # Check if folder "Results" exists and create it if necessary
    if not os.path.exists(test_report_dir):
        os.makedirs(test_report_dir)

    # Open EasyAVTest to preview with a specific video format/resolution/frame rate. (Ex : Preview MJPG/1920x1080/60fps)
    App.open(logiEasyaVTest_cmd_launch)
    
    while True:
        if exists("1493197314111.png"):
            # Wait 2 more seconds to let preview indeed presents
            wait(2)
            break
        wait(3)
    
    print("Open EasyAVTest test tool successfully!!")

    # Check AWB and take a picture and name it A
    config_whitebalance("auto")
    wait(3)
    save_and_rename_img(video_format,video_resolution,video_framerate,"A_head")
    # Uncheck AWB and take a picture and name it B
    config_whitebalance(6000)
    wait(3)
    save_and_rename_img(video_format,video_resolution,video_framerate,"B_head")
    
    # Config (Testing fastly switch between auto and munual of WB)
    for v_wb in range(1, stress_times+1, 1):
        # Uncheck AWB
        config_whitebalance("auto")
        # Check AWB
        config_whitebalance(6000)

    # Check AWB and take a picture and name it A'
    config_whitebalance("auto")
    wait(3)
    save_and_rename_img(video_format,video_resolution,video_framerate,"A_rear")
    # Uncheck AWB and take a picture and name it B'
    config_whitebalance(6000)
    wait(3)
    save_and_rename_img(video_format,video_resolution,video_framerate,"B_rear")

    # Config to default sate
    config_whitebalance("auto")    

    # Assess Pass/Fail
    #analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_head)
    r_val_a_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_head)[0]
    g_val_a_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_head)[1]
    b_val_a_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_head)[2]
    l_val_a_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_head)[3]
    
    #analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_head)
    r_val_b_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_head)[0]
    g_val_b_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_head)[1]
    b_val_b_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_head)[2]
    l_val_b_h = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_head)[3]

    diff_r = abs(r_val_a_h - r_val_b_h)
    diff_g = abs(g_val_a_h - g_val_b_h)
    diff_b = abs(b_val_a_h - b_val_b_h)
    diff_l = abs(l_val_a_h - l_val_b_h)

    if (diff_r >= tolerance_rate_rgbl or diff_g >= tolerance_rate_rgbl or diff_b >= tolerance_rate_rgbl or diff_l >= tolerance_rate_rgbl) or (diff_r != 0 and diff_g != 0 and diff_b != 0 and diff_l != 0):
        ###########################################################################
        # Compare if "A_end is A" and "B_end is B" only when "A is not B" is ture #
        ###########################################################################
        #analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_head)
        r_val_a_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_rear)[0]
        g_val_a_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_rear)[1]
        b_val_a_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_rear)[2]
        l_val_a_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_A_rear)[3]
        
        #analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_head)
        r_val_b_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_rear)[0]
        g_val_b_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_rear)[1]
        b_val_b_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_rear)[2]
        l_val_b_r = analyze_img_and_return_rgbl(logiEasyaVTest_cmd_analyze_B_rear)[3]
    
        diff_r_a = abs(r_val_a_r - r_val_a_h)
        diff_g_a = abs(g_val_a_r - g_val_a_h)
        diff_b_a = abs(b_val_a_r - b_val_a_h)
        diff_l_a = abs(l_val_a_r - l_val_a_h)
        
        diff_r_b = abs(r_val_b_r - r_val_b_h)
        diff_g_b = abs(g_val_b_r - g_val_b_h)
        diff_b_b = abs(b_val_b_r - b_val_b_h)
        diff_l_b = abs(l_val_b_r - l_val_b_h)

        if (diff_r_a <= tolerance_rate_rgbl and diff_g_a <= tolerance_rate_rgbl and diff_b_a <= tolerance_rate_rgbl and diff_l_a <= tolerance_rate_rgbl) and (diff_r_b <= tolerance_rate_rgbl and diff_g_b <= tolerance_rate_rgbl and diff_b_b <= tolerance_rate_rgbl and diff_l_b <= tolerance_rate_rgbl):
            test_result = "[Test Case] %s_%s_%s awb test\t-> pass" %(video_format, video_resolution, video_framerate)
            diff_value_result_ab = "[case 1] A != B : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r, diff_g, diff_b, diff_l)
            diff_value_result_a = "[case 2] A == A' : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r_a, diff_g_a, diff_b_a, diff_l_a)
            diff_value_result_b = "[case 3] B == B' : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r_b, diff_g_b, diff_b_b, diff_l_b)
            generate_test_report(test_report_path,test_result)
            generate_test_report(test_report_path,diff_value_result_ab)
            generate_test_report(test_report_path,diff_value_result_a)
            generate_test_report(test_report_path,diff_value_result_b)
        else:
            test_result = "[Test Case] %s_%s_%s awb test\t-> fail" %(video_format, video_resolution, video_framerate)
            diff_value_result_ab = "[case 1] A != B : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r, diff_g, diff_b, diff_l)
            diff_value_result_a = "[case 2] A == A' : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r_a, diff_g_a, diff_b_a, diff_l_a)
            diff_value_result_b = "[case 3] B == B' : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r_b, diff_g_b, diff_b_b, diff_l_b)
            generate_test_report(test_report_path,test_result)
            generate_test_report(test_report_path,diff_value_result_ab)
            generate_test_report(test_report_path,diff_value_result_a)
            generate_test_report(test_report_path,diff_value_result_b)
            
    else:
        test_result = "[Test Case] %s_%s_%s awb test\t-> fail" %(video_format,video_resolution,video_framerate)
        diff_value_result_ab = "[case 1] A != B : (Diff R, Diff G, Diff B, Diff L) = (%s, %s, %s, %s)" %(diff_r, diff_g, diff_b, diff_l)
        generate_test_report(test_report_path,test_result)
        generate_test_report(test_report_path,diff_value_result_ab)

    # Assess if default fps rate is correct
    fps_rate = read_file_and_return_fps(logieasyAVTest_psf)
    video_framerate = float(video_framerate)
    diff_fps_rate = abs(fps_rate - video_framerate)
    if diff_fps_rate > tolerance_rate_fps:
        test_result = "[Test Case] %s_%s_%s fps_rate test \t-> fail" %(video_format, video_resolution, video_framerate)
        test_result_fps_rate = "%s_%s_%s fps_rate = %s" %(video_format, video_resolution, video_framerate, fps_rate)
        diff_value_result = "(Diff fps rate) = (%s)" %(diff_fps_rate) + '\n'
        generate_test_report(test_report_path,test_result)
        generate_test_report(test_report_path,test_result_fps_rate)
        generate_test_report(test_report_path,diff_value_result) 
    else:
        test_result = "[Test Case] %s_%s_%s fps_rate test \t-> pass" %(video_format, video_resolution, video_framerate)
        test_result_fps_rate = "%s_%s_%s fps_rate = %s" %(video_format, video_resolution, video_framerate, fps_rate)
        diff_value_result = "(Diff fps rate) = (%s)" %(diff_fps_rate) + '\n'
        generate_test_report(test_report_path,test_result)
        generate_test_report(test_report_path,test_result_fps_rate)
        generate_test_report(test_report_path,diff_value_result)   
        
    # Close EasyAVTest to prepare launch next video format/resoluton/frame rate White Balance stress testing 
    #App.close(logiEasyaVTest_daemon)
    make_sure_EasyAVTest_closed_before_launch_next_testcase()
except FindFailed, err:
    print("[Error] %s" %err)
