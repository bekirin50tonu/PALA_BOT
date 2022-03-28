import discord
from discord.ext import commands


def ctx_to_attr(ctx: commands.Context):
    guild: discord.Guild = ctx.guild
    voice_client: discord.VoiceClient = ctx.voice_client
    return guild, voice_client
