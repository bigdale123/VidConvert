import os
import platform
import subprocess

def handbrake(half_path_list,source_path,convert_path):
    current_file = ""
    error_files = []
    for i in half_path_list:
        for file in os.listdir(source_path+i):
            if os.path.isfile(os.path.join(source_path+i, file)):
                if platform.system() == "Linux":
                    current_file = source_path+i+"/"+file
                    output_file = convert_path+i+"/"+file
                    print(current_file)
                    cmd = ['HandBrakeCLI','-Z',"General/Fast 1080p30",'-i',current_file,'-o',output_file,'--subtitle', 'scan,1,2,3,4,5,6,7,8,9,10', '-a', '1,2,3,4,5,6,7,8,9,10']
                elif platform.system() == "Windows":
                    current_file = source_path+i+"\\"+file
                    output_file = convert_path+i+"\\"+file
                    print(current_file)
                    cmd = ['C:\Program Files\Handbrake\HandBrakeCLI.exe','-Z',"General/Fast 1080p30",'-i',current_file,'-o',output_file,'--subtitle', 'scan,1,2,3,4,5,6,7,8,9,10', '-a', '1,2,3,4,5,6,7,8,9,10']
                subprocess.call(cmd)


def prepFunc(path,output_path):
    # convert_path = os.getcwd()+"\\"+str(series)+"_ReEnc"
    list_to_make = []
    for top, dirs, files in os.walk(path, topdown=True):
        if platform.system() == "Linux":
            list_to_make.append("/"+top[len(path)+1:])
        elif platform.system() == "Windows":    
            list_to_make.append("\\"+top[len(path)+1:])
    print(list_to_make)
    for i in range(len(list_to_make)):
        if platform.system() == "Linux":
            if list_to_make[i] == "/":
                list_to_make[i] = ""
            else:
                os.system("mkdir "+"\""+output_path+list_to_make[i]+"\"")
                print("mkdir "+"\""+output_path+list_to_make[i]+"\"")
        elif platform.system() == "Windows":
            if list_to_make[i] == "\\":
                list_to_make[i] = ""
            else:
                os.system("mkdir "+"\""+output_path+list_to_make[i]+"\"")
                print("mkdir "+"\""+output_path+list_to_make[i]+"\"")
    return list_to_make

output_folder = "C:\\Users\\Dylan\\Desktop\\Jimmy_Neutron_Boy_Genius_ReEnc"
input_folder = "C:\\Users\\Dylan\\Desktop\\Jimmy_Neutron_Boy_Genius"

half_path_list = prepFunc(input_folder,output_folder)
handbrake(half_path_list,input_folder,output_folder)
