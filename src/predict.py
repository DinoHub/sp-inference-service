from typing import Union

import torch
import librosa
import gradio as gr

from w2vlstm.lightning_model import LightningModel
from config import config, BaseConfig

''' CPU/GPU Configurations '''
if torch.cuda.is_available():
    DEVICE = [0]  # use 0th CUDA device
    ACCELERATOR = 'gpu'
else:
    DEVICE = 1
    ACCELERATOR = 'cpu'

MAP_LOCATION: str = torch.device('cuda:{}'.format(DEVICE[0]) if ACCELERATOR == 'gpu' else 'cpu')

''' Gradio Input/Output Configurations '''
inputs: Union[str, gr.Audio] = gr.Audio(source='upload', type='filepath')
outputs: gr.HighlightedText = gr.HighlightedText()

''' Helper functions '''
def initialize_sp_model(cfg: BaseConfig) -> LightningModel:

    # load the fine-tuned checkpoints
    model = LightningModel.load_from_checkpoint(cfg.sp_model_path, csv_path=cfg.labels_path)
    model = model.eval()
    return model

''' Initialize models '''
sp_model = initialize_sp_model(config)

''' Main prediction function '''
def predict(audio_path: str) -> str:

    arr, sr = librosa.load(audio_path, sr=16000, mono=True)
    tensor = torch.from_numpy(arr).unsqueeze(0)

    sample_length = config.slice_seconds * 16000
    win_length = config.slice_window * 16000

    if tensor.shape[-1] < sample_length:
        tensor = torch.nn.functional.pad(tensor, (0, sample_length - tensor.size(1)), 'constant')
        slices = tensor.unsqueeze(dim=0)
    else:
        # Split input audio into slices of input_length seconds
        slices = tensor.unfold(1, sample_length, win_length).transpose(0,1)

    # predict
    h_preds, a_preds, g_preds = [], [], []
    with torch.no_grad():
        for slice in slices:
            h_pred, a_pred, g_pred = sp_model(slice)
            h_preds.append((h_pred.view(-1) * sp_model.h_std + sp_model.h_mean).item())
            a_preds.append((a_pred.view(-1) * sp_model.a_std + sp_model.a_mean).item())
            g_preds.append(g_pred.view(-1).item())
    
    height = round(sum(h_preds)/len(h_preds),2)
    age = int(sum(a_preds)/len(a_preds))
    gender = 'Female' if sum(g_preds)/len(g_preds) > 0.5 else 'Male'

    return [(gender, 'Gender'), (height, 'Height'), (age, 'Age')]
