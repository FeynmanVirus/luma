import discord
from discord.ui import Button, View, Modal

# buyer button callback function
async def button_buyer_callback(interaction):
    # edit the embed
    embed = discord.Embed(title="Please mention the other party", description="Click the button to mention them", color=0x00ff00)
    button_mention_seller = Button(label="Mention Seller", style=discord.ButtonStyle.green)
    # button_mention_seller.callback = mention_seller_callback
    view = View()
    view.add_item(button_mention_seller)
    await interaction.response.edit_message(embed=embed, view=view)

# seller button callback function
async def button_seller_callback(interaction):
    # edit embed
    embed = discord.Embed(title="Please mention the other party", description="Click the button to mention them", color=0x00ff00)
    button_mention_buyer = Button(label="Mention Buyer", style=discord.ButtonStyle.red)
    view = View()
    view.add_item(button_mention_buyer)
    await interaction.response.edit_message(embed=embed, view=view)

# # mention seller button callback
# async def mention_seller_callback(interaction):
#     await show_modal(interaction)
#     await interaction.response.edit_message(content="Works", view=None)

# async def show_modal(interaction):
#     modal = Modal(title="This is a modal")
#     modal.add_item(InputText(label="Short Input"))
#     await ctx.send_modal(modal)