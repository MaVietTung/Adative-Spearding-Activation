import os

dirname = os.path.dirname(__file__)

BX_path = os.path.join(os.path.join(dirname, 'data'), 'BX')
BX_similarities = os.path.join(BX_path, 'data_matrix_similarities')

GB_path = os.path.join(os.path.join(dirname, 'data'), 'GB')
GB_similarities = os.path.join(GB_path, 'data_matrix_similarities')

epochs = 2
n_preds = 10
# threshold = 0.3
# cnt_threshold = 2
