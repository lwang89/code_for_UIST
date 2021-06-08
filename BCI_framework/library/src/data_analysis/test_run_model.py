from run_model import run, predict_chunk_test_data
from brain_data import read_data_single, personal_test_brain_data

#! /bin/bash
def run_model():
    param_dict = dict()

    #################### Common Parameters ####################
    param_dict["model_class"] = "CNN"
    param_dict["n_epoch"] = 10 
    param_dict["train_batch_size"] = 165
    param_dict["val_batch_size"] = 66
    # param_dict["test_batch_size"] = 66
    param_dict["test_batch_size"] = 1
    param_dict["eval_every_iteration"] = 5
    param_dict["learning_rate"] = float(1e-2)
    param_dict["input_size"] = 45
    param_dict["sequence_length"] = 10
    param_dict["num_classes"] = 3
    param_dict["val_indices_option"] = "option4"

    param_dict["load_mode"] = "personal"
    param_dict["result_save_dir"] = '../../storage/experiment/analyzed_data/exp_0/sub_0'
    param_dict["train_dir"] = '../../storage/experiment/slide_window_data/exp_0/sub_0'
    param_dict["test_dir"] = '../../storage/experiment/slide_window_data/exp_0/sub_0'

    param_dict["train_files"] = ['muse_train_10_4.csv']
    param_dict["test_files"] = ['muse_test_10_4.csv']

    # set it later
    param_dict["initialized"] = False
    param_dict["load_group_model_path"] = '/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/hz_framework_draft2_nature/fast_test_running/slided_window/group_model/CNN/group_best_model_random_seed_0.statedict'

    param_dict["gpu_index"] = "cuda:0"

    #################### Model Specific Parameters ####################
    param_dict["conv1d_hidden_size"] = 32
    param_dict["window_size"] = 5
    param_dict["window_stride"] = 1
    param_dict["linear_hidden_size"] = 36


    people_best_models = run(param_dict)
    print("Number of models: {}".format(len(people_best_models)))
    print("Get trained models!")
    person_index = 0


    test_file_path = param_dict["test_dir"] + "/" + param_dict["test_files"][0]

    chunk_test_np_array, test_chunk_labels = read_data_single(test_file_path)

    print(type(chunk_test_np_array))
    print(chunk_test_np_array.shape)

    chunk_test_np_array = chunk_test_np_array[:1]

    print(type(chunk_test_np_array))
    print(chunk_test_np_array.shape)
    print(chunk_test_np_array)

    test_set = personal_test_brain_data(chunk_test_np_array)
    print("************** wrapped object ******************")
    print(test_set)

    predicted_label = predict_chunk_test_data(test_set, people_best_models, person_index, param_dict)
    print("Predicted test chunk label: {}".format(predicted_label))

if __name__ == '__main__':
    run_model()