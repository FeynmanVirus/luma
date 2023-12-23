import random
import discord
import requests

def response(message):
    message = message.lower()
    print("called")
    match message:
        case '-hello':
            return "Hello there!"
        case '-roll':
            return random.randint(1, 6)    

        case '-help':
            return "```-hello - hello there\n-roll - roll a dice\n-meme - show a random meme\n-toss - toss a coin\n```"
        case '-meme':
            response = requests.get('https://meme-api.com/gimme').json()
            embedVar = discord.Embed(title=response['title'], description=response['postLink'], color=0x00ff00)
            embedVar.set_image(url=response['url'])
            return embedVar
        case '-toss':
            return random.choice(['Heads', 'Tails'])
        case _:
            r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                'model': 'mistral',
                'prompt': message,
                'stream': False,
            },
        ).json()
            print(r)
            return r['output']

    
