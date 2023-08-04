#!/usr/bin/python3

import csv
import os
import wget
import requests

file_exe_validation = input("please say Yes or No in uppercase Letters to automatic executing the samples: ")
vali_choices = ["NO","YES"]

while file_exe_validation not in vali_choices:
    file_exe_validation = input("please say Yes or No in uppercase Letters to automatic executing the samples: ")


csv_file = input("please set the path to csv file: ")
csv_validation = False
line = 0

while os.path.isfile(csv_file) == False and ".csv" not in csv_file:
   csv_file = input("please set the path to csv file again !: ")

if os.path.isfile(csv_file) == True:

    with open (csv_file, mode = 'r') as file:
        csv_file_true_parser = csv.reader(file)
        csv_list_parser = list(csv_file_true_parser)
        error_count = 0
        
        for url_list_parser_vali in csv_list_parser:
            if "http" in url_list_parser_vali[0]:
                line += 1
            else:
                csv_validation = False
                line += 1
                error_count += 1
                print(f"The csv file has error in Line {line} please check it !")
        
        if error_count > 0:
            quit()
current_path = str(os.path.dirname(os.path.realpath(__file__))) + "/"
dir_name = "Samples"

if os.path.isdir(current_path + dir_name) != True:
    dir_path = os.path.join(current_path, dir_name)
    dir_mode = 0o777
    os.mkdir(dir_path, dir_mode)

download_path = str(current_path) + "Samples/"

with open (csv_file, mode = 'r') as file:
    csvFile = csv.reader(file)
    csv_list = list(csvFile)

for url_list in csv_list:
    x = requests.get(url_list[0])
    if x.status_code == 200 :
        wget.download(url_list[0], download_path)
    else: 
        print("\n########## Url isn't available ! ##########")

#################### File Counter wie viele datei noch da sind von den Samples ####################################

###################################################################################################################


yes_choice = "YES"
no_choice = "NO"
file_list = []

if file_exe_validation == yes_choice:
    for filename in os.listdir(download_path):
        f = os.path.join(download_path, filename)
        if os.path.isfile(f):
            file_list.append(f)
else:
    print("Stop")

print(file_list)
