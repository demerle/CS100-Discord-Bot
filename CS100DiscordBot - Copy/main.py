from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Reaction, Member
from sheets import update_csv,upload_csv_to_google_sheets

#Loading the Token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

#Base Bot Setup
intents: Intents = Intents.default()
intents.message_content = True
intents.members = True
client: Client = Client(intents=intents)


data = {"Username": [],
        "Display Name": [],
        "Total Messages": [],
        "Total Reactions": [],
        "Trivia Participation": []}

#Bot Startup
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!') #indicates that the bot is running

    guildID = 1333635588250664990 #guild means discord server
    guild = client.get_guild(guildID)
    if guild is None:
        print("Discord Server not found!")
        return

    for member in guild.members:
        #Adding every discord member to the server // Have to do it here instead during message due to some students having no activity

        username = member.name
        displayName = member.display_name if member.display_name else "Unknown"
        data["Username"].append(username)
        data["Display Name"].append(displayName)
        data["Total Messages"].append(0)
        data["Total Reactions"].append(0)
        data["Trivia Participation"].append(0)


    for channel in guild.text_channels: # Iterate through all text channels
        print("Fetching history from channel: " + channel.name)
        try:
            counter = 0
            async for message in channel.history(limit=None): #looping through every message in the current channel
                counter+=1
                print("Reading message number " + str(counter))

                if message.author == client.user:  # if the message is from the bot, then do nothing
                    continue

                index = data["Username"].index(message.author.name)
                data["Total Messages"][index] += 1

                for reaction in message.reactions: #looping through every reaction in the current message
                    async for user in reaction.users(): #async because of discord.py bs
                        reactorMember = guild.get_member(user.id)
                        currIndex = data["Username"].index(reactorMember.name)
                        data["Total Reactions"][currIndex] += 1
                        if channel.name == "trivia":
                            data["Trivia Participation"][currIndex] += 1


        except Exception as e:
            print(f"Error in channel {channel.name}: {e}")

    update_csv(data)
    upload_csv_to_google_sheets()

    await client.close() #bot process completion

#running main
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__': #not AI btw
    main()

