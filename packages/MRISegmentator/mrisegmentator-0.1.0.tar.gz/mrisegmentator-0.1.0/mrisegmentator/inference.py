import torch
from batchgenerators.utilities.file_and_folder_operations import join
from nnunetv2.inference.predict_from_raw_data import nnUNetPredictor
import os


def mri_segmentator(input_file, output_file, device='gpu', path_to_model='nnUNetTrainer__nnUNetPlans__3d_fullres'):
    if input_file.find('.nii.gz') == -1:
        raise ValueError("invalid file type: must have .nii.gz in filename")
    if os.path.exists(input_file) == False:
        raise ValueError("path to input file must exist")
        
    if device == 'gpu':
        device = torch.device('cuda')
    elif device == 'cpu':
        device = torch.device('cpu')
    elif device == 'mps':
        device = torch.device('mps')
    else:
        raise ValueError("invalid device: must be one of 'gpu', 'cpu', or 'mps'")

    if not os.path.isdir(path_to_model):
        raise ValueError("invalid path to trained model folder")
     
    print("Instantiating nnunet predictor...")
    predictor = nnUNetPredictor(
        tile_step_size=0.5,
        use_gaussian=True,
        use_mirroring=True,
        perform_everything_on_device=True,
        device=device,
        verbose=False,
        verbose_preprocessing=False,
        allow_tqdm=True
    )

   
    print("Instantiating trained model...")
    predictor.initialize_from_trained_model_folder(
        path_to_model,
        use_folds=(0,1,2,3,4),
        checkpoint_name='checkpoint_final.pth',
    )

    print("Starting prediction...")
    return predictor.predict_from_files([[input_file]],
         [output_file],
         save_probabilities=False, overwrite=False,
         num_processes_preprocessing=1, num_processes_segmentation_export=1,
         folder_with_segs_from_prev_stage=None, num_parts=1, part_id=0)
    print("DONE!")





