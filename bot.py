"""File chính để chạy Discord bot"""
import discord
import asyncio
from discord.ext import commands
from config import DISCORD_TOKEN, PREFIX
from database import init_db

# Khởi tạo bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Danh sách cogs
initial_extensions = [
    'cogs.personality',
    'cogs.conversation',
    'cogs.slash_commands'
]

async def load_extensions():
    """Load tất cả cogs"""
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'✅ Đã load: {extension}')
        except Exception as e:
            print(f'❌ Không thể load {extension}: {e}')

@bot.event
async def on_ready():
    """Callback khi bot đã sẵn sàng"""
    init_db()
    print(f'✅ Bot đã đăng nhập: {bot.user.name} (ID: {bot.user.id})')
    print(f'🌐 Đang hoạt động trên {len(bot.guilds)} server(s)')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f'🔄 Đã sync {len(synced)} slash command(s)')
    except Exception as e:
        print(f'❌ Lỗi khi sync commands: {e}')

async def main():
    """Hàm chính để khởi động bot"""
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
