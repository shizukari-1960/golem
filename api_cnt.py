import requests
import asyncio
import aiohttp

url = 'https://bcdice.onlinesession.app'

system_alias = {
    "D":"DiceBot",
    "d":"DiceBot",
    "sw": "SwordWorld2.5:SimplifiedChinese",
    "SW": "SwordWorld2.5:SimplifiedChinese",
    "dx": 'DoubleCross',
    "sg": "ShinobiGami"
}
async def roll_dice_async(sys:str, cmd:str) -> str:
    """
    :param sys: System code provide by bcdice API.
    :type sys: str
    :param cmd: Diceroll command.
    :type cmd: str
    :return: Roll result.
    :rtype: str
    """
    endpoint = f'{url}/v2/game_system/{system_alias[sys] if sys in system_alias.keys() else sys}/roll'
    
    async with aiohttp.ClientSession() as session:
        params = {
        'command': cmd
        }
        try:
            async with session.get(endpoint, params=params, raise_for_status=True) as response:
                response.raise_for_status()
                data = await response.json()

                if data.get('ok'):
                    return data['text']
                else:
                    return data.get('reason')
        except aiohttp.ClientResponseError as e:
            print('API Fail:', e)
            return None


if __name__ == '__main__':
    c = asyncio.run(roll_dice_async('sw', 'K100@10+1'))
    print(c)
