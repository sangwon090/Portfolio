import numpy as np
import cv2

def gaussian_pyramid(image: np.ndarray, level: int = 3):
    img = image.copy()
    pyramids = [img]

    for i in range(level):
        img = cv2.pyrDown(img)
        pyramids.append(img)

    return pyramids

def gaussian_video(video: np.ndarray, level: int = 3):
    for i in range(0, video.shape[0]):
        frame = video[i]
        pyramid = gaussian_pyramid(frame, level)
        gaussian_frame = pyramid[-1]

        if i == 0:
            video_data = np.zeros((video.shape[0], gaussian_frame.shape[0], gaussian_frame.shape[1], 3))
        video_data[i] = gaussian_frame
    
    return video_data

def laplacian_pyramid(image: np.ndarray, level: int = 3):
    gaussian = gaussian_pyramid(image, level)
    pyramids = []

    for i in range(level, 0, -1):
        ge = cv2.pyrUp(gaussian[i])
        l = cv2.subtract(gaussian[i-1], ge)
        pyramids.append(l)
    
    return pyramids

def laplacian_video():
    return None