import os
#######Create Folder###########
os.system("mkdir -p testfiles")
#######Create Files###########
for i in range(45):
    with open("testfiles/file_%s.txt" %i, 'w+') as file:
        file.write('hello')
        os.system("cnvrg sync")
#######Create YAML files###########
#     with open("testfiles/file_%s.txt_tags.yml" %i, 'w+') as yml:
#         yml.write("""---
# id: \"%s\"
# source: \"yann lecun\"
# """ %i)
#######Upload file to cnvrg###########
#os.system("cnvrg data put dataset_name testfiles/")
#######delete file from local###########
#os.system("rm -rf testfiles")
