import numpy as np
import cv2

def simple_poison(image, epsilon):
    noise = np.random.uniform(low=-epsilon, high=epsilon, size=image.shape)
    noisy_image = image + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    return noisy_image

if __name__ == "__main__":
    img = cv2.imread('image.jpg')
    poisoned_image = simple_poison(img, epsilon = 10)
    cv2.imshow('image', img)
    cv2.imshow('poisoned_image', poisoned_image)
    cv2.waitKey(0)