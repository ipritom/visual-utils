# Datasets

## Train-Test Split

To split a dataset where each folder represents a class `train_test_splitter.py` can be utilized. 

NOTE: This script creates another copy of the dataset distributed into two folders. While working with a larger datset this approach may not be efficient.

Example: 
Example is show for [BanglaLekha Isolated](https://data.mendeley.com/datasets/hf6sf8zrkc/2) dataset. 

```python
import train_test_splitter as tts

root_path = "dataset/BanglaLekha-Isolated/Images"
train_path = "dataset/train"
test_path = "dataset/test"

# parsing info on the whole datset
class_dict, path_to_class, class_to_path_list, class_total_img_count = tts.info_parse(root_path)

# splitting the dataset
tts.do_split(root_path, train_path, test_path, class_to_path_list, class_dict)

# parsing info on the splitted dataset
print("--- Train Info ---")
_, _, _, _ = tts.info_parse(train_path)
print("--- Test Info ---")
_, _, _, _ = tts.info_parse(test_path)
```

Output:
```terminal

Total Class 84 
Total Samples 166105 
Minmum Sample Size 1940 
Maximum Sample Size 1988
(mlExp) pritom@ipritom:~/Desktop/workstation/PyTorch_BanglaLekhaIsolated$ python example_train_test_split.py 
Traceback (most recent call last):
  File "/home/pritom/Desktop/workstation/PyTorch_BanglaLekhaIsolated/example_train_test_split.py", line 1, in <module>
    import train_test_splitter as tts
  File "/home/pritom/Desktop/workstation/PyTorch_BanglaLekhaIsolated/train_test_splitter.py", line 85
    if not os.path.isdirtrain_target_dest):
                                         ^
SyntaxError: unmatched ')'
(mlExp) pritom@ipritom:~/Desktop/workstation/PyTorch_BanglaLekhaIsolated$ python example_train_test_split.py 
Characteristics of dataset

Total Class 84 
Total Samples 166105 
Minmum Sample Size 1940 
Maximum Sample Size 1988
--- Train Info ---
Characteristics of dataset

Total Class 84 
Total Samples 165265 
Minmum Sample Size 1930 
Maximum Sample Size 1978
--- Test Info ---
Characteristics of dataset

Total Class 84 
Total Samples 840 
Minmum Sample Size 10 
Maximum Sample Size 10
```

