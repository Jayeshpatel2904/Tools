import glob
import os
import shutil

folderpath = r"C:\Users\jayeshkumar.patel\Downloads\Quiz_120question_2.jpg"
Rename_dir = folderpath + "\Moved"


isExist1 = os.path.exists(Rename_dir)


if not isExist1:
    # Create a new directory because it does not exist 
    os.makedirs(Rename_dir)



AOF = glob.glob(folderpath + "\*.jpg")


def filterdata():
		for file in AOF:
			# print(file)
			filename = os.path.basename(file)
			print(filename)
			# filename = filename.replace("Post", "Pre")
			# print(filename)

			x = filename.split("-")
			print(x)
			if len(x[1]) == 5:

				x = "File_00" + x[1]
			elif len(x[1]) == 6:
				x = "File_0" + x[1]
			else:
				x = "File_" + x[1]

			
			print(x)
			shutil.copyfile(file, Rename_dir + '/' + x)
   

filterdata()		