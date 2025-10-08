"""Cog quản lý personality và mood commands"""
import discord
from discord.ext import commands
from utils.personalities import (
    PERSONALITIES, MOODS, SECTS, USER_ROLES,
    get_personality_list, get_mood_list, get_sect_list, get_user_role_list,
    get_sect_info, get_user_role_info
)
from database import get_user_state, update_user_state

class PersonalityCommands(commands.Cog):
    """Commands liên quan đến personality, mood và tông môn"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='setpersonality')
    async def set_personality(self, ctx, personality: str):
        """Đặt tính cách cho bot - Mỗi user có tính cách riêng"""
        user_id = ctx.author.id
        
        if personality.lower() not in PERSONALITIES:
            available = ', '.join(get_personality_list())
            await ctx.send(f"❌ Tính cách không hợp lệ! Các tính cách có sẵn: {available}")
            return
        
        update_user_state(user_id, personality=personality.lower())
        await ctx.send(f"✅ Tính cách giờ là: **{personality}**")
    
    @commands.command(name='setmood')
    async def set_mood(self, ctx, mood: str):
        """Đặt tâm trạng cho bot - Mỗi user có tâm trạng riêng"""
        user_id = ctx.author.id
        
        if mood.lower() not in MOODS:
            available = ', '.join(get_mood_list())
            await ctx.send(f"❌ Tâm trạng không hợp lệ! Các tâm trạng có sẵn: {available}")
            return
        
        update_user_state(user_id, mood=mood.lower())
        await ctx.send(f"✅ Tâm trạng giờ là: **{mood}**")
    
    @commands.command(name='setsect')
    async def set_sect(self, ctx, sect: str):
        """Đặt tông môn"""
        user_id = ctx.author.id
        
        if sect.lower() not in SECTS:
            available = ', '.join(get_sect_list())
            await ctx.send(f"❌ Tông môn không hợp lệ! Các tông môn có sẵn: {available}")
            return
        
        sect_info = get_sect_info(sect.lower())
        update_user_state(user_id, sect=sect.lower())
        
        embed = discord.Embed(title=f"⛰️ {sect_info['name']}", color=0x00ff00)
        embed.add_field(name="📜 Mô tả", value=sect_info['description'], inline=False)
        embed.add_field(name="⚔️ Đặc trưng", value=sect_info['specialty'], inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='setrole')
    async def set_role(self, ctx, role: str):
        """Đặt vai trò của user"""
        user_id = ctx.author.id
        
        if role.lower() not in USER_ROLES:
            available = ', '.join([USER_ROLES[r]['name'] for r in get_user_role_list()])
            await ctx.send(f"❌ Vai trò không hợp lệ! Các vai trò có sẵn: {available}")
            return
        
        role_info = get_user_role_info(role.lower())
        update_user_state(user_id, user_role=role.lower())
        
        embed = discord.Embed(title=f"✅ Vai trò: {role_info['name']}", color=0x00ff00)
        embed.add_field(name="Mô tả", value=role_info['description'], inline=False)
        embed.add_field(name="Bot gọi bạn", value=role_info['bot_address_to_user'], inline=True)
        embed.add_field(name="Bạn gọi bot", value=role_info['address_to_bot'], inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='mystatus')
    async def my_status(self, ctx):
        """Xem trạng thái hiện tại"""
        user_id = ctx.author.id
        state = get_user_state(user_id)
        sect_info = get_sect_info(state['sect'])
        role_info = get_user_role_info(state['user_role'])
        
        embed = discord.Embed(
            title=f"🎭 Trạng thái của {ctx.author.display_name}", 
            color=0xff69b4
        )
        embed.add_field(name="⛰️ Tông môn", value=sect_info['name'], inline=True)
        embed.add_field(name="🎭 Tính cách", value=state['personality'], inline=True)
        embed.add_field(name="💭 Tâm trạng", value=state['mood'], inline=True)
        embed.add_field(name="👤 Vai trò", value=role_info['name'], inline=True)
        embed.add_field(name="💬 Tin nhắn", value=str(len(state['history'])), inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='resethistory')
    async def reset_history(self, ctx):
        """Xóa lịch sử hội thoại"""
        user_id = ctx.author.id
        update_user_state(user_id, history=[])
        await ctx.send("✅ Đã xóa lịch sử hội thoại!")
    
    @commands.command(name='help_bot')
    async def help_command(self, ctx):
        """Hướng dẫn sử dụng bot"""
        embed = discord.Embed(title="📖 Hướng Dẫn Sử Dụng", color=0x3498db)
        
        embed.add_field(
            name="💬 Nói chuyện",
            value="Mention bot hoặc gửi DM",
            inline=False
        )
        
        embed.add_field(
            name="🎭 Commands",
            value=(
                "`!setpersonality <tên>` - Đặt tính cách\n"
                "`!setmood <tâm trạng>` - Đặt tâm trạng\n"
                "`!setsect <tông môn>` - Chọn tông môn\n"
                "`!setrole <vai trò>` - Chọn vai trò\n"
                "`!mystatus` - Xem thông tin\n"
                "`!resethistory` - Xóa lịch sử\n"
                "`/persona` - Menu thiết lập (Slash)"
            ),
            inline=False
        )
        
        await ctx.send(embed=embed)

# QUAN TRỌNG: Phải có function này
async def setup(bot):
    await bot.add_cog(PersonalityCommands(bot))
