import os
import argparse
import timm
import site
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms as T

# Define preprocessing transformations
preprocessing = T.Compose([
    T.Resize((256, 256)),
    T.ToTensor(),
    T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def load_prebuilt_model():
    """
    Load prebuilt watermark model
    """
    model = timm.create_model('efficientnet_b3a', pretrained=True, num_classes=2)
    model.classifier = nn.Sequential(
        nn.Linear(in_features=1536, out_features=625),
        nn.ReLU(),
        nn.Dropout(p=0.3),
        nn.Linear(in_features=625, out_features=256),
        nn.ReLU(),
        nn.Linear(in_features=256, out_features=2),
    )
    site_packages_dir = site.getusersitepackages()
    zip_path = os.path.join(site_packages_dir, 'ArtSnake')
    resume_name = 'watermark_model_v1.pt'
    model_path = os.path.join(zip_path, resume_name)
    state_dict = torch.load(model_path)
    model.load_state_dict(state_dict)
    model.eval()
    return model

_PRE_BUILT_WATERMARK_DETECTION_MODEL = load_prebuilt_model()


def predict_image(image_path, model=_PRE_BUILT_WATERMARK_DETECTION_MODEL):
    """
    Returns the probability of an image being a watermarked.\n
    The function assumes that the input image is preprocessed and formatted as a PyTorch tensor.\n
    The function assumes that the model's forward pass returns a tensor containing raw logits or scores.
    """
    # Load the image and apply preprocessing
    img = preprocessing(Image.open(image_path).convert('RGB'))
    batch = torch.stack([img])

    # Use GPU if available
    if torch.cuda.is_available():
        model.cuda()
        batch = batch.cuda()

    # Perform prediction
    with torch.no_grad():
        pred = model(batch)
        syms = F.softmax(pred, dim=1).detach().cpu().numpy().tolist()
        for sym in syms:
            water_sym, clear_sym = sym
            if water_sym > clear_sym:
                print(f"{image_path}: Watermarked, probability: {water_sym}")
            else:
                print(f"{image_path}: Clear, probability: {clear_sym}")
    return water_sym


def predict_images(model, directory):
    """
    Returns the probability of an image being a watermarked.
    The function assumes that the input image is preprocessed and formatted as a PyTorch tensor.
    The function assumes that the model's forward pass returns a tensor containing raw logits or scores.
    """
    # Predict images in the specified directory
    for filename in os.listdir(directory):
        image_path = os.path.join(directory, filename)
        if os.path.isfile(image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            predict_image(model, image_path)

if __name__ == '__main__':
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Detect watermark in images')
    parser.add_argument('directory', metavar='directory_path', type=str, help='path to the directory containing images')
    args = parser.parse_args()

    # Load the model
    model = load_prebuilt_model()

    # Perform prediction on images in the specified directory
    predict_images(model, args.directory)
