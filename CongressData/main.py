import pandas as pd

FIRST_CONGRESS = 97
LAST_CONGRESS = 114

congressDf = pd.DataFrame()

for i in range(FIRST_CONGRESS, LAST_CONGRESS+1):
    num = "000"
    if i < 100:
        num = "0" + str(i)
    else:
        num = str(i)

    print(i)

    print("descs")
    descsDf = pd.read_csv(f"descs/descr_{num}.txt", sep="|", encoding = 'unicode_escape', on_bad_lines='skip')
    print("speeches")
    speechesDf = pd.read_csv(f"speeches/speeches_{num}.txt", sep="|", encoding = 'unicode_escape', on_bad_lines='skip')
    print("speakers")
    speakersDF = pd.read_csv(f"speakers/{num}_SpeakerMap.txt", sep="|", encoding = 'unicode_escape', on_bad_lines='skip')

    descsDf = descsDf.merge(speechesDf, on="speech_id", how="outer")
    descsDf = descsDf.merge(speakersDF, on="speech_id", how="outer")

    congressDf = pd.concat([congressDf, descsDf])

congressDf.to_csv('data.csv', sep="|")
