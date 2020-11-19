import mcstatus

server = mcstatus.MinecraftServer.lookup('10.0.0.50')

print(server.ping())
print(server.status().raw)