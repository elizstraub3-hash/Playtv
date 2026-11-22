# Lista as pausas de uma narração (para dividir em frases e calcular o tempo de cada palavra).
# Uso: python3 pausas.py narracao.wav   (converta antes: ffmpeg -i voz.mp3 -ar 48000 -ac 1 narracao.wav)
import wave, sys, numpy as np
w = wave.open(sys.argv[1]); sr = w.getframerate()
x = np.frombuffer(w.readframes(w.getnframes()), '<i2') / 32768
hop = sr // 100; fr = len(x) // hop
db = 20 * np.log10(np.array([np.sqrt(np.mean(x[i*hop:(i+1)*hop]**2)) for i in range(fr)]) + 1e-6)
q = db < db.max() - 32; gaps = []; i = 0
while i < fr:
    if q[i]:
        j = i
        while j < fr and q[j]: j += 1
        if j - i >= 12: gaps.append((round(i/100, 2), round((j-i)/100, 2)))
        i = j
    else: i += 1
print('duração', round(len(x)/sr, 2)); print('pausas (início, duração):', gaps)
