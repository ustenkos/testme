import uuid
uuid = str(uuid.uuid4())
f = open("{}.txt".format(uuid), "a")
f.write("Now the file has more content! {}".format(uuid))
f.close()
