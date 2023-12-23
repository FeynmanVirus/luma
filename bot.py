import discord
import responses
from discord.ui import Button, View
from discord.ext import commands
from config import TOKEN 
import callbacks

# intents and bot command
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="-", intents=intents)

def run_bot():
    # TOKEN = "MTE1MTEwOTk4MTQyMTE3NDc5NQ.GpWDfF.ozwe7j-rEToYUQp3BC66eZ0O8bBU78LQPnEVMc"

    
    client = discord.Client(intents=intents)

    
    @client.event
    async def on_ready():
        print(f"{client.user} is running.")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} messaged {user_message} in {channel}")
        
        if user_message == '-escrow':
            await escrow(message)
        elif '-google' in user_message:
            await google(message, user_message)
        elif '-luma' in user_message:
            await respond(message, user_message)
        elif user_message.startswith('-'):
            await respond(message, user_message)

    client.run(TOKEN)

@bot.command()
async def respond(message, user_input):
    try: 
        response = responses.response(user_input)
        if user_input == "-meme":
            await message.channel.send(embed=response) 
        else:
            await message.channel.send(response)
    except Exception:
        return Exception

@bot.command()
async def escrow(ctx):
    try:
        embed = discord.Embed(title="Are you a buyer or a seller?", description="Choose one to initiate the transaction", color=0x00ff00)
        button_buyer = Button(label="Buyer", style=discord.ButtonStyle.green)
        button_seller = Button(label="Seller", style=discord.ButtonStyle.red)

        # add callbacks to initial buttons
        button_buyer.callback = callbacks.button_buyer_callback # from callbacks.py
        button_seller.callback = callbacks.button_seller_callback # from callbacks.py
        view = View()
        view.add_item(button_buyer)
        view.add_item(button_seller)
        await ctx.channel.send(embed=embed, view=view)
    except Exception:
        return Exception

@bot.command()
async def google(ctx, search):
    # try:
    search_terms = ""
    for term in search.split():
        if term == '-google':
            continue
        search_terms += term + "+"
    print(search_terms)
    button = Button(label="Go to Google", url=f"https://www.google.com/search?q={search_terms}", style=discord.ButtonStyle.link)
    view = View()
    view.add_item(button)
    await ctx.channel.send(f"Results for {search}", view=view)
    # except Exception:
    #     return Exception
