import os
from dotenv import load_dotenv
import logging
from logging.config import dictConfig
import discord

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")

GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")