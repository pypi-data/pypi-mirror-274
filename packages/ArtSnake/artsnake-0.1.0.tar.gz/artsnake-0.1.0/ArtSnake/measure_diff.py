import cv2
import numpy as np

def make_same_shape(img1, img2):
    if img1.shape != img2.shape:
        img1 = cv2.resize(img1, (min(img1.shape[1], img2.shape[1]), min(img1.shape[0], img2.shape[0])))
        img2 = cv2.resize(img2, (min(img1.shape[1], img2.shape[1]), min(img1.shape[0], img2.shape[0])))
    return img1, img2

def measure_diff_simple(img1, img2, show_diff=False):
    subtracted = cv2.subtract(img1, img2)
    diff = sum(cv2.sumElems(subtracted))
    diff_norm = diff / (img1.shape[0] * img1.shape[1] * 255 * 3) * 100
    if show_diff:
        cv2.imshow('subtracted', subtracted)
        print(f'Difference: {diff_norm}%')
    return diff

def measure_similarity_psnr(img1, img2, show_diff=False):
    # Peak Signal-to-Noise Ratio
    diff = cv2.absdiff(img1, img2)
    mse = np.mean((img1 - img2) ** 2)
    psnr = 10 * np.log10(255 * 255 / mse)
    if show_diff:
        cv2.imshow('diff', diff)
        print(f'PSNR: {psnr:.2f}')
    return psnr

def measure_similarity_ssim(img1, img2, show_similarity=False):
    # Structural Similarity
    img1 = np.clip(img1, 0, 255).astype(np.uint8)
    img2 = np.clip(img2, 0, 255).astype(np.uint8)
    if len(img1.shape) == 3:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    if len(img2.shape) == 3:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    mu1 = cv2.GaussianBlur(img1, (11, 11), 1.5)
    mu2 = cv2.GaussianBlur(img2, (11, 11), 1.5)
    sigma1_sq = cv2.GaussianBlur(img1 * img1, (11, 11), 1.5) - mu1 * mu1
    sigma2_sq = cv2.GaussianBlur(img2 * img2, (11, 11), 1.5) - mu2 * mu2
    sigma12 = cv2.GaussianBlur(img1 * img2, (11, 11), 1.5) - mu1 * mu2
    C1 = (0.01 * 255) ** 2
    C2 = (0.03 * 255) ** 2
    ssim_map = ((2 * mu1 * mu2 + C1) * (2 * sigma12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) * (sigma1_sq + sigma2_sq + C2))
    ssim_map = np.clip(ssim_map, -1, 1)
    ssim_value = ssim_map.mean()
    if show_similarity:
        print(f'SSIM: {ssim_value:.2f}')
    return ssim_value


if __name__ == '__main__':
    img1 = cv2.imread('example.jpg')
    img2 = cv2.imread('example2.jpg')
    img1, img2 = make_same_shape(img1, img2)
    measure_diff_simple(img1, img2, show_diff=True)
    measure_similarity_psnr(img1, img2, show_diff=True)
    measure_similarity_ssim(img1, img2, show_similarity=True)
    cv2.waitKey(0)
    cv2.destroyAllWindows()