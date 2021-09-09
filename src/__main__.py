import asyncio
from logging import getLogger
from omegaconf import OmegaConf
import discord
import requests
from discord.ext.commands import Bot
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

logger = getLogger(__name__)
config = OmegaConf.load('config.yaml')


class PriceData:
    def __init__(self):
        self.previous_price = 0


price_data = PriceData()
bot = Bot(command_prefix='!')


def get_metadata():
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/wall-street-bets-dapp").json()
        usd_price = response.get('market_data').get('current_price').get('usd')
        percentage_change_24 = response.get('market_data').get('price_change_percentage_24h')
        weekly_delta = response.get('market_data').get('price_change_percentage_7d')
        return {
            '24hr_change': f'{float(percentage_change_24):.2f}',
            'price': f'{usd_price:.6f}',
            'weekly_delta': f'{weekly_delta:.2f}'
        }
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print('Error when getting CoinGecko info: ', e)


@bot.event
async def on_ready():
    logger.warning('Started WSB DApp Price Bot')
    bot.loop.create_task(update_price())
    metadata = get_metadata()
    is_greater = False
    if float(metadata['price']) >= price_data.previous_price:
        is_greater = True
    price_data.previous_price = float(metadata['price'])
    await bot.change_presence(activity=discord.Activity(type=discord.activity.ActivityType.watching,
                                                        name=f"24hr: {metadata['24hr_change']}% | Don't 🧻 👐"))
    await bot.get_guild(771505726333255680).get_member(bot.user.id).edit(
        nick=f"{'⬈' if is_greater else '⬊'} {metadata['price']} 🚀")


@bot.command()
async def price(ctx):
    metadata = get_metadata()
    is_greater = False
    color = 0xff0000
    if float(metadata['price']) > price_data.previous_price:
        is_greater = True
        color = 0x00ff00
    price_data.previous_price = float(metadata['price'])
    await bot.get_guild(771505726333255680).get_member(bot.user.id).edit(
        nick=f"{'⬊' if is_greater else '⬈'} {metadata['price']} 🚀")
    embed = discord.Embed(title="WSB DApp Price Info", description=f"Price from CoinGecko", color=color)
    embed.add_field(name="💸 Price", value=f"{metadata['price']} USD")
    embed.add_field(name="💱 24hr Change", value=f"{metadata['24hr_change']}%")
    embed.add_field(name="📆 Weekly Delta", value=f"{metadata['weekly_delta']}%")
    if ctx.channel.id != 884903874190802994:
        await ctx.author.send(embed=embed)
    else:
        await ctx.reply(embed=embed)


async def update_price():
    while True:
        logger.warning('Updating Price...')
        metadata = get_metadata()
        price_data.previous_price = float(metadata['price'])
        await bot.change_presence(activity=discord.Activity(type=discord.activity.ActivityType.watching,
                                                            name=f"24hr: {metadata['24hr_change']}% | Don't 🧻 👐"))
        is_greater = float(metadata['price']) >= float(price_data.previous_price)
        await bot.get_guild(771505726333255680).get_member(bot.user.id).edit(
            nick=f"{'⬈' if is_greater else '⬊'} {metadata['price']} 🚀")
        await asyncio.sleep(60)


if __name__ == "__main__":
    bot.run(config.token)
