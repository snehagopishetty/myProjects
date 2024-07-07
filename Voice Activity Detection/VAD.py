import numpy as np
from matplotlib import pyplot as plt
from scipy.io.wavfile import read as readwav
from statistics import mean

frameSize = 25 #25 mislliseconds in a frame
windowSize = int(44100*(5/2000))

def wavInput(path): 
    wavInfo = {} 
    wavInfo['fs'], tempData = readwav(path)
    wavInfo['data'] = tempData.astype(np.float64)
    return wavInfo

def ZCR(wavInfo): 
    #SPF(samples per frame) #ZC(Array of zero crossings in each frame) 
    ZC = [] 
    SPF = int(frameSize*(wavInfo['fs']/1000)) 
    frameCount = int(len(wavInfo['data'])/SPF)

    for i in range(frameCount):
        begin = i*SPF
        end = min(len(wavInfo['data']), begin+SPF)
        frameSamples = wavInfo['data'][begin:end]
        tempZC = 0
        for j in range(1, len(frameSamples)):
            tempZC = tempZC + abs(np.sign(frameSamples[j]) - np.sign(frameSamples[j-1]))
        ZC.append(tempZC/len(frameSamples))
        
    return ZC

def STE(wavInfo):
    #SPF(samples per frame) #STEarr(Array of shortterm energies in each frame)
    STEarr = [] 
    SPF = int(frameSize*(wavInfo['fs']/1000)) 
    frameCount = int(len(wavInfo['data'])/SPF)
    
    for i in range(frameCount):
        begin = i*SPF
        end = min(len(wavInfo['data']), begin+SPF)
        #Now to get the squares of amplitude of the frame samples
        tempArr = np.zeros(np.array(wavInfo['data']).shape)
        tempArr[begin:end] = 1
        #Energy is proportional to the square of the amplitude
        STEarr.append(sum(((np.array(wavInfo['data']))**2)*tempArr))
    return STEarr

##The driver function that operates the VAD
#Threshold was tuned for the recorded audios, can be tuned better with more data, but for now this is working really good
def VAD(wavInfo):
    zcr = ZCR(wavInfo)
    ste = STE(wavInfo)
    threshold = 0.16*mean(ste)
    size = len(ste)
    SPF = int(frameSize*(wavInfo['fs']/1000))
    VAD = []
    
    for i in range(size):
        val = 0
        if ste[i] > threshold and zcr[i] < 0.1:
            val = 1
        for j in range(SPF):
            VAD.append(val)
    return VAD

#I/O part of the code
audio = wavInput("../Audio_Clips/Q5/male.wav")
plt.plot(audio['data'])
plt.savefig("../Plots/male_audio.png")
plt.close()
vad = VAD(audio)
plt.plot(vad)
plt.savefig("../Plots/male_VAD.png")
plt.close()