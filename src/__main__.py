from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import json
import os
import re
import matplotlib.pyplot as plt

def harvest_scripts():
    df = pd.read_csv('data/export.csv',header=0)

    for ind, row in df.iterrows():
        path = f'data/transcripts/{row['href']}.json'
        if os.path.exists(path): continue
        try:
            transcript = YouTubeTranscriptApi.get_transcript(row['href'])
        except Exception as e:
            print(e)
            print(row['href'])
            continue

        with open(path, 'w') as fp:
            json.dump(transcript,fp,indent=4) 

def parse_html():
    export = ['title,href']
    with open('data/export.html', 'r') as fp:
        html = fp.read()
    video_chunks = re.findall(r'(title="[^"]+?" href="/watch\?v=.+?")',html)
    for post in video_chunks:
        _, title, _, href, _ = post.split("\"")
        title = re.sub(",",";",title)
        href = re.sub("\/watch\?v=","",href)
        href = re.sub(r"(;|t=|&|&amp).*$","",href)
        # print(title,' ][ ',href)
        export.append(f'{title},{href}')
    csv = '\n'.join(export)
    with open('data/export.csv', 'w') as fp:
        fp.write(csv)

def char_to_time():
    df = pd.read_csv('data/export.csv',header=0)

    for ind, row in df.iterrows():
        path = f'data/transcripts/{row['href']}.json'
        if not os.path.exists(path): continue
        with open(path,'r') as file:
            content = json.load(file)
        for jnd, snippet in enumerate(content):
            if snippet['text'][-1] != ' ':
                snippet['text'] = snippet['text']+' '
            snippet_len = len(snippet['text'])
            if jnd == 0:
                snippet_dist = 0
            else:
                snippet_dist = content[jnd-1]['snippet_len'] + content[jnd-1]['snippet_dist']
            snippet['snippet_len'] = snippet_len
            snippet['snippet_dist'] = snippet_dist
        with open(path, 'w') as fp:
            json.dump(content,fp,indent=4) 

def segment_text():
    db = []
    df = pd.read_csv('data/export.csv',header=0)

    for ind, row in df.iterrows():
        fp = f'data/transcripts/{row['href']}.json'
        if not os.path.exists(fp): continue
        with open(fp,'r') as file:
            content = json.load(file)
        
        text = []
        for snippet in content:
            text.append(snippet['text'])
        
        transcript = ' '.join(text)
        transcript = transcript.replace(',',';')
        transcript = transcript.replace('  ',' ')
        transcript = transcript.lower()

        len_script = len(transcript)

        pos_theNameIsThe = None
        pos_theNameIs = None
        pos_theName = None
        end_agen = 0
        mid_agen = 0
        t_start = 0
        filtered_list = []

        pos_theNameIsThe = re.split(r'\Wthe name is the\W', transcript)
        pos_theNameIsThe = len_script - len(pos_theNameIsThe[-1])
        pos_theNameIs = re.split(r'\Wthe name is\W', transcript)
        pos_theNameIs = len_script - len(pos_theNameIs[-1])
        pos_theName = re.split(r'\Wthe name (?!(of|for))', transcript)
        pos_theName = len_script - len(pos_theName[-1])

        window = transcript[max([pos_theNameIsThe,pos_theNameIs,pos_theName]):-1]

        split_end_agen = re.split(r'\W(primy|prime|primon|primeagen|rimeag|genen|chen|genin|jen|jet|jin|jit|j|jan|ait|aen|ged|aent|agen|agent|legion)$', window)
        if len(split_end_agen)> 1:
            end_agen = len_script - len(split_end_agen[-1])
        
        split_mid_agen = re.split(r'\W(primy|prime|primon|primeagen|primeag|genen|chen|genin|jen|jet|jin|jit|j|jan|ait|aen|ged|aent|agen|agent|legion)\W', window)
        if len(split_mid_agen)> 1:
            mid_agen = len_script - len(split_mid_agen[-1])

        filtered_list = [d for d in content if d['snippet_dist'] < max([pos_theNameIsThe,pos_theNameIs,pos_theName])]
        if len(filtered_list) > 1:
            t_start = int(filtered_list[-1]['start']-2)

        filtered_list = [d for d in content if d['snippet_dist'] < max([end_agen,mid_agen])]
        if len(filtered_list) > 1:
            t_end = int(filtered_list[-1]['start']-2)

        tail_terms = window[-50: len(window)]

        episode = {
            'ref': ind,
            'title': row['title'],
            'href': row['href'],
            'len_script':len_script,
            'len_window':len(window),
            't_span':t_end-t_start,
            'pos_theNameIsThe':pos_theNameIsThe,
            'pos_theNameIs':pos_theNameIs,
            'pos_theName':pos_theName,
            'end_agen':end_agen,
            'mid_agen':mid_agen,
            't_start': t_start,
            't_end': t_end,
            'tail_terms': tail_terms
        }

        db.append(episode)
    # with open('data/db.json', 'w') as fp:
    #     json.dump(db,fp,indent=4)

    df = pd.DataFrame(db)
    df_pre = pd.read_csv('data/db.csv')
    df_pre = df_pre[['href','notes']] #imported to bring back manually added notes from CSV

    df['start_true'] = True
    df['end_true'] = True
    df.loc[(df['pos_theName'].eq(0)), 'start_true'] = None
    df.loc[(df['end_agen'].lt(1) & df['mid_agen'].lt(1)), 'end_true'] = None
    df['start_link'] = 'https://youtu.be/'+df['href']+'&t='+df['t_start'].astype(str)
    df['end_link'] = 'https://youtu.be/'+df['href']+'&t='+df['t_end'].astype(str)

    df = pd.merge(df,df_pre,on='href',how='outer')
    df = df.sort_values('t_span', ascending=False)

    df.to_csv('data/db.csv')
        

def main():
        
    option = input('''
(1) Extract Video Links from HTML Blob
(2) Harvest Transcripts
(3) Measure Time Against Characters
(4) Consolidate to Dataset
''')
    
    match option:
        case "1":
            parse_html()
        case "2":
            harvest_scripts()
        case "3":
            char_to_time()
        case "4":
            segment_text()

if __name__ == "__main__":
    main()