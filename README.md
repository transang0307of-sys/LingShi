# Discord Bot Tu Tiên - Đại Sư Tỷ

Bot Discord với 12 tính cách dere, phong cách tu tiên/võ hiệp.

## Features

- 12 tính cách: Tsundere, Kuudere, Dandere, Deredere, Himedere, Yandere, Oneesan, Genki, Megane, Ojousama, Kawaii, Baka
- 5 tông môn tu tiên
- 5 vai trò người dùng: Sư đệ, Sư phụ, Đạo hữu, Sư huynh, Tông chủ
- Slash commands với dropdown menus
- Phản hồi 250-1300 ký tự, tự động điều chỉnh
- Hỗ trợ tiếng Việt, phong cách tu tiên/võ hiệp

## Setup

1. Clone repo:

```
git clone <your-repo-url>
cd <repo-name>
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Tạo file `.env`:
```
DISCORD_TOKEN=your_discord_token_here
GEMINI_API_KEY=your_gemini_api_key_here
```

4. Chạy bot:
```
python main.py
```

## Requirements

- Python 3.9+
- discord.py 2.0+
- google-generativeai
- python-dotenv

## Cấu Trúc Project
```
lingshi/
├── bot.py                 # File chính để chạy bot
├── config.py              # Lưu constants và config
├── database.py            # Quản lý database operations
├── requirements.txt       # Dependencies
├── .env                   # Lưu tokens (không push lên git)
├── cogs/                  # Folder chứa cogs (commands)
│   ├── __init__.py
│   ├── personality.py     # Commands về personality
│   └── conversation.py    # Xử lý hội thoại
└── utils/                 # Helper functions
    ├── __init__.py
    └── personalities.py   # Data personalities và moods

```

## Commands

### Slash Commands
- `/persona` - Menu thiết lập tính cách, tông môn, vai trò
- `/status` - Xem trạng thái hiện tại
- `/reset` - Xóa lịch sử hội thoại

### Prefix Commands (!)
- `!setpersonality <tên>` - Đặt tính cách
- `!setmood <tâm trạng>` - Đặt tâm trạng
- `!setsect <tông môn>` - Chọn tông môn
- `!setrole <vai trò>` - Chọn vai trò
- `!mystatus` - Xem thông tin
- `!resethistory` - Xóa lịch sử

