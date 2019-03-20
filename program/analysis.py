import numpy as np
from scipy.signal import butter, sosfiltfilt, sosfreqz
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt

from . import by3OctBand


def ene2dB(eneList, cali=1.0):
    ene = np.array(eneList)
    return 10 * np.log10((ene / cali)) + 94.0

def analyze_allBandEne(file):
    fs, data = read(file)
    data = data.astype("float32")
    # trueLen = len(data)
    eneList = []
    for centerF in by3OctBand.fList:
        filtData = bandPass(data, centerF, fs)
        bandEne = (filtData * filtData).sum()
        eneList.append(bandEne)
    return eneList

# ---------------------------------------------
# バンド分析詳細
# ---------------------------------------------
def mk_passFilt(lowcut, highcut, fs, order=8):
    fnyq = 0.5 * fs
    low = lowcut / fnyq
    high = highcut / fnyq
    sos = butter(order, [low, high], btype="bandpass", output="sos")  # 発散するので2次セクション化
    z, p, k = butter(order, [low, high], btype="bandpass", output="zpk")
    IRLen = getIRLen(p)
    return sos, IRLen

def getIRLen(p, eps=1e-9):  # eps:０近似ライン（計算機イプシロン？？,1e-9or7)
    r = np.max(np.abs(p))
    approx_impulse_len = int(np.ceil(np.log(eps) / np.log(r)))
    return approx_impulse_len

def bandPass(data, centerF, fs):
    lowcut = by3OctBand.rangeDic[centerF][0]
    highcut = by3OctBand.rangeDic[centerF][1]
    sos, IRLen = mk_passFilt(lowcut, highcut, fs)
    filtData = sosfiltfilt(sos, data, padlen=IRLen)
    return filtData

def getPower(file):
    fs, data = read(file)
    data = data.astype("float32")
    power = (data*data).sum()
    return power

def getCaliPower(file):
    fs, data = read(file)
    data = data.astype("float32")
    filtData = bandPass(data, 1000, fs)
    cali = (filtData * filtData).sum()
    return cali

# ---------------------------------------------
# グラフ作成
# ---------------------------------------------


def mk_fGraph(sos, fs=48000.0):
    freq, h = sosfreqz(sos, worN=24000)
    h[0] = h[1]
    plt.subplot(2, 1, 1)
    db = 20 * np.log10(np.abs(h))
    plt.xscale("log")
    plt.plot(24000 * freq / np.pi, db)
    plt.ylim(-75, 5)
    plt.grid(True)
    plt.yticks([0, -20, -40, -60])
    plt.ylabel('Gain [dB]')
    plt.title('Frequency Response')
    # plt.plot(freq/ np.pi, np.angle(h))
    # plt.grid(True)
    # plt.yticks([-np.pi, -0.5 * np.pi, 0, 0.5 * np.pi, np.pi],
    #                 ...[r'$-\pi$', r'$-\pi/2$', '0', r'$\pi/2$', r'$\pi$'])
    # plt.ylabel('Phase [rad]')
    plt.xlabel('Normalized frequency (1.0 = Nyquist)')
    plt.show()