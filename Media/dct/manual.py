import numpy as np
import cv2
import pywt
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
from simple import calculate_psnr
import argparse

def dct_manual(block):
    N = block.shape[0]
    dct_result = np.zeros_like(block, dtype=np.float32)
    alpha = lambda x: 1 / np.sqrt(2) if x == 0 else 1

    for u in range(N):
        for v in range(N):
            sum = 0
            for x in range(N):
                for y in range(N):
                    sum += block[x, y] * np.cos(((2 * x + 1) * u * np.pi) / (2 * N)) * np.cos(((2 * y + 1) * v * np.pi) / (2 * N))
            dct_result[u, v] = 0.25 * alpha(u) * alpha(v) * sum
    return dct_result

def idct_manual(block):
    N = block.shape[0]
    idct_result = np.zeros_like(block, dtype=np.float32)
    alpha = lambda x: 1 / np.sqrt(2) if x == 0 else 1

    for x in range(N):
        for y in range(N):
            sum = 0
            for u in range(N):
                for v in range(N):
                    sum += alpha(u) * alpha(v) * block[u, v] * np.cos(((2 * x + 1) * u * np.pi) / (2 * N)) * np.cos(((2 * y + 1) * v * np.pi) / (2 * N))
            idct_result[x, y] = 0.25 * sum
    return np.clip(idct_result, 0, 255)

def dwt_haar_manual(image):
    image = image.astype(np.float32)

    height, width = image.shape
    LL = np.zeros((height // 2, width // 2))
    LH = np.zeros((height // 2, width // 2))
    HL = np.zeros((height // 2, width // 2))
    HH = np.zeros((height // 2, width // 2))
    
    for i in range(0, height, 2):
        for j in range(0, width, 2):
            a = image[i, j]
            b = image[i, j + 1]
            c = image[i + 1, j]
            d = image[i + 1, j + 1]
            
            LL[i // 2, j // 2] = (a + b + c + d) / 4
            LH[i // 2, j // 2] = (a - b + c - d) / 4
            HL[i // 2, j // 2] = (a + b - c - d) / 4
            HH[i // 2, j // 2] = (a - b - c + d) / 4

    return LL, LH, HL, HH

def idwt_haar_manual(LL, LH, HL, HH):
    height, width = LL.shape
    reconstructed = np.zeros((height * 2, width * 2), dtype=np.float32)



    for i in range(height):
        for j in range(width):
            a = LL[i, j] + LH[i, j] + HL[i, j] + HH[i, j]
            b = LL[i, j] - LH[i, j] + HL[i, j] - HH[i, j]
            c = LL[i, j] + LH[i, j] - HL[i, j] - HH[i, j]
            d = LL[i, j] - LH[i, j] - HL[i, j] + HH[i, j]
            
            reconstructed[i * 2, j * 2] = a
            reconstructed[i * 2, j * 2 + 1] = b
            reconstructed[i * 2 + 1, j * 2] = c
            reconstructed[i * 2 + 1, j * 2 + 1] = d

    return np.clip(reconstructed, 0, 255).astype(np.uint8)



if __name__ == '__main__':
    

    parser = argparse.ArgumentParser()    

    parser.add_argument("-i", help="Path to the input image.")
    args = parser.parse_args()  

    # Load image
    image = cv2.imread(args.i, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (512, 512))

    # Save original image
    cv2.imwrite('original_image.png', image)


    block_size = 8
    height, width = image.shape
    compressed_dct = np.zeros_like(image, dtype=np.float32)

    # forward DCT
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = image[i:i+block_size, j:j+block_size]
            compressed_dct[i:i+block_size, j:j+block_size] = dct_manual(block)

    # reverse DCT
    reconstructed_dct_man = np.zeros_like(image, dtype=np.float32)
    for i in range(0, height, block_size):
        for j in range(0, width, block_size):
            block = compressed_dct[i:i+block_size, j:j+block_size]
            reconstructed_dct_man[i:i+block_size, j:j+block_size] = idct_manual(block)
    reconstructed_dct_man = reconstructed_dct_man.astype(np.uint8)

    # DWT
    LL, LH, HL, HH = dwt_haar_manual(image)
    compressed_LL = LL.copy()
    reconstructed_dwt_man = idwt_haar_manual(compressed_LL, np.zeros_like(LH), np.zeros_like(HL), np.zeros_like(HH))


    cv2.imwrite('reconstructed_dct_manual.png', reconstructed_dct_man)
    cv2.imwrite('reconstructed_dwt_manual.png', reconstructed_dwt_man)


    psnr_dct = calculate_psnr(image, reconstructed_dct_man)
    psnr_dwt = calculate_psnr(image, reconstructed_dwt_man)


    print(f"PSNR for DCT Manual: {psnr_dct:.2f} dB")
    print(f"PSNR for DWT Manual: {psnr_dwt:.2f} dB")