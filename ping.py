import mcstatus

server = mcstatus.MinecraftServer.lookup('xps.apmonitor.com')

print(server.ping())
print(server.status().raw)