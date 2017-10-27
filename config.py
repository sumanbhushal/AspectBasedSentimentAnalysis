import os
currentWorkingDirectory = os.getcwd()
#print(currentWorkingDirectory)

Datasets_path = currentWorkingDirectory+"\Datasets\\"
Output_file_path = currentWorkingDirectory+"\Files\\"
Stanford_POS_Tagger_Path = currentWorkingDirectory + "\stanford-postagger-full-2017-06-09\\"

# java path
java_path = "C:\\Program Files\\Java\\jdk1.8.0_151\\bin\\java.exe"
os.environ['JAVAHOME'] = java_path
#print(Output_file_path)