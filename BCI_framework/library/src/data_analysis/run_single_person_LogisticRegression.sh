#! /bin/bash

model_class=LogisticRegression
nEpoch=30 #for fast testing purpose
train_batchSize=165 #11*15each person's train csv file contains 165 datapoints
val_batchSize=66
test_batchSize=66
eval_every_iteration=1
learningRate=3e-4
input_size=32
sequence_length=165 #each chunk contains 165 rows
num_classes=3
val_indices_option=option3
result_save_dir='/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/duijie/demo/person_specific_model_finetune_from_group/'
train_dir='/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/nature_dataset_with_column_name/processed_raw_train/'
test_dir='/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/nature_dataset_with_column_name/processed_raw_test/'
load_group_model_path='/cluster/tufts/hugheslab/zhuang12/HCI/brain_data_processing-master/hz_framework_draft3_nature_remove_redundant_features/fast_test_running/slided_window/fixedLR/raw_data/group_model/LogisticRegression/batch_4290_lr_0.001_FixedLR/group_best_model_random_seed_3.statedict'
initialized_option=No
GPU_idx="cuda:0"

python3 run_model.py $model_class $nEpoch $train_batchSize $val_batchSize $test_batchSize $eval_every_iteration $learningRate $input_size $sequence_length $num_classes $val_indices_option $result_save_dir $train_dir $test_dir $load_group_model_path $initialized_option $GPU_idx


