import os
CURRENT_WORKING_DIRECTORY = os.getcwd()
#print(CURRENT_WORKING_DIRECTORY)

DATASETS_PATH = CURRENT_WORKING_DIRECTORY + "\Datasets\\"
OUTPUT_FILE_PATH = CURRENT_WORKING_DIRECTORY + "\Files\\"
MANUAL_LABLED_ASPECT_PATH = OUTPUT_FILE_PATH + "\manual_labeled_aspects\\"
STANDFORD_POS_TAGGER_PATH = CURRENT_WORKING_DIRECTORY + "\stanford-postagger-full-2017-06-09\\"
LEXICONS_PATH = CURRENT_WORKING_DIRECTORY + "\opinion-lexicon-English\\"

# java path
JAVA_PATH = "C:\\Program Files\\Java\\jdk1.8.0_151\\bin\\java.exe"
os.environ['JAVAHOME'] = JAVA_PATH
#print(Output_file_path)