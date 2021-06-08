#! /bin/bash

model_class=CNN
nEpoch=10 
train_batchSize=165
val_batchSize=66
test_batchSize=66
eval_every_iteration=5
learningRate=1e-2
input_size=45
sequence_length=10
conv1d_hidden_size=32
window_size=5
window_stride=1
linear_hidden_size=36
num_classes=3

val_indices_option=option4

result_save_dir='../../storage/experiment/analyzed_data/exp_0/sub_0'
train_dir='../../storage/experiment/slide_window_data/exp_0/sub_0'
test_dir='../../storage/experiment/slide_window_data/exp_0/sub_0'

# set it later
initialized_option=No
load_group_model_path='/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/hz_framework_draft2_nature/fast_test_running/slided_window/group_model/CNN/group_best_model_random_seed_0.statedict'

GPU_idx="cuda:0"

python3 run_model.py $model_class $nEpoch $train_batchSize $val_batchSize $test_batchSize $eval_every_iteration $learningRate $input_size $sequence_length $conv1d_hidden_size $window_size $window_stride $linear_hidden_size $num_classes $val_indices_option $result_save_dir $train_dir $test_dir $load_group_model_path $initialized_option $GPU_idx


