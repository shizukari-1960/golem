from time import time

import aiohttp
import asyncio
import json
import pandas as pd
import os
import time
from random import uniform
from pprint import pprint


os.chdir(os.path.dirname(os.path.abspath(__file__)))

def csv_to_df(csv_data):
    from io import StringIO
    df = pd.read_csv(StringIO(csv_data))
    return df

def modify_df(df):
    chr_dict = df.to_dict(orient='list')
    #list欄位特別類舉
    list_cols = ['skills','skill_lev','growth']
    not_list_cols = [col for col in chr_dict.keys() if col not in list_cols]
    for col in not_list_cols:
        if col in chr_dict:
            chr_dict[col] = chr_dict[col][0]
    for col in list_cols:
        chr_dict[col] = [x for x in chr_dict[col] if pd.notna(x)]
        chr_dict[col] = [x for x in chr_dict[col] if x != '#REF!']

    #merge skill and skill_lev into a dict
    skills = chr_dict['skills']
    skill_levs = chr_dict['skill_lev']
    skill_dict = {}
    for skill, lev in zip(skills, skill_levs):
        skill_dict[skill] = lev
    chr_dict['skills'] = skill_dict
    chr_dict.pop('skill_lev', None)

    return chr_dict

_rate_limit_lock = asyncio.Lock()
_last_import_time = 0.0

async def import_chr(url):
    global _last_import_time
    async with _rate_limit_lock:
        now = time.monotonic()
        delay = uniform(3.0, 5.0)  # 隨機延遲3到5秒
        wait = delay - (now - _last_import_time)
        if wait > 0:
            await asyncio.sleep(wait)
        _last_import_time = time.monotonic()
        try:
            doc_code = url.split('/d/')[1].split('/')[0]
        except IndexError:
            return "Invalid URL format"
        try:
            gid = url.split('#gid=')[1]
        except IndexError:
            return "Invalid URL format"
        print(f"Importing character from doc: {doc_code}, gid: {gid}")

        url = f"https://docs.google.com/spreadsheets/d/{doc_code}/export"
        params = {
            "format": "csv",
            "gid": gid
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status == 200:
                    csv_data = await response.text(encoding='utf-8')
                    df = csv_to_df(csv_data)
                    if df.columns[0] != 'player':
                        return "Bad format"
                    chr = modify_df(df)
                    jsonstring = json.dumps(chr, ensure_ascii=False, indent=4)
                    with open(f'./chr_data/{doc_code}_{gid}.json', 'w', encoding='utf-8') as f:
                        f.write(jsonstring)
                    return f"Character imported successfully: {doc_code}_{gid}.json"
                else:
                    return f"Failed to fetch data: {response.status}"
                



    
if __name__ == "__main__":
    rt = asyncio.run(import_chr("https://docs.google.com/spreadsheets/d/19Eeq9w9xvTFUFZNcwt6XA_ztwAwX7GDLUcbAYIt_hKw/edit?gid=1236171943#gid=1236171943"))
    print(rt)