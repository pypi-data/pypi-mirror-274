from src.experiment_helpers.training import train_pipeline
from PIL import Image
from accelerate import Accelerator
from diffusers import StableDiffusionPipeline
from diffusers.models import AutoencoderKL
import torch
from accelerate import Accelerator
from random import randint
from PIL import Image
from torchvision.transforms import PILToTensor
from transformers import CLIPImageProcessor, CLIPTextModel, CLIPTokenizer, CLIPVisionModelWithProjection
import torch.nn.functional as F
from tqdm.auto import tqdm
from peft import LoraConfig, get_peft_model

def basic_test():
    accelerator=Accelerator(log_with="wandb",gradient_accumulation_steps=4)
    accelerator.init_trackers(project_name="testing_bullshit")
    pipeline=StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
    img=Image.open("ArcaneJinx.jpg").convert("RGB").crop((0,0,64,64)).resize((512,512))
    for model in [pipeline.text_encoder, pipeline.vae,pipeline.unet]:
        model.eval()
        model.requires_grad_(False)
    config = LoraConfig(
            r=4,
            lora_alpha=16,
            target_modules=["to_k", "to_q", "to_v", "to_out.0"],
            lora_dropout=0.0,
            bias="none")
    pipeline.unet = get_peft_model(pipeline.unet, config)

