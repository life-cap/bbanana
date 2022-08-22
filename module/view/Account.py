import discord
from firebase_admin import db


class Join(discord.ui.View):
    def __init__(self, _id: discord.User.id):
        super().__init__()
        self._id = _id

    @discord.ui.button(label='오케이!', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self._id:
            db.reference(f'account/{interaction.user.id}').update({"money": 100})

            embed = discord.Embed(title="🎉 가입을 축하해요!", description="빠나나 왕국의 시민이 되신 걸 축하해요 :)",
                                  color=discord.Color.green())
            embed.set_author(name=f"{interaction.user.display_name}#{interaction.user.discriminator}",
                             icon_url=f"{interaction.user.display_avatar.url}")

            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()

    @discord.ui.button(label='싫어!', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self._id:
            embed = discord.Embed(title=":( 아쉽네요", description="다음 생에 볼 수 있기를 바랄게요 😭",
                                  color=discord.Color.red())
            embed.set_author(name=f"{interaction.user.display_name}#{interaction.user.discriminator}",
                             icon_url=f"{interaction.user.display_avatar.url}")

            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()


class Quit(discord.ui.View):
    def __init__(self, _id: discord.User.id):
        super().__init__()
        self._id = _id

    @discord.ui.button(label='남아있을게', style=discord.ButtonStyle.green)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self._id:
            embed = discord.Embed(title="🎉 마음 바로잡으신거죠?", description="빠나나 왕국에서 오래 봤으면 좋겠어요 :)",
                                  color=discord.Color.green())
            embed.set_author(name=f"{interaction.user.display_name}#{interaction.user.discriminator}",
                             icon_url=f"{interaction.user.display_avatar.url}")

            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()

    @discord.ui.button(label='그래도 할거야', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self._id:
            db.reference(f'account/{interaction.user.id}').delete()
            embed = discord.Embed(title=":( 아쉽네요 ㅜㅜ", description="다음 생에 볼 수 있기를 바랄게요 😭",
                                  color=discord.Color.red())
            embed.set_author(name=f"{interaction.user.display_name}#{interaction.user.discriminator}",
                             icon_url=f"{interaction.user.display_avatar.url}")

            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()
