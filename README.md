# code_for_UIST
use command: "python3 main.py" to run the program.

## 3phase_code
### Environment requirement
#### Python3
#### PyTorch
#### pandas
#### numpy
#### glob
### brain_data.py
please set the local path for fNIRS brain data here.

### main.py

In line 248-250, you can choose "allphases" to run all 3phase models, or "last2phases" to run on phase2 and phase3 models, or "baseline" to run on only phase3 model.

In line 256-258, you can choose load full or half of the training data.

In line 266-270, you can choose to run binary classification or 4-class classification.

### train_phase1_model.py
Please check comments inside the file.
### train_phase2_model.py
Please check comments inside the file.
### train_phase3_model.py
Please check comments inside the file.
### utils.py
Some functions here, including MixUp.
### models.py
we have two models here: LR and CNN.

## BCI_framework
use command "python3 run_app.py" to start the system.

### Front-end Environment requirement
#### VUE
#### YARN

Go to folder "web" in terminal, input "yarn" to install dependencies.

Then "yarn build" to generate related html files.

### Back-end Environment requirement
#### Python3
#### Use "pip3 install requirement.txt" to install all dependencies.

