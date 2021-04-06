import discord


def create_server_embed(server_data, server_address, server_name = 'Server is Online'):
    # description
    full_description = ''

    for list_item in server_data['description']['extra']:
        full_description += list_item['text']

    # main embed
    server_embed = discord.Embed(title=server_name, description=full_description, color=discord.Color.green())

    server_embed.add_field(name='Server Address', value=server_address)
    server_embed.add_field(name='Version', value=server_data['version']['name'])

    # number of players
    number_online = server_data['players']['online']
    online_max = server_data['players']['max']

    server_embed.add_field(name='Number of Players Online', value=str(number_online)+'/'+str(online_max))

    # player names
    if 'sample' in server_data['players']:
        players = []

        for player in server_data['players']['sample']:
            players.append(player['name'])

        formatted_players = ', '.join(players)

        server_embed.add_field(name='Players Online', value=formatted_players, inline=False)

    return server_embed