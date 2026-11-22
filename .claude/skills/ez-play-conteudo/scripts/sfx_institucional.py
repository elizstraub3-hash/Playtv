# Efeitos sonoros e trilha do vídeo EZ Play, sintetizados do zero (sem material de terceiros).
import numpy as np, wave, sys
SR = 48000; DUR = 60.0; N = int(SR * DUR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR

def env_adsr(n, a=0.01, r=0.2):
    e = np.ones(n); na = max(1, int(a * SR)); nr = max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr) ** 2
    return e

def svf_bandpass(x, f0, f1, q=1.5):
    """Filtro passa-banda com frequência variando de f0 a f1 (varredura)."""
    y = np.zeros_like(x); low = band = 0.0
    fr = np.geomspace(f0, f1, len(x))
    for i in range(len(x)):
        f = 2 * np.sin(np.pi * fr[i] / SR)
        high = x[i] - low - band / q
        band += f * high; low += f * band
        y[i] = band
    return y

def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)):
        s = (1 - a) * x[i] + a * s; y[i] = s
    return y

def whoosh(d=0.7, f0=300, f1=4000, amp=0.5):
    n = int(d * SR); x = rng.standard_normal(n)
    y = svf_bandpass(x, f0, f1, 2.0)
    e = np.sin(np.linspace(0, np.pi, n)) ** 1.6
    return y / (np.abs(y).max() + 1e-9) * e * amp

def riser(d=1.3, amp=0.45):
    n = int(d * SR); t = np.arange(n) / SR
    tone = np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 1400, n)) / SR) * 0.35
    noise = svf_bandpass(rng.standard_normal(n), 400, 7000, 1.2)
    noise /= np.abs(noise).max() + 1e-9
    e = (t / d) ** 2.2
    return (tone + noise * 0.8) * e * amp

def impact(amp=0.9):
    n = int(1.6 * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (45 + 60 * np.exp(-t * 18)) * t) * np.exp(-t * 2.8)
    hit = lowpass(rng.standard_normal(n) * np.exp(-t * 30), 1800)
    hit /= np.abs(hit).max() + 1e-9
    return (sub * 0.9 + hit * 0.5) * amp

def bell(freq, d=1.4, amp=0.3):
    n = int(d * SR); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * freq * k * t) * w * np.exp(-t * (3 + k * 2)) for k, w in [(1, 1), (2.01, .45), (3.02, .22), (4.2, .1)])
    return y * env_adsr(n, 0.002, 0.05) * amp

def shimmer(amp=0.25):
    out = np.zeros(int(1.6 * SR))
    for i, f in enumerate([1318.5, 1567.98, 1975.5, 2637.0]):
        b = bell(f, 1.0, amp); s = int(i * 0.09 * SR); out[s:s + len(b)] += b[:len(out) - s]
    return out

def click(amp=0.55):
    n = int(0.05 * SR); t = np.arange(n) / SR
    tick = np.diff(rng.standard_normal(n + 1)) * np.exp(-t * 400) * 0.6
    blip = np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 120)
    return (tick + blip) * amp

def pop(amp=0.45, f0=950, f1=320):
    n = int(0.12 * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t * 45)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 28) * amp

def ding(amp=0.32):
    out = np.zeros(int(1.8 * SR)); b1 = bell(1318.5, 1.2, amp); b2 = bell(1975.5, 1.4, amp)
    out[:len(b1)] += b1; s = int(0.14 * SR); out[s:s + len(b2)] += b2[:len(out) - s]
    return out

sfx = np.zeros(N)
def put(sound, at):
    s = int(at * SR); e = min(N, s + len(sound))
    if s < N: sfx[s:e] += sound[:e - s]

# --- Linha do tempo (segundos) ---
put(riser(1.2, 0.7), 0.0)
put(impact(0.6), 1.05)
put(shimmer(), 2.2)
for at in [4.75, 10.75, 18.75, 25.75, 32.75, 39.75, 46.75, 52.75]:   # trocas de cena
    put(whoosh(0.7, 250, 5000, 1.0), at)
for at in [11.2, 19.2, 26.2, 33.2]:                                  # celular subindo
    put(whoosh(0.9, 2500, 300, 0.75), at)
put(pop(0.4, 700, 260), 7.2)                                          # "Conheça o EZ Play"
put(click(0.5), 36.35)                                                   # toque no filme
put(whoosh(0.6, 800, 3500, 0.3), 40.3)                                # TV aparece
put(whoosh(0.5, 3000, 600, 0.28), 41.3)                               # celular entra
put(pop(0.38), 42.3)                                                  # aparelhos
for i in range(4): put(pop(0.75, 1000 + i * 120, 330 + i * 40), 47.4 + i * 0.35)   # cards
put(impact(0.45), 53.05)                                              # logo final
put(pop(0.4), 54.0)                                                   # planos
put(click(0.5), 55.6); put(ding(), 55.75)                             # botão WhatsApp
put(shimmer(0.18), 57.2)

# --- Trilha: pad + baixo + batida leve, 100 bpm, Am - F - C - G ---
bpm = 100; beat = 60 / bpm; bar = beat * 4
chords = [[57, 60, 64], [53, 57, 60], [48, 55, 60], [55, 59, 62]]   # MIDI
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
music = np.zeros(N)
nbar = int(DUR / bar) + 1
for b in range(nbar):
    c = chords[b % 4]; s = int(b * bar * SR); n = int(bar * SR); e = min(N, s + n)
    if s >= N: break
    t = np.arange(e - s) / SR
    pad = sum(np.sin(2 * np.pi * mtof(m + 12) * t + np.sin(2 * np.pi * 0.3 * t) * 0.4) * 0.5 +
              np.sin(2 * np.pi * mtof(m + 12) * 1.003 * t) * 0.3 for m in c)
    pad *= env_adsr(e - s, 0.5, 0.6)[: e - s] * 0.09
    bass = np.sin(2 * np.pi * mtof(c[0] - 12) * t) * 0.16 * (0.6 + 0.4 * np.exp(-(t % beat) * 4))
    music[s:e] += pad + bass
# batida a partir dos 5 s (entra junto com o gancho), sai suave no fim
kick_n = int(0.35 * SR); kt = np.arange(kick_n) / SR
kick = np.sin(2 * np.pi * (48 + 110 * np.exp(-kt * 35)) * kt) * np.exp(-kt * 9) * 0.55
hat_n = int(0.05 * SR); ht = np.arange(hat_n) / SR
hat = np.diff(rng.standard_normal(hat_n + 1)) * np.exp(-ht * 90) * 0.06
tb = 5.0
while tb < DUR - 1.5:
    i = int(tb * SR); music[i:i + kick_n] += kick[: max(0, min(kick_n, N - i))]
    j = int((tb + beat / 2) * SR); music[j:j + hat_n] += hat[: max(0, min(hat_n, N - j))]
    tb += beat
fade = np.ones(N); fi = int(1.5 * SR); fo = int(3 * SR)
fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] = np.linspace(1, 0, fo)
music *= fade

def write(name, x):
    x = np.clip(x, -1, 1); st = np.stack([x, x], 1)
    with wave.open(name, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())

out = sys.argv[1]
sfx *= 0.9 / max(1e-9, np.abs(sfx).max())
music *= 0.55 / max(1e-9, np.abs(music).max())
write(out + '/sfx.wav', sfx)
write(out + '/musica.wav', music)
write(out + '/sfx_musica.wav', sfx * 0.85 + music * 0.7)
print('ok')
