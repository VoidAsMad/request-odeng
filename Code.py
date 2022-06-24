import discord
from discord.ext import commands
import asyncio
from discord_components.client import DiscordComponents
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
bot = commands.Bot(command_prefix="릴레야 ")

token = "봇의 토큰을 입력해주세요"

@bot.event
async def on_ready():
    DiscordComponents(bot)
    print(f"봇 {bot.user.name} 로 로그인했습니다")
    bot.remove_command('help')
    activity = discord.Game(name="https://discord.gg/WVnzBuu69g", type=4)
    await bot.change_presence(status=discord.Status.online, activity=activity)

    
    
@bot.command()
async def 초대(ctx):
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    embed=discord.Embed(color=0xFFFFFF)
    embed.add_field(name=f"{ctx.author} 님의 초대 횟수", value=f"{totalInvites}회", inline=False)
    await ctx.reply(embed=embed)

    
    
@bot.command()
async def 인증버튼(ctx):
    if ctx.author.guild_permissions.administrator:
        embed=discord.Embed(color=0x04ff00)
        embed.add_field(name="역할받기", value=f"아래 버튼을 누르면 <@&989130123112497152> 이 부여됩니다", inline=False)
        await ctx.send(embed=embed, components=[Button(label="역할받기", custom_id=f"verify_button")])
    else:
        await ctx.send("당신은 이 명령어를 사용할 권한이 없습니다")

        
        
@bot.command()
async def 티켓버튼(ctx):
    if ctx.author.guild_permissions.administrator:
        embed=discord.Embed(color=0x04ff00)
        embed.add_field(name="티켓생성", value=f"관리자와 1대1 채팅방을 생성합니다\n장난으로 생성시 불이익을 받을수있습니다", inline=False)
        await ctx.send(embed=embed, components=[Button(label="티켓 생성", custom_id=f"ticket_create")])
    else:
        await ctx.send("당신은 이 명령어를 사용할 권한이 없습니다")
 


@bot.event
async def on_button_click(interaction):
    if interaction.custom_id == "verify_button":
        role = discord.utils.get(bot.get_guild(interaction.user.guild.id).roles, id = 989130123112497152)
        await interaction.user.add_roles(role)
        await interaction.send(f"<@&989130123112497152> 역할이 지급되었습니다.")
    if interaction.custom_id == "ticket_create":
        channel = await interaction.guild.create_text_channel(f"{interaction.author.name}-님의-티켓")
        channel = bot.get_channel(channel.id)
        perms = interaction.channel.overwrites_for(interaction.guild.default_role)
        perms.read_messages=False
        await channel.set_permissions(interaction.guild.default_role, overwrite=perms)
        user = await bot.fetch_user(interaction.author.id)
        perms = interaction.channel.overwrites_for(user)
        await channel.set_permissions(user, read_messages=True)
        await interaction.send(f"<#{channel.id}> 티켓이 생성되었습니다")
        embed=discord.Embed(color=0x04ff00)
        embed.add_field(name=f"{user.name} 님의 티켓", value=f"관리자와 1대1 채팅방이 생성되었습니다", inline=False)
        await channel.send(f"<@{user.id}>",embed=embed)
 


@bot.command(aliases=["벤","차단"])
async def 밴(ctx, member:discord.Member=None, * ,reason=None):
    if ctx.author.guild_permissions.administrator:
        if not member:
            await ctx.send(embed=discord.Embed(title="오류", description=f"밴할 유저를 멘션해주세요", color=0xff0000), delete_after=3)
        else:
            await member.send(embed=discord.Embed(title=f"당신은 {ctx.guild.name} 에서 {ctx.author.name}에 의해 차단되었습니다.", description=f"사유: **{reason}**"))
            await member.ban(reason=reason)
            await ctx.send(embed=discord.Embed(title=f"{member.name}이(가) {ctx.author.name}에 의해 차단되었습니다.", description=f"사유: **{reason}**"), delete_after=3)
    else:
        await ctx.send("당신은 이 명령어를 사용할 권한이 없습니다")

        
        
bot.run(token)
