import os
import time
start_time = time.time()
os.system("mkdir -p testfilenews")
i=1
while time.time() <= start_time + 300: 
    with open("testfilenews/file_%s.txt" %i, 'w+') as file:
        file.write('hello rohit')

    i= i+1
print("script finised")
