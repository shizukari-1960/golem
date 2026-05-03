import requests

url = 'http://localhost:9292'

system_alias = {
    "D":"DiceBot",
    "d":"DiceBot",
    "sw": "SwordWorld2.5:SimplifiedChinese",
    "SW": "SwordWorld2.5:SimplifiedChinese",
    "dx": 'DoubleCross'
}

def roll_dice(sys:str, cmd:str) -> str:
    
    endpoint = f'{url}/v2/game_system/{system_alias[sys] if sys in system_alias.keys() else sys}/roll'
    params = {
        'command': cmd
    }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get('ok'):
            return data['text']
            
        else:
            return data.get('reason')
        
        
    except requests.exceptions.RequestException as e:
        print('Api fail:', e)
        return None


if __name__ == '__main__':
    roll_dice('sw','k100@10+7')
