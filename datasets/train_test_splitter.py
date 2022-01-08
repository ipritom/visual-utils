"""
This utility script can be utilized to split dataset
where each folder represents a class.
"""


import os
from glob import glob
import shutil
import random

#Reproducability
def seed_everything(seed=0):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    os.environ['TF_DETERMINISTIC_OPS'] = '1'

seed_everything(42)




def info_parse(root_path):

    class_paths = glob(f'{root_path}/*') #get list of class folders
    class_dict = {n: os.path.basename(path) for n, path in enumerate(class_paths,0)} # dictionary for class names and numeric labels
    path_to_class = {}
    class_to_path_list = {}
    img_paths = [] #image path list

    # mapping image paths to classes
    for i in class_dict:
        # taking all image paths for class i
        temp_image_paths = glob(f'{root_path}/{class_dict[i]}/*')
        class_to_path_list[i] = temp_image_paths
        # adding paths to img_paths (total path list)
        img_paths = img_paths + temp_image_paths
        # mapping classes against paths
        for path in temp_image_paths:
            path_to_class[path] = i

    #Shuffling images in class
    for class_id, path_list in sorted(class_to_path_list.items()):
        class_to_path_list[class_id] = random.sample(path_list, len(path_list))
    
        #class,image count dict
    class_total_img_count = dict()
    for class_id in class_to_path_list:
        class_total_img_count[class_id] = len(class_to_path_list[class_id])
    

    # print(class_total_img_count)
    print("Characteristics of dataset")
    print('\nTotal Class',len(class_total_img_count),
        '\nTotal Samples',  sum(class_total_img_count.values()),
        '\nMinmum Sample Size', min(class_total_img_count.values()),
        '\nMaximum Sample Size',max(class_total_img_count.values()))

    return class_dict, path_to_class, class_to_path_list, class_total_img_count



def do_split(source_dest, train_target_dest, test_target_dest, class_to_path_list, class_dict, split_value=[1,5,10]):
    """
    Processes and return a train and test folder based dataset
        
    Parameters
    ---------------
    source_dest
    train_target_dest
    test_target_dest
    class_to_path_list
    class_dict
    split_value

    """


    # checking the existance of train and test folder
    if not os.path.isdir(train_target_dest):
        os.mkdir(train_target_dest)
    
    if not os.path.isdir(test_target_dest):
        os.mkdir(test_target_dest)


    for class_id, folder_name in class_dict.items():

        try:
            os.mkdir( os.path.join(train_target_dest, folder_name) )
            os.mkdir( os.path.join(test_target_dest, folder_name) )
        except:
            print("File or Folder already exists")
    
    #copy images to train and test based on preset values
    for class_id, path_list in class_to_path_list.items():
        # copying to test set with default split_value list
        # default split_value = [1,5,10]
        # if (total samples under a class) <  11 : copy 1 
        # elif (total samples under a class) > 10  : copy 5
        # elif (total samples under a class) > 60 : copy 10
        if (len(path_list)<11):
            
            #preset value
            value = split_value[0]
            batch_copy(value, path_list, train_target_dest, test_target_dest)

        elif (len(path_list)>10 and len(path_list)<61):

            #preset value
            value = split_value[1]
            batch_copy(value, path_list, train_target_dest, test_target_dest)

        elif (len(path_list)>60):
   
            #preset value
            value = split_value[2]
            batch_copy(value, path_list, train_target_dest, test_target_dest)


def batch_copy(value, path_list, train_target_dest, test_target_dest):
    """
    Perform Batch Copy
    """
    #copy at preset value
    for index in range(len(path_list)):
        if index < value:
            #copy to test
            shutil.copyfile(path_list[index], test_target_dest + "/" + "/".join( path_list[index].rsplit("/")[-2:] ))

        else:
            #copy to train
            shutil.copyfile(path_list[index], train_target_dest + "/" + "/".join( path_list[index].rsplit("/")[-2:] ))




if __name__ == "__main__":
    #root paths
    root_path = "/home/nybsysml/Desktop/workstation_pritom/Pritom/MaskedFaceRec/dataset/AFDB_face_dataset/AFDB_face_dataset"
    train_path = "/home/nybsysml/Desktop/workstation_pritom/Pritom/MaskedFaceRec/dataset/AFDB_face_dataset/train"
    test_path = "/home/nybsysml/Desktop/workstation_pritom/Pritom/MaskedFaceRec/dataset/AFDB_face_dataset/test"
        
    class_dict, path_to_class, class_to_path_list, class_total_img_count = info_parse(train_path)




    # do_split(root_path, train_path, test_path, class_to_path_list, class_total_img_count, class_dict)
    print("--- Train Info ---")
    class_dict, path_to_class, class_to_path_list, class_total_img_count = info_parse(train_path)
    print("--- Test Info ---")
    class_dict, path_to_class, class_to_path_list, class_total_img_count = info_parse(test_path)