import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print('load data ', end='')
frames = []
for root, d_names, f_names in os.walk('wneus'):
   for f in f_names:
       fname = os.path.join(root, f)
       print('.', end='')
       frame = pd.read_csv(fname, index_col=0, sep=' ', header=None).dropna()
       frame.index = pd.to_datetime(frame.index)
       frames.append(frame)
print('')

frame = pd.concat(frames).sort_index()
max_delta = np.timedelta64(5, 'm')
exceeds_max_delta = np.diff(frame.index.values) > max_delta
jumps = frame[1:].index[exceeds_max_delta]
start = frame.index[0]
time_grouped_frames = []
for end in jumps:
    df = frame[(start <= frame.index) & (frame.index < end)]
    print(df)
    time_grouped_frames.append(df)
    start = end
df = frame[frame.index >= start]
time_grouped_frames.append(df)

fig, axes = plt.subplots((len(time_grouped_frames) + 1) // 2, 2)
row = 0
col = 0
for df in time_grouped_frames:
    df.plot(style='.', ax=axes[row, col])
    col += 1
    if col ==2:
        col = 0
        row += 1
