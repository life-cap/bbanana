import asyncio

import discord
from discord.ext import commands
import os

import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

load_dotenv()


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        cred = credentials.Certificate("firebase.json")
        firebase_admin.initialize_app(cred, {
            "databaseURL": os.environ.get("FIREBASE_DB")
        })
        super().__init__(command_prefix="?", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Synced slash commands for {self.user}.")

    async def on_command_error(self, ctx, error):
        await ctx.reply(error, ephemeral=True)


bot = Bot()


async def main():
    async with bot:
        for filename in os.listdir("./commands"):
            if filename.endswith(".py"):
                await bot.load_extension(f"commands.{filename[:-3]}")
        await bot.start(os.environ.get("TOKEN"))


asyncio.run(main())
