import os, sys, torch,random
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import cm
from torchvision import transforms
import cv2
import site

site_packages_dir = site.getusersitepackages()
clone_path = os.path.join(site_packages_dir, 'ArtSnake', 'deep-blind-watermark-removal')
sys.path.append(clone_path)
sys.path.insert(0, clone_path)

from scripts.utils.imutils import im_to_numpy
import scripts.models as models
from PIL import Image, ImageChops

def seed_everything(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

seed_everything(18)

site_packages_dir = site.getusersitepackages()
zip_path = os.path.join(site_packages_dir, 'ArtSnake')
resume_name = '27kpng_model_best.pth.tar'
resume_path = os.path.join(zip_path, resume_name)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model():
      model = models.__dict__['vvv4n']().to(device)
      model.load_state_dict(torch.load(resume_path, map_location=device)['state_dict'])
      model.eval()
      return model
    
def load_transform(size):
      trans = transforms.Compose([
            transforms.Resize(size),
            transforms.ToTensor(),
            lambda x: x.unsqueeze(0)
            ])
      return trans
      
def remove_watermark_from_dir(image_dir, model = None, trans = None, trans_size_default_model = (256, 256)):
      if model is None:
            model = load_model()
      if trans is None:
            trans = load_transform(trans_size_default_model)
      results = []
      with torch.no_grad():
            for image_name in os.listdir(image_dir):
                  if not image_name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        raise Exception("Error")
                  image_path = os.path.join(image_dir, image_name)
                  ims1 = remove_watermark(image_path, model, trans)
                  results.append(ims1)
            return results

def remove_watermark(image_path, model = None, trans = None, trans_size_default_model = (256, 256)):
      if model is None:
            model = load_model()
      if trans is None:
            trans = load_transform(trans_size_default_model)
      if not image_path.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            raise Exception("Error")
      with torch.no_grad():      
            image = Image.open(image_path).convert('RGB')
            transformed_image = trans(image).to(device)
            imoutput,immask,_ = model(transformed_image)
            imrefine = imoutput[0]*immask + transformed_image*(1-immask)
            ims1 = im_to_numpy(torch.clamp(torch.cat([imrefine],dim=3)[0]*255,min=0.0,max=255.0)).astype(np.uint8)
            ims1 = cv2.cvtColor(ims1, cv2.COLOR_RGB2BGR)
            return ims1


if __name__ == '__main__':
      image_path = "example.jpg"
      result = remove_watermark(image_path)
      cv2.imshow("result", result)
      cv2.waitKey(0)
      cv2.destroyAllWindows()
