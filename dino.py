import os
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModel

# Load the pre-trained processor and model
processor = AutoImageProcessor.from_pretrained('facebook/dinov2-base')
model = AutoModel.from_pretrained('facebook/dinov2-base')

# Define the directory containing images
img_dir = './selected_images'

# List and sort images, excluding specified files
exclude_files = {'demon.png', 'pfode.png', 'ref.jpg'}
imgs = [img for img in os.listdir(img_dir) if img not in exclude_files]
imgs.sort(key=lambda x: (int(x.split('_')[0]), int(x.split('_')[1])))

@torch.inference_mode()
def get_dinov2_embeddings(images):
    """
    Computes embeddings for a list of images using the DINOv2 model.
    """
    inputs = processor(images=images, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

# Load the reference image and compute its embeddings
ref_img_path = os.path.join(img_dir, 'ref.jpg')
ref_img = Image.open(ref_img_path)
ref_emb = get_dinov2_embeddings(ref_img)

# Load special images and compute their embeddings
special_images = ['pfode.png', 'demon.png']
special_imgs = [Image.open(os.path.join(img_dir, img)) for img in special_images]
special_embs = get_dinov2_embeddings(special_imgs)

# Compute cosine similarities between the reference and special images
sims = torch.nn.functional.cosine_similarity(ref_emb, special_embs, dim=1)
print(f"Original: {sims[0].item():.4f}, Final: {sims[1].item():.4f}")

# Process images in batches and compute similarities
batch_size = 16
for i in range(0, len(imgs), batch_size):
    batch_imgs = [Image.open(os.path.join(img_dir, img)) for img in imgs[i:i + batch_size]]
    batch_embs = get_dinov2_embeddings(batch_imgs)
    sims = torch.nn.functional.cosine_similarity(ref_emb, batch_embs, dim=1)
    print(f"{sims.mean().item():.4f} ± {sims.std().item():.4f}")
