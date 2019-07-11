
import os

for i in range(7):
    i+=1
    os.system("python output_las_class.py las_files/Maynooth.las maynooth_%i.las --pointclass %i" %(i,i)
