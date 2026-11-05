import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True          # 닉네임 변경 감지 필수 권한

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= ⚙️ 7개 키워드 & 역할 설정 =================
# "닉네임에 들어갈 단어": "부여할 디스코드 역할 이름" 형태로 적어주세요.
KEYWORD_MAP = {
    "[LV.10]": "브론즈 Lv.10",
    "[LV.20]": "실버 Lv.20",
    "[LV.30]": "골드 Lv.30",
    "[LV.40]": "에메랄드 Lv.40",
    "[LV.50]": "다이아 Lv.50",
    "[LV.75]": "마스터 Lv.75",
    "[LV.100]": "정복자 Lv.100",
}

BOT_TOKEN = ""
# ==========================================================

async def check_and_assign_role(member: discord.Member):
    # 7개의 키워드를 하나씩 검사
    for keyword, role_name in KEYWORD_MAP.items():
        if keyword in member.display_name:
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role and role not in member.roles:
                try:
                    await member.add_roles(role)
                    print(f"[성공] {member.display_name} 님에게 '{role.name}' 역할을 지급했습니다.")
                except discord.Forbidden:
                    print(f"[오류] 봇 역할 순위가 '{role.name}'보다 낮아 부여하지 못했습니다.")

@bot.event
async def on_ready():
    print(f"✅ HCF 봇이 성공적으로 실행되었습니다! (7개 키워드 감지 중)")

@bot.event
async def on_member_join(member: discord.Member):
    await check_and_assign_role(member)

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.display_name != after.display_name:
        await check_and_assign_role(after)

bot.run(BOT_TOKEN)