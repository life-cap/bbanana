import discord
from discord.ext import commands
from firebase_admin import db
from module import is_joined, Join, Quit


class Account(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="가입", with_app_command=True, description="빠나나 왕국의 시민이 되고 싶다면 명령어로 시민이 되어주세요!")
    async def join(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        if db.reference(f'account/{ctx.author.id}').get() is not None:
            embed = discord.Embed(title="이미 가입하셨잖아요!", description="사기치지마세요!", color=discord.Color.red())
            embed.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator}님의 정보",
                             icon_url=f"{ctx.author.display_avatar.url}")
            return await ctx.reply(embed=embed)

        embed = discord.Embed(title="가입", description="정말 가입을 하실 건가요?", color=discord.Color.from_str("#F4E334"))
        embed.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator}님의 정보",
                         icon_url=f"{ctx.author.display_avatar.url}")
        await ctx.reply(embed=embed, view=Join(ctx.author.id))

    @commands.hybrid_command(name="탈퇴", with_app_command=True, description="빠나나 왕국의 일상이 즐겁지 않으시다면 명령어로 왕국을 나가세요!")
    async def quit(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        if db.reference(f'account/{ctx.author.id}').get() is None:
            embed = discord.Embed(title="가입 안하셨잖아요!", description="빠나나 왕국의 시민이 되고 싶다면\n`/가입`으로 가입해주세요!",
                                  color=discord.Color.red())
            embed.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator}님의 정보",
                             icon_url=f"{ctx.author.display_avatar.url}")
            return await ctx.reply(embed=embed)

        embed = discord.Embed(title="탈퇴", description="정말..정말...나가..실..거예요?", color=discord.Color.red())
        embed.set_author(name=f"{ctx.author.name}#{ctx.author.discriminator}",
                         icon_url=f"{ctx.author.display_avatar.url}")
        await ctx.reply(embed=embed, view=Quit(ctx.author.id))

    @commands.hybrid_command(name="나", with_app_command=True, description="현재 자신의 스탯을 보여줘요!")
    async def me(self, ctx: commands.Context, member: discord.Member = None):
        await ctx.defer()
        account = await is_joined(ctx)
        if account is not None:
            return await ctx.reply(embed=account)
        if member.bot:
            member = None
        if member is None:
            money = db.reference(f'account/{ctx.author.id}/money').get()
            embed = discord.Embed(color=discord.Color.from_str("#F4E334"))
            embed.add_field(name="MONEY", value=money)
            embed.set_author(name=f"{ctx.author.display_name}#{ctx.author.discriminator}님의 정보",
                             icon_url=f"{ctx.author.display_avatar.url}")
            await ctx.reply(embed=embed)
        else:
            money = db.reference(f'account/{member.id}/money').get()
            embed = discord.Embed(color=discord.Color.from_str("#F4E334"))
            embed.add_field(name="MONEY", value=money)
            embed.set_author(name=f"{member.display_name}#{member.discriminator}님의 정보",
                             icon_url=f"{member.display_avatar.url}")
            await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Account(bot))
