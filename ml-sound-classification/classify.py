from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img

import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import librosa
import librosa.display
import pyaudio
import wave
import time
import os

sounds = ['air_conditioner','car_horn','children_playing','dog_bark','drilling','engine_idling','gun_shot','jackhammer','siren','street_music']
pa = pyaudio.PyAudio()

def save_spectrogram(input, output):
    y, sr = librosa.load(input)
    librosa.display.specshow(librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max))
    plt.axis('off')
    plt.savefig(output, bbox_inches='tight', pad_inches=0)
    plt.clf()

for i in range(pa.get_device_count()):
    print(f'#{i}', pa.get_device_info_by_index(i)['name'].replace('\r\n', ''))

i_device = int(input('사용할 입력 장치: '))
sec = 1
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=192000, input=True, input_device_index=i_device, frames_per_buffer=512)

frames = []
model = tf.keras.models.load_model('model.h5')

while True:
    stream.start_stream()

    for i in range(0, int(192000 / 512 * sec)):
        data = stream.read(512)
        frames.append(data)

    timer_start = time.time()
    stream.stop_stream()
    out = wave.open('out.wav', 'wb')
    out.setnchannels(1)
    out.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    out.setframerate(192000)
    out.writeframes(b''.join(frames))
    out.close()

    save_spectrogram('./out.wav', './out.png')
    img = img_to_array(load_img('./out.png'))

    timer_prep = time.time()

    result = model.predict(img.reshape((1,)+img.shape))
    sorted_result = sorted([(v, result[0][i]) for i, v in enumerate(sounds)], key=lambda x: -x[1])

    os.system('cls' if os.name=='nt' else 'clear')

    timer_end = time.time()
    print('전처리 속도: %.4f개/sec' %(1.0 / (timer_prep - timer_start)))
    print('  예측 속도: %.4f예측/sec' %(1.0 / (timer_end - timer_prep)))
    print('    총 속도: %.4f예측/sec\n' %(1.0 / (timer_end - timer_start)))

    for i in range(10):
        print('%d. %s (%.4f%%)' %(i+1, sorted_result[i][0], sorted_result[i][1] * 100))

stream.stop_stream()
stream.close()
pa.terminate()