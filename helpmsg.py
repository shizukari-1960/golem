import discord

help = []
help.append(discord.Embed(title='指令幫助訊息', description='此處將列舉所有本機器人中可使用的指令:',color=15844367))
help.append(discord.Embed(title='1.一般擲骰', description='語法為`.[系統簡稱/系統名稱] [指令]`，如`.sw k100@10`\n使用方式皆與CCFOLIA、烏東等BCDice系相同，如`.sw x3 k15@10`\n另外，只要是BCDice允許的系統全稱，也可用此指令觸發，如`.DoubleCross 10dx`',color=5793522))
help.append(discord.Embed(title='2.可用簡稱觸發表', description='1.通用骰子:\nd, D\n2.SW:\nsw, SW', color=5793522))
help.append(discord.Embed(title='3.免觸發詞指令表', description='1. 平骰:如`2D6`\n2.多次骰:如`x3 2d6`\n3. 威力表擲骰:如`K100@10`(有@的才會觸發!)', color=5793522))