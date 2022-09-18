import cv2
import time
import numpy as np
import numpy.fft as fft
import scipy.signal as signal
import mediapipe as mp
import matplotlib.pyplot as plt

from evm import magnify_color

mp_face_mesh = mp.solutions.mediapipe.python.solutions.face_mesh

video_width = 640
video_height = 480
roi_width = 160
roi_height = 80
roi_buffer_limit = 100
hr_buffer_limit = 10

if __name__ == '__main__':
    fps = 0
    previous_time = time.time()

    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, video_width)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, video_height)

    roi_left = 0
    roi_top = 0
    roi_frames = []
    roi_avg = []
    roi_acc = 0

    hr_buffer = []

    while True:
        # record video
        ret, frame = video.read()



        # calculate fps
        current_time = time.time()
        elapsed = current_time - previous_time
        previous_time = current_time
        fps = int(1 / elapsed)



        # extract roi
        with mp_face_mesh.FaceMesh() as face_mesh:
            results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            if not results.multi_face_landmarks:
                continue
            
            landmarks = results.multi_face_landmarks[0]

            if roi_left == 0:
                roi_left = int(landmarks.landmark[117].x * video_width)
            
            if roi_top == 0:
                roi_top = int(landmarks.landmark[117].y * video_height) - 15

        roi = frame[roi_top:roi_top+roi_height, roi_left:roi_left+roi_width]

        if roi.shape != (80, 160, 3):
            continue



        # get the average intensity of the roi
        roi_r, roi_g, roi_b = cv2.split(roi)
        roi_frames.append(roi)
        roi_avg.append(roi_g.sum() / (roi_width * roi_height))

        cv2.imshow('camera', frame)
        cv2.imshow('roi', roi_g)

        if cv2.waitKey(16) > 0:
            break

        if len(roi_frames) > roi_buffer_limit:
            roi_frames.pop(0)
        elif len(roi_frames) < roi_buffer_limit:
            continue

        if len(roi_avg) > roi_buffer_limit:
            roi_avg.pop(0)
        elif len(roi_avg) < roi_buffer_limit:
            continue

        roi_acc += 1



        # estimate heartrate
        if roi_acc <= (roi_buffer_limit + 30):
            continue

        roi_avg_avg = sum(roi_avg) / len(roi_avg)
        roi_norm = roi_avg.copy()

        for i in range(len(roi_avg)):
            roi_norm[i] = roi_norm[i] - roi_avg_avg

        fft_result = (fft.rfft(roi_norm)/len(roi_norm))[7:14]*2
        fft_freq = fft.rfftfreq(len(roi_norm), 1/15)[7:14]
        fft_peaks = signal.find_peaks(fft_result)

        if len(fft_peaks[0]) == 0:
            continue

        hr_buffer.append(int(fft_freq[fft_peaks[0][0]] * 60))

        if len(hr_buffer) > hr_buffer_limit:
            hr_buffer.pop(0)
        elif len(hr_buffer) < hr_buffer_limit:
            continue

        hr_estimated = sum(hr_buffer) / hr_buffer_limit
        print(f'estimated hr: {hr_estimated}')

        # measure more accurate heartrate
        magnified = magnify_color(np.array(roi_frames), 15, 1.0, 2.0, 3, 200)
        mag_g = magnified[:,:,:,1]
        mag_avg = [x.sum() / (roi_width * roi_height) for x in mag_g]
        mag_avg_avg = sum(mag_avg) / len(mag_avg)
        mag_norm = mag_avg.copy()

        for i in range(len(mag_avg)):
            mag_norm[i] = mag_norm[i] - mag_avg_avg

        mag_fft_result = (fft.rfft(mag_norm)/len(mag_norm))[10:20]*2
        mag_fft_freq = fft.rfftfreq(len(mag_norm), 1/10)[10:20]
        mag_fft_peaks = signal.find_peaks(mag_fft_result)

        if len(mag_fft_peaks[0]) == 0:
            continue

        mag_hr = int(mag_fft_freq[mag_fft_peaks[0][0]] * 60)

        print(f'estimated hr after evm: {mag_hr}')

        #plt.plot(range(roi_buffer_limit), roi_norm)
        #plt.xlabel('frame')
        #plt.ylabel('intensity')
        #plt.show()

        #plt.stem(fft_freq, abs(fft_result))
        #plt.xlabel('frequency')
        #plt.ylabel('amplitude')
        #plt.show()

        #plt.plot(range(roi_buffer_limit), mag_norm)
        #plt.xlabel('frame')
        #plt.ylabel('intensity')
        #plt.show()

        #plt.stem(mag_fft_freq, abs(mag_fft_result))
        #plt.xlabel('frequency')
        #plt.ylabel('amplitude')
        #plt.show()

        #plt.subplot(2, 2, 1)
        #plt.plot(range(roi_buffer_limit), roi_norm)
        #plt.xlabel('time')
        #plt.ylabel('intensity')
        #plt.grid()

        #plt.subplot(2, 2, 3)
        #plt.stem(fft_freq, abs(fft_result))
        #plt.xlabel('frequency')
        #plt.ylabel('amplitude')
        #plt.grid()

        #plt.subplot(2, 2, 2)
        #plt.plot(range(roi_buffer_limit), mag_norm)
        #plt.xlabel('frame')
        #plt.ylabel('intensity')
        #plt.grid()

        #plt.subplot(2, 2, 4)
        #plt.stem(mag_fft_freq, abs(mag_fft_result))
        #plt.xlabel('frequency')
        #plt.ylabel('amplitude')
        #plt.grid()

        #plt.show()

        if len(fft_peaks[0]) == 0:
            continue

        for _ in range(30):
            roi_frames.pop(0)
            roi_avg.pop(0)

        print('\n' * 21)

        if cv2.waitKey(16) > 0:
            break