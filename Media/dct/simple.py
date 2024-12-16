import numpy as np
import cv2
import pywt
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
import argparse

def apply_dct(image):
    height, width = image.shape
    dct_image = np.zeros_like(image, dtype=np.float32)
    
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = image[i:i+8, j:j+8]
            dct_block = dct(dct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
            dct_image[i:i+8, j:j+8] = dct_block
    
    return dct_image

def compress_dct(dct_image, keep_coeff=8):
    compressed = np.zeros_like(dct_image)
    height, width = dct_image.shape
    
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = dct_image[i:i+8, j:j+8]
            block[:keep_coeff, :keep_coeff] = block[:keep_coeff, :keep_coeff]
            compressed[i:i+8, j:j+8] = block
            
    return compressed

def apply_idct(dct_image):
    height, width = dct_image.shape
    reconstructed = np.zeros_like(dct_image, dtype=np.float32)
    
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = dct_image[i:i+8, j:j+8]
            idct_block = idct(idct(block, axis=0, norm='ortho'), axis=1, norm='ortho')
            reconstructed[i:i+8, j:j+8] = idct_block
            
    return np.clip(reconstructed, 0, 255).astype(np.uint8)

def apply_dwt(image):
    coeffs2 = pywt.dwt2(image, 'haar')
    LL, (LH, HL, HH) = coeffs2
    return LL, (LH, HL, HH)

def compress_dwt(LL):
    return np.round(LL)

def apply_idwt(LL, coeffs):
    return pywt.idwt2((LL, coeffs), 'haar')


def calculate_psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    return 10 * np.log10(max_pixel ** 2 / mse)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()    

    parser.add_argument("-i", help="Path to the input image.")
    args = parser.parse_args()  

    # Load image
    image = cv2.imread(args.i, cv2.IMREAD_GRAYSCALE)
    image = cv2.resize(image, (512, 512))

    # Save original image
    cv2.imwrite('original_image.png', image)



    # Library DCT Implementation
    dct_image = apply_dct(image)
    compressed_dct = compress_dct(dct_image, keep_coeff=4)
    reconstructed_dct_lib = apply_idct(compressed_dct)

    cv2.imwrite('reconstructed_dct_library.png', reconstructed_dct_lib)
    #cv2.imwrite('compressed_dct_library.png', compressed_dct)

    # Library DWT Implementation
    LL, coeffs = apply_dwt(image)
    compressed_LL = compress_dwt(LL)
    reconstructed_dwt_lib = apply_idwt(compressed_LL, (np.zeros_like(coeffs[0]), 
                                                    np.zeros_like(coeffs[1]), 
                                                    np.zeros_like(coeffs[2])))

    cv2.imwrite('reconstructed_dwt_library.png', reconstructed_dwt_lib)
#    cv2.imwrite('compressed_dwt_library.png', compressed_LL)

  
    # Calculate PSNR
    psnr_dct_lib = calculate_psnr(image, reconstructed_dct_lib)
    psnr_dwt_lib = calculate_psnr(image, reconstructed_dwt_lib)

    # Print PSNR Results
    print(f"PSNR for DCT Library: {psnr_dct_lib:.2f} dB")
    print(f"PSNR for DWT Library: {psnr_dwt_lib:.2f} dB")
