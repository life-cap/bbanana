from discord.ext import commands
import discord
from firebase_admin import db


async def is_joined(ctx: commands.Context):
    if db.reference(f'account/{ctx.author.id}').get() is None:
        embed = discord.Embed(title="가입 안하셨잖아요!", description="빠나나 왕국의 시민이 되고 싶다면\n`/가입`으로 가입해주세요!",
                              color=discord.Color.red())
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                         icon_url=f"{ctx.author.display_avatar.url}")
        return embed
