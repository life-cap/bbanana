from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="test", with_app_command=True, description="Testing")
    async def test(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)
        await ctx.reply("hi!")


async def setup(bot):
    await bot.add_cog(Test(bot))
