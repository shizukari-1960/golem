import aiohttp
import asyncio
import csv
import pandas as pd
from pprint import pprint

async def fetch_data(doc_code, gid):
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
                return csv_data
            else:
                raise Exception(f"Failed to fetch data: {response.status}")

def csv_to_df(csv_data):
    from io import StringIO
    df = pd.read_csv(StringIO(csv_data))
    return df

def modify_df(df):
    chr_dict = df.to_dict(orient='list')
    not_list_cols = ['player', 'age', 'gender', 'adven_class', 'belief', 'chr_name', 'race', 'reputation_total','reputation_used','soulscar', 'total_abi','total_exp','used_exp']
    list_cols = [col for col in chr_dict.keys() if col not in not_list_cols]
    for col in not_list_cols:
        if col in chr_dict:
            chr_dict[col] = chr_dict[col][0]
    for col in list_cols:
        chr_dict[col] = [x for x in chr_dict[col] if pd.notna(x)]
    return chr_dict
    
    
if __name__ == "__main__":
    csv_data = asyncio.run(fetch_data("19Eeq9w9xvTFUFZNcwt6XA_ztwAwX7GDLUcbAYIt_hKw", "1236171943"))
    data = csv_to_df(csv_data)
    data = modify_df(data)
    pprint(data)