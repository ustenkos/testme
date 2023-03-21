import os
#######Create Folder###########
os.system("mkdir -p testfiles")
#######Create Files###########
for i in range(45):
    with open("testfiles/file_%s.txt" %i, 'w+') as file:
        file.write('hello')
