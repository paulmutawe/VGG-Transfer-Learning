import os

def mkdir(p):
  if not os.path.exists(p):
    os.mkdir(p)

def link(src, dst):
  if not os.path.exists(dst):
    os.symlink(src, dst, target_is_directory=True)

mkdir('/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-small')


classes = [
  'apple_golden_1',
  'zucchini_1',
  'carrot_1',
]

train_path_from = os.path.abspath('/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-original-size/Training')
valid_path_from = os.path.abspath('/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-original-size/Validation')

train_path_to = os.path.abspath('/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-small/Training')
valid_path_to = os.path.abspath('/Users/paulmutawe/Downloads/archive (2)/fruits-360_dataset_original-size/fruits-360-small/Validation')

mkdir(train_path_to)
mkdir(valid_path_to)


for c in classes:
  link(train_path_from + '/' + c, train_path_to + '/' + c)
  link(valid_path_from + '/' + c, valid_path_to + '/' + c)