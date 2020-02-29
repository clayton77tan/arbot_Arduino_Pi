file1 = open("file.txt", "r")
file1.seek(0,0)
print("seek 0,0: " + file1.readline())

file1.seek(0,1)
print("seek 0,1: " + file1.readline())

file1.seek(0,2)
print("seek 0,2: " + file1.readline())

file1.close()
