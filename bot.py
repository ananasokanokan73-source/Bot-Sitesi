import discord
from discord.ext import commands
import os
import random

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Basit bir XP (Seviye) sistemi için sözlük
kullanici_xp = {}

@bot.event
async def on_ready():
    print(f'Bot aktif: {bot.user.name}')
    await bot.change_presence(activity=discord.Game(name="!yardım | Pro Bot 🚀"))

# --- YARDIM MENÜSÜ ---
@bot.command(name='yardım')
async def yardim(ctx):
    embed = discord.Embed(
        title="🤖 Gelişmiş Bot Komut Listesi",
        description="Sunucunuzu yönetmek ve eğlenmek için tüm komutlar:",
        color=discord.Color.purple()
    )
    embed.add_field(name="🛠️ Moderasyon", value="`!temizle [sayı]` - Mesaj siler\n`!kick [@kullanıcı]` - Sunucudan atar\n`!ban [@kullanıcı]` - Yasaklar\n`!sustur [@kullanıcı]` - Zaman aşımı uygular", inline=False)
    embed.add_field(name="🎉 Eğlence & Ekonomi", value="`!zar` - Zar atar\n`!yazıtura` - Yazı tura atar\n`!profil` - Seviye ve XP durumunu gösterir\n`!çekiliş` - Rastgele kazanan seçer", inline=False)
    embed.add_field(name="📌 Bilgi & Sistem", value="`!merhaba` - Selamlaşır\n`!ping` - Gecikme süresini gösterir\n`!sunucubilgi` - Sunucu detaylarını verir", inline=False)
    embed.set_footer(text="Mobil Discord Botu 🚀")
    await ctx.send(embed=embed)

# --- TEMEL & BİLGİ KOMUTLARI ---
@bot.command(name='merhaba')
async def merhaba(ctx):
    await ctx.send(f'Selamlar {ctx.author.mention}! Mobil bottan selamlar! 🚀')

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! 🏓 Gecikme süresi: **{latency}ms**')

@bot.command(name='sunucubilgi')
async def sunucubilgi(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} Sunucu Bilgileri", color=discord.Color.green())
    embed.add_field(name="👑 Sunucu Sahibi", value=guild.owner, inline=True)
    embed.add_field(name="👥 Toplam Üye", value=guild.member_count, inline=True)
    embed.add_field(name="📅 Kuruluş Tarihi", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    await ctx.send(embed=embed)

# --- EĞLENCE VE ÇEKİLİŞ ---
@bot.command(name='zar')
async def zar(ctx):
    sonuc = random.randint(1, 6)
    await ctx.send(f'🎲 Atılan Zar: **{sonuc}**')

@bot.command(name='yazıtura')
async def yazitura(ctx):
    secenek = random.choice(["Yazı 🦅", "Tura 🪙"])
    await ctx.send(f'Paranın sonucu: **{secenek}**')

@bot.command(name='çekiliş')
async def cekilis(ctx, *, odul: str = "Hediye"):
    await ctx.send(f'🎉 **ÇEKİLİŞ BAŞLADI!** Ödül: **{odul}**\nKatılmak için 🎉 emojisine tıklayın!')
    # (Not: Gelişmiş reaksiyon tabanlı kazanan seçimi eklenebilir)

# --- SEVİYE (XP) SİSTEMİ ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    user_id = message.author.id
    # Her mesaj attığında rastgele XP kazandır
    kullanici_xp[user_id] = kullanici_xp.get(user_id, 0) + random.randint(5, 15)
    
    await bot.process_commands(message)

@bot.command(name='profil')
async def profil(ctx):
    user_id = ctx.author.id
    xp = kullanici_xp.get(user_id, 0)
    embed = discord.Embed(title=f"👤 {ctx.author.name} - Profil", color=discord.Color.gold())
    embed.add_field(name="✨ Toplam XP", value=f"{xp} XP", inline=True)
    await ctx.send(embed=embed)

# --- GELİŞMİŞ MODERASYON ---
@bot.command(name='temizle')
@commands.has_permissions(manage_messages=True)
async def temizle(ctx, miktar: int = 5):
    await ctx.channel.purge(limit=miktar + 1)
    await ctx.send(f'🧹 {miktar} adet mesaj başarıyla silindi.', delete_after=3)

@bot.command(name='kick')
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'👢 {member.mention} sunucudan atıldı! Sebep: {reason}')

@bot.command(name='ban')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'🔨 {member.mention} sunucudan yasaklandı! Sebep: {reason}')

@bot.command(name='sustur')
@commands.has_permissions(moderate_members=True)
async def sustur(ctx, member: discord.Member, dakika: int = 5, *, reason=None):
    from datetime import timedelta
    await member.timeout(timedelta(minutes=dakika), reason=reason)
    await ctx.send(f'🔇 {member.mention} {dakika} dakika süreyle susturuldu!')

# --- OTOMATİK KARŞILAMA ---
@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='hosgeldin')
    if channel:
        await channel.send(f'Aramıza hoş geldin {member.mention}! 🎉 Seninle beraber **{member.guild.member_count}** kişiyiz.')

# Botu Çalıştırma
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    TOKEN = 'BURAYA_BOT_TOKENINIZI_YAZIN'

bot.run(TOKEN)
  
