from pydub import AudioSegment, silence
from discogs_lookup import GetAlbumFromDiscogs

record = AudioSegment.from_wav("/Users/benhenry/Desktop/Music/Poems Prayers and Promises.wav")
record_info = GetAlbumFromDiscogs("Poems Prayers and Promises")


norm = record #.normalize()

# If there are two or more silences with a "pop" or "click" sound between them, this function will stitch them together.
# User can set the pop_width parameter to the number of milliseconds that the pop or click sound lasts.
def stitch_silences(silences, pop_width=100):
    i = 0
    while i < len(silences) - 1:
        if silences[i][1] + pop_width > silences[i + 1][0]:
            silences[i][1] = silences[i + 1][1]
            silences.pop(i + 1)
        else:
            i += 1
    return silences

#Detect and remove periods of zero input - i.e. record not even recording
no_input = silence.detect_silence(norm, min_silence_len=1000, silence_thresh=-55, seek_step=100)
no_input = stitch_silences(no_input)
print(no_input)

tmp = None
last_silence = None
for index, silent in enumerate(no_input):
    end_condition = False
    if (index == 0):
        end_condition = True
        tmp = norm[0:silent[0]]
        last_silence = silent
    
    if (index == len(no_input) - 1):
        end_condition = True
        tmp += norm[last_silence[1]:silent[0]] + norm[silent[1]:]

    if not end_condition and last_silence is not None:
        tmp += norm[last_silence[1]:silent[0]]
        last_silence = silent


print(no_input)
print(norm.duration_seconds)
print(tmp.duration_seconds)
norm = tmp


print("Duration: ", round(norm.duration_seconds/60), "m", round(norm.duration_seconds)%60, "s")
silences = silence.detect_silence(norm, min_silence_len=1500, silence_thresh=-25, seek_step=50)
print("Silences: ", len(silences))
silences = stitch_silences(silences, pop_width=1000)
for i, s in enumerate(silences):
    # print(f"Silence {i}: {round((s[0]/1000)/60)}m{round((s[0]/1000)%60)}s for {round((s[1]-s[0])/1000,1)}s")
    print(f"Silence {i}: {round((s[0]/1000))}s for {round((s[1]-s[0])/1000,1)}s")

if (silences[0][0] <= 5):
    print("Detected leading silence")
    if (silences[0][1] - silences[0][0] > 3000):
        print("Removing all but 3s of leading silence")
        norm = norm[silences[0][1]-2000:]
    silences.pop(0)

#TODO: Optimize - could probably just subtract the removed amount from all silences.
silences = stitch_silences(silence.detect_silence(norm, min_silence_len=1500, silence_thresh=-25, seek_step=50), pop_width=500)

endmarks = []
for track in record_info['tracks']:
    duration = int(track['duration'].split(':')[0]) * 60 + int(track['duration'].split(':')[1])
    if track['position'] == 1:
        endmarks.append(duration)
    else: 
        endmarks.append(duration + endmarks[-1])

print("Endmarks: ", endmarks)

def distance(point_ms, silence):
    distance = 0
    if point_ms < silence[0]:
        distance = silence[0] - point_ms
    elif point_ms > silence[1]:
        distance = point_ms - silence[1]
    return distance

#Inefficient,but definitely not the slowest part of this script
for endmark in endmarks:
    closest_silence = [None, 9999999999999]
    for silenct in silences:
        if distance(endmark * 1000, silenct) < closest_silence[1]:
            closest_silence = [silenct, distance(endmark * 1000, silenct)]
    print(f"{endmark} is {closest_silence[1]/1000}s away from silence {closest_silence[0]}")



