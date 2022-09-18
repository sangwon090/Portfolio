import numpy as np
import cv2

from pyramid import gaussian_pyramid, gaussian_video, laplacian_pyramid, laplacian_video
from filter import Filter, filter

def load_video(video_path: str):
    video = cv2.VideoCapture(video_path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = int(video.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    video_data = np.zeros((frame_count, height, width, 3), dtype='float')
    x = 0

    while video.isOpened():
        ret, frame = video.read()
        if ret == True:
            video_data[x] = frame
            x += 1
        else:
            break
    
    return video_data, fps

def amplify(video: np.ndarray, amp: int):
    return video * amp

def magnify_color(video: np.ndarray, fps: int, low: float, high: float, level: int = 3, amp: int = 20):
    gaussian = gaussian_video(video, level)
    filtered = filter(gaussian, Filter.IDEAL, fps, low, high)
    amplified = amplify(filtered, amp)
    result = reconstruct(video, amplified, level)
    
    return result

def magnify_motion(video: np.ndarray, fps: int, low: float, high: float, level: int, amp: int):
    laplacian = laplacian_video(video, level)
    videos = []

    for i in range(level):
        filtered = filter(video, Filter.BUTTERWORTH, fps, low, high)
        filtered *= amp
        videos.append(filtered)

def reconstruct(original: np.ndarray, amplified: np.ndarray, level: int):
    result = np.zeros(original.shape)
    
    for i in range(amplified.shape[0]):
        frame = amplified[i]

        for j in range(level):
            frame = cv2.pyrUp(frame)
        
        frame += original[i]
        result[i] = frame

    return result

def save_video(path: str, video: np.ndarray, fps: int):
    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    [height, width] = video[0].shape[0:2]
    writer = cv2.VideoWriter(path, fourcc, fps, (width, height), True)

    for i in range(video.shape[0]):
        writer.write(cv2.convertScaleAbs(video[i]))
    
    writer.release()

if __name__ == '__main__':
    print('loading...')
    video, fps = load_video('sample/output.mov')
    
    print('magnifying...')
    magnified = magnify_color(video, fps, 1, 2, 4, 100)

    print('saving...')
    save_video('result.mp4', magnified, fps)