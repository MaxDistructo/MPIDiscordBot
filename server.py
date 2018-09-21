from mpi4py import MPI
import discord
from Config import readtoken

client = discord.Client()
token = readtoken()
mpi_clients = ["192.168.1.70", "192.168.1.71"]
i = 0
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
useclient = True


@client.event
async def on_ready():
    print('Logged in as: ')
    print(client.user.name)
    print(client.user.id)
    client.run(token)


@client.event
async def on_message(message):
    if rank == 0:
        if useclient:
            data2 = {"message", message.id, "token", token, "channel", message.channel.id}
            comm.send(data2, 1, 11)
        else:
            print("[" + comm.hostname + "] " + message.channel.guild.name + " #" + message.channel.name + " " +
                  message.author.name + "#" + message.author.discriminator + " " + message.channel.content)
            useclient = False

    elif rank == 1:
        data2 = comm.recieve(0, 11)
        client.run(data2["token"])
        message = client.get_message(client.get_channel(data2["channel"]), data2["message"])
        print("[" + comm.hostname + "] " + message.channel.guild.name + " #" + message.channel.name + " " +
              message.author.name + "#" + message.author.discriminator + " " + message.channel.content)
