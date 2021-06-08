#usage:
#from: Jan_stage2_Embedding/BreastScreening/code/utilities/logger.py
#Jan_stage2_Embedding/BreastScreening/code/patch_classification/patch_model/patch_classification_2stage_V4.py

#1. import the module: import hz_logger as logger
#2. create the logger object: logger = logger.logger(model_saves_directory, log_file_name)
#3. log information: logger.log('dimension of embed_returned is {}'.format(numpy.array(embed_returned).shape))
#4. immediate flush if wished: logger.flush()
#5. Can log traceback info as flowing example:

# try:
#         start_time = time.time()
#         main(parameters, logger, model_saves_directory)
#         end_time = time.time()
#         logger.log('elapsed time is {}'.format(end_time-start_time))

#     except:
#         tb = traceback.format_exc()
#         logger.log(tb)
#         logger.flush()


import os
import sys
import subprocess

# The reason why it is beneficial to accumulate text to log and actually write it only once in a while is that writing
# to a network file system is slow, even for small amounts of data.


class logger:
	def __init__(self, log_file_directory, log_file_name, buffer_size=100000):

		self.buffer_size = buffer_size
		self.text_to_log = ''	

		os.makedirs(log_file_directory, exist_ok=True)

		log_file_path = os.path.join(log_file_directory, log_file_name)

		if not os.path.exists(log_file_path):
			print('Creating the log file at:', log_file_path)
		else:
			print('Log file at:', log_file_path, 'already exists. Appending to the existing file.')

		self.log_file = open(log_file_path, 'a')

	def __del__(self):

		if not self.log_file.closed:
			self.log_file.write(self.text_to_log)
			self.log_file.close()

	def log(self, string_to_log, log_log=True, print_log=False, no_enter=False):

		end_of_line = '' if no_enter else '\n'

		if log_log:
			self.text_to_log += string_to_log + end_of_line

			if len(self.text_to_log) > self.buffer_size:
				self.log_file.write(self.text_to_log)
				self.text_to_log = ''

		if print_log:
			print(string_to_log, end=end_of_line)

	def flush(self):
		self.log_file.write(self.text_to_log)
		self.text_to_log = ''
		self.log_file.flush()
		os.fsync(self.log_file.fileno())

	def close(self):

		self.log_file.write(self.text_to_log)
		self.log_file.close()


class PrintLogger:
	def log(self, string_to_log, log_log=True, print_log=True, no_enter=False):
		sep = "" if no_enter else "\n"
		print(string_to_log, sep=sep)

	def flush(self):
		sys.stdout.flush()

	def close(self):
		pass


class SilentLogger:
	def log(self, string_to_log, log_log=True, print_log=True, no_enter=False):
		pass

	def flush(self):
		pass

	def close(self):
		pass


def common_log_initialization(logger_, parameters):
	# log experiment settings
	logger_.log('')
	for parameter, value in parameters.items():
		logger_.log(parameter + ': ' + str(value))
	logger_.log('')

	# log hostname
	host_name = subprocess.check_output(['hostname'])
	logger_.log("running on host {0}".format(host_name.strip()))
