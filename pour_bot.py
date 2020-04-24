import discord 
import pandas as pd

def embed_csv_file():
    df = pd.DataFrame(pd.read_csv('candles.csv'))
    categories = ['Candle_name', 'Amount', 'Other_info']
    candle_name_list= df[categories[0]].dropna().tolist()
    candle_amount = df[categories[1]].dropna().tolist()
    other_info = df[categories[2]].dropna().tolist()
    counter = 0 
    embed = discord.Embed(
        title='The Pour List',
        description = "Current pourlist",
        color = discord.Color.red() 
    )
    #Discord API limits 25 fields... 8*3 = 24 (No left over candle_name_list field)
    for x in range(len(candle_name_list)):
        if counter <= 7:
            embed.add_field(value= str(x+1) + '.) ' +  candle_name_list[x], name="Candle Name", inline= True)
            embed.add_field(value=candle_amount[x], name="Quantity", inline= True)
            embed.add_field(value=other_info[x] +  "\n\u200b", name="Other Information", inline=True)
            counter = counter + 1
        else:
            print('No remainder field due to API limit')
    embed.set_footer(text="Type !help for more information and commands")
    return embed 

client = discord.Client() 

@client.event
async def on_ready():
    print('We have logged in {0.user}'.format(client))

@client.event
async def on_member_join(member):
    # whenever someone joins the server... do: 
    #Place holder print statement -- May do something with this later. 
    print('welcome')

@client.event 
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!pourlist'):
        await message.channel.send(embed=embed_csv_file())
    if message.content.startswith('!help'):
        embed = discord.Embed(
            title='Commands Help'
        )
        embed.add_field(name="!pourlist", value='This command shows the current pourlist', inline=True)
        embed.add_field(name="!remove #", value="This command will remove a list item EX: !remove 2... this will remove item 2 on the list")
        await message.channel.send(embed=embed)
    if message.content.startswith('!remove'):
        df = pd.DataFrame(pd.read_csv('candles.csv'))
        message_list  = list(message.content)
        print(message_list)
        # Since the API restrics to 8 you can just read one digit([8] in list )
        new_pour_list = df.drop(index=int(message_list[8]) - 1) # +1 accounts for lists starting at 0 in py 
        new_pour_list.to_csv('candles.csv')
        # After a remove the content is now outdated, so send out a new one...
        await message.channel.send(embed=embed_csv_file())
client.run('')