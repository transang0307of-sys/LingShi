"""Slash commands với UI components"""
import discord
from discord import app_commands
from discord.ext import commands
from utils.personalities import (
    PERSONALITIES, MOODS, SECTS, USER_ROLES,
    get_personality_list, get_mood_list, get_sect_list, get_user_role_list,
    get_sect_info, get_user_role_info
)
from database import get_user_state, update_user_state

class PersonalitySelect(discord.ui.Select):
    """Select menu cho tính cách - Chia thành 2 menu vì Discord limit 25 options"""
    def __init__(self, page=1):
        self.page = page
        
        if page == 1:
            # Trang 1: 5 tính cách đầu
            options = [
                discord.SelectOption(
                    label="Tsundere",
                    emoji="💢",
                    description="Gắt gỏi, khó chịu nhưng thầm quan tâm",
                    value="tsundere"
                ),
                discord.SelectOption(
                    label="Kuudere",
                    emoji="❄️",
                    description="Lạnh lùng, ít nói, bình thản",
                    value="kuudere"
                ),
                discord.SelectOption(
                    label="Dandere",
                    emoji="🌸",
                    description="Nhút nhát, e dè, chỉ mở lòng với người tin tưởng",
                    value="dandere"
                ),
                discord.SelectOption(
                    label="Deredere",
                    emoji="✨",
                    description="Vui vẻ, thân thiện, năng động",
                    value="deredere"
                ),
                discord.SelectOption(
                    label="Himedere",
                    emoji="👑",
                    description="Kiêu ngạo như công chúa",
                    value="himedere"
                ),
                discord.SelectOption(
                    label="Yandere",
                    emoji="🔪",
                    description="Yêu mãnh liệt, dễ ghen, nguy hiểm",
                    value="yandere"
                ),
            ]
        else:
            # Trang 2: 6 tính cách còn lại
            options = [
                discord.SelectOption(
                    label="Oneesan",
                    emoji="🌺",
                    description="Dịu dàng, chăm sóc như chị gái",
                    value="oneesan"
                ),
                discord.SelectOption(
                    label="Genki",
                    emoji="🎉",
                    description="Năng động, hoạt bát, luôn vui vẻ",
                    value="genki"
                ),
                discord.SelectOption(
                    label="Megane",
                    emoji="👓",
                    description="Thông minh, nghiêm túc, đeo kính",
                    value="megane"
                ),
                discord.SelectOption(
                    label="Ojousama",
                    emoji="💎",
                    description="Quý phái, lịch sự, tiểu thư nhà giàu",
                    value="ojousama"
                ),
                discord.SelectOption(
                    label="Kawaii",
                    emoji="🐰",
                    description="Dễ thương, ngọt ngào",
                    value="kawaii"
                ),
                discord.SelectOption(
                    label="Baka",
                    emoji="🤪",
                    description="Ngốc nghếch, vô tư, đáng yêu",
                    value="baka"
                )
            ]
        
        super().__init__(
            placeholder=f"Chọn tính cách (Trang {page}/2)...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id=f"personality_page_{page}"
        )
    
    async def callback(self, interaction: discord.Interaction):
        """Xử lý khi user chọn tính cách"""
        await interaction.response.defer(ephemeral=True)
        
        selected = self.values[0]
        user_id = interaction.user.id
        
        update_user_state(user_id, personality=selected)
        
        personality_data = PERSONALITIES[selected]
        embed = discord.Embed(
            title=f"✅ Thiết lập thành công - {selected.title()}",
            description=f"{personality_data['base']}\n\n**Phong cách:**\n{personality_data['speech_style']}",
            color=0x00ff00
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class MoodSelect(discord.ui.Select):
    """Select menu cho tâm trạng"""
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Vui",
                emoji="😊",
                description="Tâm trạng vui vẻ, nhiệt tình",
                value="vui"
            ),
            discord.SelectOption(
                label="Buồn",
                emoji="😢",
                description="Tâm trạng buồn bã, trầm lắng",
                value="buồn"
            ),
            discord.SelectOption(
                label="Giận",
                emoji="😠",
                description="Tâm trạng khó chịu, dễ nổi giận",
                value="giận"
            ),
            discord.SelectOption(
                label="Bình thường",
                emoji="😐",
                description="Tâm trạng ổn định",
                value="bình thường"
            )
        ]
        super().__init__(
            placeholder="Chọn tâm trạng...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="mood_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        selected = self.values[0]
        user_id = interaction.user.id
        
        update_user_state(user_id, mood=selected)
        
        embed = discord.Embed(
            title="✅ Thiết lập thành công",
            description=f"Tâm trạng giờ là: **{selected.title()}**",
            color=0x00ff00
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class SectSelect(discord.ui.Select):
    """Select menu cho tông môn"""
    def __init__(self):
        options = []
        for key, sect in SECTS.items():
            options.append(
                discord.SelectOption(
                    label=sect['name'],
                    emoji="⛰️",
                    description=sect['description'][:100],
                    value=key
                )
            )
        
        super().__init__(
            placeholder="Chọn tông môn...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="sect_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        selected = self.values[0]
        user_id = interaction.user.id
        sect_info = get_sect_info(selected)
        
        update_user_state(user_id, sect=selected)
        
        embed = discord.Embed(
            title=f"⛰️ {sect_info['name']}",
            description=sect_info['description'],
            color=0x00ff00
        )
        embed.add_field(name="⚔️ Đặc trưng", value=sect_info['specialty'], inline=False)
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class UserRoleSelect(discord.ui.Select):
    """Select menu cho role của user"""
    def __init__(self):
        options = []
        for key, role in USER_ROLES.items():
            options.append(
                discord.SelectOption(
                    label=role['name'],
                    emoji="🎭",
                    description=role['description'],
                    value=key
                )
            )
        
        super().__init__(
            placeholder="Bạn là ai đối với bot?",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="user_role_select"
        )
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        selected = self.values[0]
        user_id = interaction.user.id
        role_info = get_user_role_info(selected)
        
        update_user_state(user_id, user_role=selected)
        
        embed = discord.Embed(
            title=f"✅ Thiết lập vai trò: {role_info['name']}",
            description=f"**Mô tả:** {role_info['description']}\n\n"
                       f"**Bot sẽ gọi bạn là:** {role_info['bot_address_to_user']}\n"
                       f"**Bạn gọi bot là:** {role_info['address_to_bot']}",
            color=0x00ff00
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

class PersonaView(discord.ui.View):
    """View chứa select menu cho persona"""
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(PersonalitySelect(page=1))
        self.add_item(PersonalitySelect(page=2))
        self.add_item(MoodSelect())
        self.add_item(SectSelect())
        self.add_item(UserRoleSelect())

class SlashCommands(commands.Cog):
    """Slash commands cho bot"""
    
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="persona", description="Thiết lập tính cách, tâm trạng, tông môn và vai trò")
    async def persona(self, interaction: discord.Interaction):
        """Hiển thị menu persona"""
        user_id = interaction.user.id
        state = get_user_state(user_id)
        sect_info = get_sect_info(state['sect'])
        role_info = get_user_role_info(state['user_role'])
        
        embed = discord.Embed(
            title="🎭 Thiết lập Nhân Vật",
            description="Hãy chọn tính cách, tâm trạng, tông môn và vai trò từ menu bên dưới:",
            color=0xFF69B4
        )
        
        embed.add_field(
            name="🎭 Tính cách hiện tại",
            value=f"{PERSONALITIES[state['personality']]['emoji']} {state['personality'].title()}",
            inline=True
        )
        embed.add_field(
            name="💭 Tâm trạng hiện tại",
            value=state['mood'].title(),
            inline=True
        )
        embed.add_field(
            name="⛰️ Tông môn hiện tại",
            value=sect_info['name'],
            inline=True
        )
        embed.add_field(
            name="👤 Vai trò của bạn",
            value=role_info['name'],
            inline=True
        )
        
        embed.set_footer(text="Chỉ bạn mới thấy được tin nhắn này • Sẽ tự động biến mất sau 5 phút")
        
        await interaction.response.send_message(
            embed=embed,
            view=PersonaView(),
            ephemeral=True
        )
    
    @app_commands.command(name="status", description="Xem trạng thái hiện tại")
    async def status(self, interaction: discord.Interaction):
        """Xem status"""
        await interaction.response.defer(ephemeral=True)
        
        user_id = interaction.user.id
        state = get_user_state(user_id)
        sect_info = get_sect_info(state['sect'])
        role_info = get_user_role_info(state['user_role'])
        personality_data = PERSONALITIES[state['personality']]
        
        embed = discord.Embed(
            title=f"🎭 Thông Tin Nhân Vật - {interaction.user.display_name}",
            color=0xFF69B4
        )
        
        embed.add_field(
            name="⛰️ Tông môn", 
            value=f"{sect_info['name']}\n*{sect_info['description']}*", 
            inline=False
        )
        embed.add_field(
            name="🎭 Tính cách", 
            value=f"{personality_data['emoji']} {state['personality'].title()}\n*{personality_data['base'][:100]}...*",
            inline=False
        )
        embed.add_field(
            name="💭 Tâm trạng", 
            value=state['mood'].title(), 
            inline=True
        )
        embed.add_field(
            name="👤 Vai trò", 
            value=f"{role_info['name']}\n*Bot gọi bạn: {role_info['bot_address_to_user']}*",
            inline=True
        )
        embed.add_field(
            name="💬 Lịch sử", 
            value=f"{len(state['history'])} tin nhắn", 
            inline=True
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="reset", description="Xóa lịch sử hội thoại")
    async def reset(self, interaction: discord.Interaction):
        """Reset history"""
        await interaction.response.defer(ephemeral=True)
        
        user_id = interaction.user.id
        update_user_state(user_id, history=[])
        
        embed = discord.Embed(
            title="✅ Đã xóa lịch sử",
            description="Lịch sử hội thoại đã được xóa sạch!",
            color=0x00ff00
        )
        
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashCommands(bot))
