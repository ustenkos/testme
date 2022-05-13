import os
#######Create Folder###########
os.system("mkdir -p testfiles")
#######Create Files###########
for i in range(200):
   with open("testfiles/file_%s.txt" %i, 'w+') as file:
       file.write('hello')
       os.system("cnvrg sync")
print("execution completed")