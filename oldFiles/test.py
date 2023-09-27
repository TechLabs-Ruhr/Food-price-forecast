from os.path import dirname, join
current_dir = dirname(__file__)
file_path = join(current_dir, "./test.txt")
with open(file_path, 'r') as f