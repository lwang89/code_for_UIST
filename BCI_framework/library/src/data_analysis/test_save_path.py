import os
import torch

def create_local_file(train_dir, test_dir, result_save_dir):
    print("\n****************************************************")

    print("test to create files for ML")

    path_list = [train_dir, test_dir, result_save_dir]

    for dir_path in path_list:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print("create ---- " + dir_path)

        else:
            print("already exists ---- " + dir_path)

    print("\n****************************************************")
    pass