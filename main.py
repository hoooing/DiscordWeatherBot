import settings
import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
import requests
import json

logger = settings.logging.getLogger("bot")
dt_obj = datetime.now()
ts_am_pm = dt_obj.strftime('%I:%M %p')

def get_weather_info(city: str):
    # url = "http://api.weatherapi.com/v1/current.json"
    complete_url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={city}"
    res = requests.get(complete_url)
    print(res.status_code)
    if res.status_code == 200:
        data = res.json()
        location_name = data['location']['name']
        temperature_c = data['current']['temp_c']
        condition_text = data['current']['condition']['text']
        feels_like = data['current']['feelslike_c']
        local_time = data['location']['localtime']
        icon = data['current']['condition']['icon']
        return location_name, temperature_c, condition_text, feels_like, local_time, icon
    else:
        print(f"Failed to get data. Status code: {res.status_code}")
        return None        

def get_forecast_info(city: str):
    """"Extract high/low temp and chance of rain"""
    url = "http://api.weatherapi.com/v1/current.json"
    complete_url = f'http://api.weatherapi.com/v1/forecast.json?key={settings.WEATHER_API_KEY}&q={city}&days=1&aqi=no&alerts=no'
    res = requests.get(complete_url)
    print(f'{res.status_code} forecast')
    if res.status_code == 200:
        data = res.json()
        high = data['forecast']['forecastday'][0]['day']['maxtemp_c']
        low = data['forecast']['forecastday'][0]['day']['mintemp_c']
        chance = data['forecast']['forecastday'][0]['day']['daily_chance_of_rain']
        
        return high, low, chance
    else:
        print(f"Failed to get data. Status code: {res.status_code}")
        return None

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    
    bot = commands.Bot(command_prefix="!", intents=intents)
    
    @bot.event
    async def on_ready():
        print(bot.user)
        print(bot.user.id)
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)
        
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required Argument")
    
    @bot.tree.command()
    @app_commands.describe(name ="display the weather of the nearest city ex)/weather [city]")
    @app_commands.rename(name="location")
    async def weather(interaction: discord.Interaction, name : str):
        location, temp, cond, feels_like, local_time, icon = get_weather_info(name)
        high, low, chance_rain = get_forecast_info(name)
        embed = discord.Embed(
            colour=discord.Colour.dark_blue(),
            description="Weather Information given by weatherapi",
            title=f'Condition: {cond}'
        )
        degree_symbol = '\u00B0'
        embed.set_footer(text=f"Today at {ts_am_pm}")
        embed.set_author(name=f"Weather in {location}") #later add google maps location
        print(f'{icon}')
        embed.set_thumbnail(url = f'https:{icon}') 
        embed.add_field(name="Temperature", value = f"{temp} {degree_symbol}C")
        embed.add_field(name="Feels like", value = f"{feels_like} {degree_symbol}C")
        embed.add_field(name="High/Low", value = f"{high}/{low} {degree_symbol}C")
        embed.add_field(name="Localtime", value = f'{local_time}') 
        embed.add_field(name="Chance of rain", value = f'{chance_rain}')
        await interaction.response.send_message(embed=embed)
    

    bot.run(settings.DISCORD_API_SECRET)
if __name__ == "__main__":
    run()
    get_forecast_info('paris')
    