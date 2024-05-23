# MRISegmentator

A package to segment 62 abdominal organs and structures on T1-weighted MR images. You can find the original publication at [https://arxiv.org/abs/2405.05944](https://arxiv.org/abs/2405.05944).

![MRISegmentator Figure 1](https://i.imgur.com/ydwPr6T.png)


## Usage instructions

Requirements: We recommend running on a computer with a GPU. This package can be run on a computer with a CPU, but it will take a very long time to process a single scan. 

Step 1: Install the package  
*We recommend you install MRISegmentator in a conda environment to avoid dependency conflicts. Note you can use any version of python that supports nnUNet v2.2 or above*

```
conda create -n MRISegmentator python=3.11
pip install MRISegmentator
```

Step 2: Download weights  
**Coming soon!**

Step 3: Run!
```
MRISegmentator -i path/to/input/mri.nii.gz -o path/to/output/segmentation.nii.gz -d gpu -m path/to/model
```

For the `-d` option, you can also provide `cpu` or `mps` as an option (cpu runs on your computer's CPU only and mps runs on M1/2 processors).

You can also run this package via importing it in a python script:

```py
from mrisegmentator.inference import mri_segmentator

input_file_path = # path to your input file /mypath/input/input.nii.gz
output_file_path = # path to where you want to segmentation to save. e.g. /mypath/result/out.nii.gz
device = # one of 'gpu', 'cpu', 'mps'
path_to_model = # path to a trained nnunet mode
mri_segmentator(input_file_path, output_file_path, device, path_to_model)
```

## Segmentation Codes

Below is a table that maps the segmentation codes to the original bodypart name

| background                   | 0  |
|------------------------------|----|
| spleen                       | 1  |
| kidney_right                 | 2  |
| kidney_left                  | 3  |
| gallbladder                  | 4  |
| liver                        | 5  |
| esophagus                    | 6  |
| stomach                      | 7  |
| aorta                        | 8  |
| inferior_vena_cava           | 9  |
| portal_vein_and_splenic_vein | 10 |
| pancreas                     | 11 |
| adrenal_gland_right          | 12 |
| adrenal_gland_left           | 13 |
| lung_right                   | 14 |
| lung_left                    | 15 |
| small_bowel                  | 16 |
| duodenum                     | 17 |
| colon                        | 18 |
| iliac_artery_left            | 19 |
| iliac_artery_right           | 20 |
| iliac_vena_left              | 21 |
| iliac_vena_right             | 22 |
| gluteus_maximus_left         | 23 |
| gluteus_maximus_right        | 24 |
| gluteus_medius_left          | 25 |
| gluteus_medius_right         | 26 |
| autochthon_left              | 27 |
| autochthon_right             | 28 |
| iliopsoas_left               | 29 |
| iliopsoas_right              | 30 |
| hip_left                     | 31 |
| hip_right                    | 32 |
| sacrum                       | 33 |
| rib_left_4                   | 34 |
| rib_left_5                   | 35 |
| rib_left_6                   | 36 |
| rib_left_7                   | 37 |
| rib_left_8                   | 38 |
| rib_left_9                   | 39 |
| rib_left_10                  | 40 |
| rib_left_11                  | 41 |
| rib_left_12                  | 42 |
| rib_right_4                  | 43 |
| rib_right_5                  | 44 |
| rib_right_6                  | 45 |
| rib_right_7                  | 46 |
| rib_right_8                  | 47 |
| rib_right_9                  | 48 |
| rib_right_10                 | 49 |
| rib_right_11                 | 50 |
| rib_right_12                 | 51 |
| vertebrae_L5                 | 52 |
| vertebrae_L4                 | 53 |
| vertebrae_L3                 | 54 |
| vertebrae_L2                 | 55 |
| vertebrae_L1                 | 56 |
| vertebrae_T12                | 57 |
| vertebrae_T11                | 58 |
| vertebrae_T10                | 59 |
| vertebrae_T9                 | 60 |
| vertebrae_T8                 | 61 |
| vertebrae_T7                 | 62 |

## Citation information

Original paper at [https://arxiv.org/abs/2405.05944](https://arxiv.org/abs/2405.05944)

```
@misc{zhuang2024mrisegmentatorabdomen,
      title={MRISegmentator-Abdomen: A Fully Automated Multi-Organ and Structure Segmentation Tool for T1-weighted Abdominal MRI}, 
      author={Yan Zhuang and Tejas Sudharshan Mathai and Pritam Mukherjee and Brandon Khoury and Boah Kim and Benjamin Hou and Nusrat Rabbee and Ronald M. Summers},
      year={2024},
      eprint={2405.05944},
      archivePrefix={arXiv},
      primaryClass={eess.IV}
}
```

Also please consider citing nnUNet as this work uses their library to train our segmentation algorithm [https://github.com/MIC-DKFZ/nnUNet](https://github.com/MIC-DKFZ/nnUNet)