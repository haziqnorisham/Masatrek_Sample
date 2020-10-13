import re
import subprocess

subprocess.check_output([r'C:\MyKad_Reader\SDK_App\automatic_reader.bat'])
file = open('C:\\MyKad_Reader\\SDK_App\\output.txt', 'r')
content = file.readlines()

for line in content:
    
    ic = "IC:"
    do_print = True
    
    for i, char in enumerate(ic):        
        try:
            if line[i] == char:
                pass
            else:
                do_print = False
        except Exception as e:
            pass
        
    if "Name:" in line:
        print(repr(line))
        colon_loc = line.find(':')        
        line_split = line.split()
        name = ''
        for parts in line_split:
            if parts == "Name:":
                pass
            else:
                name = name + parts + " "

        print(name)
        
    if do_print is True:
        print()
        print(repr(line))
        line_split = line.split()
        name = ''
        for parts in line_split:
            if parts == "IC:":
                pass
            else:
                name = name + parts + " "

        print(name)
