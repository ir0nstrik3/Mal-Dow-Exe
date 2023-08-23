#!/usr/bin/python3

import os
import requests
import time
import pyzipper
import json
import sys

def clear_console():
    sys.stdout.write("\033c")
    sys.stdout.flush()
    
clear_console()
file_exe_validation = input("please say Yes or No in uppercase Letters to automatic executing the samples: ")
vali_choices = ["NO","YES"]
clear_console()

while file_exe_validation not in vali_choices:
    file_exe_validation = input("please say Yes or No in uppercase Letters to automatic executing the samples: ")
    clear_console()

    
malware_types = ["exe", "doc", "xls", "dll", "msi", "ps1"]
select_types = []


while True:
    clear_console()
    
    print("Please choose the Malware Typey's")
    for i, malware_type in enumerate(malware_types):
        print(f"{i + 1}: {malware_type}")

    if select_types:
        print("\nSelected Malware Type's")
        for i, option in enumerate(select_types):
            print(f"{i + 1}: {option}")
            
    choice = input("\n Please select a number of an Malware Type or (delete with 'r' or end the selection with 'd'): ")
    
    if choice.lower() == "d":
        break
    elif choice.lower() == "r":
        if select_types: 
            clear_console()

            print("\nSelected Malware Type's")
            for i, option in enumerate(select_types):
                print(f"{i +1}: {option}")
            remove_choice = input("\nSelect an Malware type to delete or ( 'q' to quit ): ")
            if remove_choice.lower() == "q":
                continue
            try :
                remove_choice = int(remove_choice)
                if 1 <= remove_choice <= len(select_types):
                    removed_option = select_types.pop(remove_choice - 1)
                    print(f"{removed_option} was deleted")
                    time.sleep(0.5)    
                else:
                    print(f"Not Allowed, please choice an Option between 1 and {len(select_types)}")
            except ValueError:
                print("Not Allowed input Please insert a Number")
        else:
            print("No Options there to delet!")
            time.sleep(0.5)
    else:
        try:
            choice = int(choice)
            if 1 <= choice <= len(malware_types):
                selected_option = malware_types[choice - 1]
                if selected_option not in select_types:
                    select_types.append(selected_option)
                    time.sleep(0.1)
                else:
                    print("This Malware Type is still selectetd")
                    time.sleep(0.5)
            else:
                print(f"Not Allowed, please insert a number between 1 and {len(malware_types)}")
                time.sleep(0.5)
        except:
            print(f"Not Allowed, please insert a Number between 1 and {len(malware_types)}")
            time.sleep(0.5)
clear_console()
           
print("Your selected Malware Type's")            
for i, option in enumerate(select_types):
    print(f"{i + 1}: {option}")
time.sleep(2)

clear_console()

samples_amount = []

for sample in select_types:
    amount_input = input(f"How much Smaples of {sample}'s do you want: ")
    clear_console()
    while amount_input.isnumeric() == False:
        amount_input = input(f"How much Smaples of {sample}'s do you want: ")
        clear_console()
    samples_amount.append(amount_input)
    
for sample, i in zip(select_types,samples_amount):
    print(f"for type {sample} you choose {i} sample's")

time.sleep(5)
clear_console()

print("wait some time ...")         
       
current_path = str(os.path.dirname(os.path.realpath(__file__))) + "/"
dir_name = "Samples"

if os.path.isdir(current_path + dir_name) != True:
    dir_path = os.path.join(current_path, dir_name)
    dir_mode = 0o777
    os.mkdir(dir_path, dir_mode)

download_path = str(current_path) + "Samples/"

for sample, number in zip(select_types, samples_amount):
    download_file_json = requests.post('https://mb-api.abuse.ch/api/v1/', data={'query': 'get_file_type', 'file_type': sample, 'limit': number})
    open(download_path + "Malware_samples_" + str(sample) + ".json", 'wb').write(download_file_json.content)
    time.sleep(5)
malware_sha256_hash_list = []


for samples in select_types:
    json_file = open(download_path + "Malware_samples_" + str(samples) + ".json")
    try:
        json_data = json.load(json_file)
        for i in json_data['data']:
            malware_sha256_hash_list.append(i['sha256_hash'])
        json_file.close()
    except ValueError:
        print("in one jason was an error and was skipped !")

  
malware_count = 0

while malware_count < int(len(malware_sha256_hash_list)):
    sha256 = malware_sha256_hash_list[malware_count]
    download_file = requests.post('https://mb-api.abuse.ch/api/v1/', data={'query': 'get_file', 'sha256_hash': sha256})
    open(download_path + "Malware_" + str(malware_count) + ".zip", 'wb').write(download_file.content)
      
    with pyzipper.AESZipFile(download_path + "Malware_" + str(malware_count) + ".zip", 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as zip_ref:
        zip_ref.extractall(download_path , members=None, pwd=b'infected')

    os.remove(download_path + "Malware_" + str(malware_count) + ".zip")
    malware_count += 1
    
    print(f"file {malware_count} of {len(malware_sha256_hash_list)} is downloaded now !", end="\r")
    time.sleep(0.5)


for i in select_types:
    os.remove(download_path + "Malware_samples_" + str(i) + ".json")
 
print("\n")
print("0.5 min later it will let you know how much files are left")
time_count = 0
for seconds in range(0,30):
    time_count += 1
    print(f"Seconds {time_count}", end="\r")
    time.sleep(1)

yes_choice = "YES"
no_choice = "NO"
file_list = []

for filename in os.listdir(download_path):
    f = os.path.join(download_path, filename)
    if os.path.isfile(f):
        file_list.append(f)
        
files_left = len(file_list)
no_executable_count = 0

print(f"There are {files_left} files left in the directory !")
file_exe_count = 1
if file_exe_validation == yes_choice:
    for file in file_list:
        if ".exe" in str(file[0]):
            file_exe_count += 1
            os.system(file[0])
            print(f"file {file_exe_count} is executed !", end="\r")
            time.sleep(5)
        else:
            no_executable_count += 1
            print(f"Not executable files {no_executable_count}  !!", end="\r") 
            