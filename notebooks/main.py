import pandas as pd

FIRST_CONGRESS = 97
LAST_CONGRESS = 114

def get_num(i):
    if i < 100:
        return "0" + str(i)
    else:
        return str(i)

def get_full_speeches():
    congressDf = pd.DataFrame()

    for i in range(FIRST_CONGRESS, LAST_CONGRESS+1):
        num = get_num(i)

        descsDf = pd.read_csv(f"data/descs/descr_{num}.txt", sep="|", encoding = 'unicode_escape', on_bad_lines='skip')
        descsDf["speech_id"] = descsDf["speech_id"].astype("string")

        speechesDf = pd.read_csv(f"data/speeches/speeches_{num}.txt", sep="|", encoding = 'unicode_escape', on_bad_lines='skip')
        speechesDf["speech_id"] = speechesDf["speech_id"].astype("string")

        speakersDf = pd.read_csv(f"data/speakers/{num}_SpeakerMap.txt", sep="|", encoding = 'unicode_escape', on_bad_lines='skip')
        speakersDf["speech_id"] = speechesDf["speech_id"].astype("string")

        descsDf = descsDf.merge(speechesDf, on="speech_id", how="outer")
        descsDf = descsDf.merge(speakersDf, on="speech_id", how="outer")

        descsDf.to_csv(f"data/full/full_{num}.csv")

get_full_speeches()