'''
#raw_data_path = "../../../storage/raw_data/muse.csv"
raw_data_path = "muse.txt"
open_file_mode = "a"

file = open(raw_data_path, open_file_mode)
file.write("xxxxxxxxxxxx")
file.close()
'''
'''
from pathlib import Path

open_file_mode = "a"
raw_data_path = Path(__file__).parent / "../../../storage/raw_data/muse.csv"
with open(raw_data_path, open_file_mode) as file:
    file.write("xxxxxxxxxxxx")
'''

'''
import csv
with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "Name", "Contribution"])
    writer.writerow([1, "Linus Torvalds", "Linux Kernel"])
    writer.writerow([2, "Tim Berners-Lee", "World Wide Web"])
    writer.writerow([3, "Guido van Rossum", "Python Programming"])
'''
a = [1,2,3]
b = [4,5,6]
c = a + b
print(c)