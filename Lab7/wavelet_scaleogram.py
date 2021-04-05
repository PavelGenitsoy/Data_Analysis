import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pywt

content = pd.read_excel(r'C:\Users\Lenovo\PycharmProjects\Data_Analysis\Lab6\statistics.xlsx', index_col=0)
doc_count = np.array(content.doc_count)

f_s = 100  # Sampling rate

N = doc_count.shape[0]
t = range(N)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 8))

ax1.plot(t, doc_count)
ax1.grid(True)
ax1.set_ylabel("Number of publications")
ax1.set_title("Dynamic of publications")

# Wavelet transform, i.e. scaleogram
cwtmatr, freqs = pywt.cwt(doc_count, range(1, N), "mexh", sampling_period=1/f_s)
ax2.pcolormesh(t, freqs, cwtmatr, vmin=-100, cmap="inferno", shading='auto')
ax2.set_ylim(0, 10)
ax2.set_ylabel("Scale")
ax2.set_xlabel("Time")
ax2.set_title("Scaleogram based on MexH wavelet")

plt.show()

fig.savefig('diagrams.png')
