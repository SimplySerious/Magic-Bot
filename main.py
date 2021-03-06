import discord
import asyncio
from discord.ext import commands
from datetime import datetime

yes = ['yes', 'y', 'ye', 'aye', 'ha', 'haan', 'yeah', 'yup']
no = ['no', 'n', 'nay', 'na', 'nhi', 'nah', 'nope']
end = ['end', 'break', 'drop', 'exit', 'bye', 'cancel', 'close']
client = commands.Bot(command_prefix="do ", case_insensitive=True)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(msg):
    if not msg.author.bot and msg.content in [f'<@{client.user.id}>', f'<@!{client.user.id}>']:
            await msg.channel.send(f"My prefix is '{client.command_prefix}'")
    await client.process_commands(msg)

@client.command(name="guess", help='Guess a no and reply the bot corrctly to let the bot predict the no')
async def guess(ctx, limit=99):
    while True:
        time = datetime.utcnow()
        emb = discord.Embed(description=f"""Choose a natural no. lower than {limit} and keep that in your mind.
The bot will then try to predict your number by sending set lists of numbers
If your number is the most recent list of numbers, Say yes or else no.
Do you wanna start?""",
                            color=discord.Colour.blue())
        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        emb.timestamp = time
        await ctx.send(embed=emb)

        def check(msg):
            return msg.author == ctx.author
        try:
            msg = await client.wait_for('message', check=check, timeout=30)
            if msg.content.lower() in yes:
                x = 1
                ans = 0
                while x < (limit + 1):
                    nos = ''
                    write = False
                    for n in range(x, limit + 1):
                        if n % x == 0:
                            write = not write
                        if write == True:
                            nos += str(f"{'0' * (len(str(limit)) - len(str(n)))}{n}, ")
                    nos = nos[:-2] + '.'
                    try:
                        emb = discord.Embed(color=discord.Colour.blue())
                        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        emb.add_field(name="Is Your No Present Between The Following Group of Numbers?",
                                      value=f"```{nos}```")
                        emb.timestamp = time
                        await ctx.send(embed=emb)
                        ask = await client.wait_for('message', check=check, timeout=60)
                        if ask.content.lower() in yes:
                            ans += x
                        elif ask.content.lower() in no:
                            pass
                        elif ask.content.lower() in end:
                            emb = discord.Embed(description="Ok, Cancelling the game", color=discord.Colour.red())
                            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            emb.timestamp = time
                            await ctx.send(embed=emb)
                            return
                        else:
                            emb = discord.Embed(
                                description="Invalid Option, use some variant of yes or no\nif you dont wanna play, reply end or wait 60 seconds",
                                color=discord.Colour.red())
                            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                            emb.timestamp = time
                            await ctx.send(embed=emb)
                            continue
                    except asyncio.TimeoutError:
                        emb = discord.Embed(description="You waited too long, Cancelling the game",
                                            color=discord.Colour.red())
                        emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                        emb.timestamp = time
                        await ctx.send(embed=emb)
                        return
                    x *= 2
                if ans == 0 or ans > limit:
                    emb = discord.Embed(description="Why did you jus spam, read carefully next time?",
                                        color=discord.Colour.red())
                    emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    emb.timestamp = time
                    await ctx.send(embed=emb)

                else:
                    emb = discord.Embed(description=f"**Your number is {ans}**", color=discord.Colour.blue())
                    emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                    emb.timestamp = time
                    await ctx.send(embed=emb)


            elif msg.content.lower() in no:
                emb = discord.Embed(description="Ok, Cancelling the game", color=discord.Colour.red())
                emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                emb.timestamp = time
                await ctx.send(embed=emb)
                return
            else:
                emb = discord.Embed(description="Invalid Option, use some variant of yes or no",
                                    color=discord.Colour.blue())
                emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
                emb.timestamp = time
                await ctx.send(embed=emb)
                continue
        except asyncio.TimeoutError:
            emb = discord.Embed(description="You waited too long, Cancelling the game", color=discord.Colour.blue())
            emb.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            emb.timestamp = time
            await ctx.send(embed=emb)
            return
        return


client.run("Your-Token-Here")
