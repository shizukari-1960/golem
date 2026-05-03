import discord

help = []
help[0] = discord.Embed(title='指令幫助訊息', description='此處將列舉所有本機器人中可使用的指令:')
help[1] = discord.Embed(title='1.一般擲骰', description='語法為`.[系統簡稱/系統名稱] [指令]`，如`.sw k100@10`，使用方式皆與CCFOLIA、烏東等BCDice系相同，如`.sw x3 k15@10`，另外，只要是BCDice允許的系統全稱，也可用此指令觸發，如`.DoubleCross 10dx`')
help[2] = discord.Embed(title='2.可用簡稱觸發表', description='1.通用骰子:\nd, D\n2.SW:\nsw, SW')