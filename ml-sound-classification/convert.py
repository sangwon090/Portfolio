import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import librosa
import os

cmap = plt.get_cmap('inferno')

def save_linear(input, output):
    y, sr = librosa.load(input)
    plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB')
    plt.axis('off')
    plt.savefig(output, bbox_inches='tight', pad_inches=0)
    plt.clf()

def save_mel(input, output):
    y, sr = librosa.load(input)
    librosa.display.specshow(librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=sr), ref=np.max))
    plt.axis('off')
    plt.savefig(output, bbox_inches='tight', pad_inches=0)
    plt.clf()

with open('./UrbanSound8K.csv', newline='') as csv_file:
    data = csv_file.readlines()

    for index, row in enumerate(data):
        if index == 0:
            continue
            
        row = row.split(',')
        t = row[7].replace('\n', '')
        print(f'{row[0]} ({t})')

        if not os.path.exists(f'./out/linear/fold{row[5]}/'):
            os.makedirs(f'./out/linear/fold{row[5]}/')

        if not os.path.exists(f'./out/mel/fold{row[5]}/'):
            os.makedirs(f'./out/mel/fold{row[5]}/')

        temp = row[0].replace('wav', 'png')
        save_linear(f'./audio/fold{row[5]}/{row[0]}', f'./out/linear/fold{row[5]}/{temp}')
        save_mel(f'./audio/fold{row[5]}/{row[0]}', f'./out/mel/fold{row[5]}/{temp}')