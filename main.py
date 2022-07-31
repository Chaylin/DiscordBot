import discord
import pymongo
from datetime import datetime


TOKEN = 'OTgyNjA5OTc0MTgwMDY5NDQ3.GMk-sM.4U4U2roA45c_S_RoyRkbhGN515FHTZz5Tz1S3s'

client = discord.Client()
m_client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster0.kxi86.mongodb.net/Database?retryWrites=true&w=majority")
db = m_client.tribalwars
player = db.player
own_villages = db.own_villages
villages = db.villages202
dblogs = db.logs


@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    username = str(message.author).split('#')[0]
    user_msg = str(message.content)
    channel = str(message.channel.name)
    if message.author == client.user:
        return

    if channel == 'chat-bot':
        if user_msg.lower() == 'hello':
            await message.channel.send(f'Hello {username}')
            return

        if user_msg.lower() == 'bye':
            await message.channel.send(f'Bye {username}')
            return

        if user_msg.lower() == 'how are u':
            await message.channel.send(f"Hi {username}, thanks i'm fine!")
            return

        if user_msg.lower() == '!help':
            await message.channel.send('Database information \n'
                                       '!get player <key> <value> <player name> \n'
                                       '!get village <key> <value> <village-id> \n'
                                       '            keys: \n'
                                       '                apm_cap - "Get actions per minute limit (number)" \n'
                                       '                sleep - "Get farming (True/False)"\n'
                                       '                timeout_farm - "Get time between farm attacks (minutes)"\n'
                                       '                timeout_scout - "Get time between scout attacks (minutes)"\n'
                                       '                timeout_ram - "Get time between ram/cata attacks (minutes)"\n'
                                       '                gather - "Get gathering (True/False)"\n'
                                       '                recruit - "Get recruiting (True/False)"\n'
                                       '                build - "Get building (True/False)"\n'
                                       '                farm - "Get farming (True/False)"\n'
                                       '                gather - "Get gathering (True/False)"\n'
                                       '                recruit - "Get recruiting (True/False)"\n'
                                       '                fa_template_a[spear] - "Get FA template" \n'
                                       '                fa_template_b[light] - "Get FA template" \n'
                                       '                    units:  [spear] \n'
                                       '                            [sword] \n'
                                       '                            [axe] \n'
                                       '                            [archer] \n'
                                       '                            [spy] \n'
                                       '                            [light] \n'
                                       '                            [marcher] \n'
                                       '                            [heavy] \n'
                                       '!set player <key> <value> <player name> \n'
                                       '!set village <key> <value> <village-id> \n'
                                       )

            return


        # !log steff4080 2022-07-29 account
        if '!log' in user_msg.lower():
            data = get_log(f"{str(user_msg.lower()).split(' ')[1]} {str(user_msg.lower()).split(' ')[2]}")
            if 'account' in user_msg.lower():
                if data:
                    account = str(user_msg.lower()).split(' ')[1]
                    await message.channel.send(
                        f'Account [{account}] logs: \n'
                        f'Time spend for build: {round(data[account]["time_build"])} seconds \n'
                        f'Time spend for gather: {round(data[account]["time_gather"])} seconds \n'
                        f'Time spend for farm: {round(data[account]["time_farm"])} seconds \n'
                        f'Time spend for recruit: {round(data[account]["time_recruit"])} seconds \n'
                        f'Time spend for reports: {round(data[account]["time_reports"])} seconds \n'
                        f'Time lost for apm_cap: {round(data[account]["time_apm_cap"])} seconds \n'
                        f'Time lost for bot-captcha: {round(data[account]["time_bot_captcha"])} seconds \n'
                        f'Time spend for scan map: {round(data[account]["time_scan_map"])} seconds \n'
                        f'Read Reports: {round(data[account]["count_reports"])} \n'
                        f'Hit apm_cap: {round(data[account]["count_apm_cap"])} \n'
                        f'Hit bot_captcha: {round(data[account]["count_bot_captcha"])} \n'
                        f'Scan map: {round(data[account]["count_scan_map"])} \n'
                        f'Send farm_attacks: {round(data[account]["count_farm_attacks"])} \n'
                        f'Send scout_attacks: {round(data[account]["count_scout_attacks"])} \n'
                        f'Send ram_attacks: {round(data[account]["count_ram_attacks"])} \n'
                        f'Send cata_attacks: {round(data[account]["count_cata_attacks"])} \n'
                        f'Send gather: {round(data[account]["count_gather_send"])} \n'
                        f'Count buildings_build: {round(data[account]["count_buildings_build"])} \n'
                        f'Count units_recruit: {round(data[account]["count_units_recruit"])} \n'
                    )
                    return
            if user_msg.lower().split(' ')[3].isnumeric():
                if user_msg.lower().split(' ')[3] in data.keys():
                    vil_id = str(user_msg.lower().split(' ')[3])
                    await message.channel.send(
                        f'Village [{vil_id}] logs: \n'
                        f'Time spend on this village: {round(data[vil_id]["time_vil"])} seconds \n'
                        f'Time spend for build: {round(data[vil_id]["time_build"])} seconds \n'
                        f'Time spend for gather: {round(data[vil_id]["time_gather"])} seconds \n'
                        f'Time spend for farm: {round(data[vil_id]["time_farm"])} seconds \n'
                        f'Time spend for recruit: {round(data[vil_id]["time_recruit"])} seconds \n'
                        f'Time spend for farm_attacks: {round(data[vil_id]["time_farm_attacks"])} \n'
                        f'Time spend for scout_attacks: {round(data[vil_id]["time_scout_attacks"])} \n'
                        f'Time spend for ram_attacks: {round(data[vil_id]["time_ram_attacks"])} \n'
                        f'Time spend for cata_attacks: {round(data[vil_id]["time_cata_attacks"])} \n'
                        f'Send farm_attacks: {round(data[vil_id]["count_farm_attacks"])} \n'
                        f'Send scout_attacks: {round(data[vil_id]["count_scout_attacks"])} \n'
                        f'Send ram_attacks: {round(data[vil_id]["count_ram_attacks"])} \n'
                        f'Send cata_attacks: {round(data[vil_id]["count_cata_attacks"])} \n'
                        f'Send gather: {round(data[vil_id]["count_gather_send"])} \n'
                        f'Count buildings_build: {round(data[vil_id]["count_buildings_build"])} \n'
                        f'Count units_recruit: {round(data[vil_id]["count_units_recruit"])} \n'
                    )

                else:
                    await message.channel.send('No data found! Type: !help for formatting help')
                    return

        # !get player FA_template_A['spear'] stoffl2108
        if '!get' in user_msg.lower():
            data = None
            if '!get player' in user_msg.lower():
                data = get_player(str(user_msg.lower()).split(' ')[3])
            if '!get village' in user_msg.lower():
                data = get_village(str(user_msg.lower()).split(' ')[3])
            if '[' in user_msg.lower():
                key = str(user_msg).split(' ')[2]
                f_key = str(key.split('[')[0])
                n_key = str(key.split('[')[1])
                nested_key = str(n_key.replace("]", ""))
                try:
                    value = data[f'{f_key}'][f'{nested_key}']
                except KeyError:
                    await message.channel.send('No data found! Type: !help for formatting help')
                    return
            else:
                value = data[f"{str(user_msg.lower()).split(' ')[2]}"]
            if data:
                try:
                    await message.channel.send(
                        f"{str(user_msg.lower()).split(' ')[2]}: {value}")
                    return
                except KeyError:
                    await message.channel.send('No data found! Type: !help for formatting help')
                    return

            else:
                await message.channel.send('No data found! Type: !help for formatting help')
            return

        # !set player FA_template_A['spear'] 10 stoffl2108
        if '!set' in user_msg.lower():
            data = None
            if '!set player' in user_msg.lower():
                data = get_player(str(user_msg.lower()).split(' ')[4])
                set_player(str(user_msg.lower()).split(' ')[4],
                           str(user_msg.lower()).split(' ')[2],
                           user_msg.lower().split(' ')[3],
                           )
            if '!set village' in user_msg.lower():
                data = get_village(str(user_msg.lower()).split(' ')[4])
                set_village(str(user_msg.lower()).split(' ')[4],
                            str(user_msg.lower()).split(' ')[2],
                            user_msg.lower().split(' ')[3],
                            )
            if data:
                try:
                    await message.channel.send(
                        f"Set {str(user_msg.lower()).split(' ')[2]} of {str(user_msg.lower()).split(' ')[4]} to: \n"
                        f"{str(user_msg.lower()).split(' ')[3]}")
                    return
                except KeyError:
                    await message.channel.send('No data found! Type: !help for formatting help')
                    return

            else:
                await message.channel.send('No data found! Type: !help for formatting help')
            return

        if '!info' in user_msg.lower():
            data = get_enemy_vil(user_msg.lower().split(' ')[1])
            if data:

                await message.channel.send(
                    f"Village ID: {data['id']} \n \n"
                    f"Name: {data['name']} \n"
                    f"Punkte: {data['points']} \n"
                    f"Letzter Scout: {datetime.fromtimestamp(data['last scout'])} \n"
                    f"Gebäude: {data['buildings']} \n"
                )
                return
            else:
                await message.channel.send('No data found! Type: !help for formatting help')
                return

        if '!delete' in user_msg.lower():
            data = get_enemy_vil(user_msg.lower().split(' ')[1])
            if data:
                await message.channel.send(
                    f"Deleting following data from database: \n"
                    f"Village ID: {data['id']} \n \n"
                    f"Name: {data['name']} \n"
                    f"Punkte: {data['points']} \n"
                    f"Letzter Scout: {datetime.fromtimestamp(data['last scout'])} \n"
                    f"Name: {data['name']} \n"
                )
                delete_enemy_vil(user_msg.lower().split(' ')[1])
                return
            else:
                await message.channel.send('No data found! Type: !help for formatting help')
                return


def get_enemy_vil(village_id):
    find = {"id": village_id}
    result = villages.find_one(find)
    return result

def delete_enemy_vil(village_id):
    find = {"id": village_id}
    villages.delete_one(find)

def get_log(query):
    find = {'query': query}
    result = dblogs.find_one(find)
    return result


def get_player(player_name):
    find = {"player": player_name}
    result = player.find_one(find)
    return result


def get_village(village_id):
    find = {"id": int(village_id)}
    result = own_villages.find_one(find)
    return result


def set_player(player_name, key, value):
    if value.isnumeric():
        value = int(value)
    if type(value) == str:
        if 'false' in value:
            value = False
    if type(value) == str:
        if 'true' in value:
            value = True
    find = {"player": player_name}
    if '[' in key:
        f_key = str(key.split('[')[0])
        n_key = str(key.split('[')[1])
        nested_key = str(n_key.replace("]", ""))
        data = {f"{f_key}": {f"{nested_key}": value}}
    else:
        data = {f"{key}": value}

    result = player.find_one(find)
    if result:
        update = {"$set": data}
        player.update_one(find, update)


def set_village(village_id, key, value):
    if value.isnumeric():
        value = int(value)
    if type(value) == str:
        if 'false' in value:
            value = False
    if type(value) == str:
        if 'true' in value:
            value = True
    find = {"id": village_id}
    data = {f"{key}": value}
    result = own_villages.find_one(find)
    if result:
        update = {"$set": data}
        own_villages.update_one(find, update)


client.run(TOKEN)
