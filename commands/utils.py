import interactions
from utils.authorisation import Authorization
from utils.update import Update

class Bot(interactions.Extension):
    def __init__(self, client, args):
        self._client: interactions.Client = client
        self._auth:Authorization = args[0]
        self._update:Update = args[1]

    @interactions.extension_command(
        name="shutdown",
        description="Schaltet den Bot aus"
    )
    async def shutdown(self, ctx: interactions.CommandContext):
        if not self._auth.check(ctx.user.id, ctx.command.name):
            return

        self._update.stop()
        await ctx.send("Schlafenszeit zZz")
        await self._client._stop()

    @interactions.extension_command(
        name="update",
        description="Startet Aktualisierung der stats"
    )
    @interactions.autodefer(delay=60)
    async def update(self, ctx: interactions.CommandContext):
        if not self._auth.check(ctx.user.id, ctx.command.name):
            return
        
        await ctx.send("Starte Update")
        self._update.force()
        await ctx.message.edit("Update Complete")
    
    @interactions.extension_command(
        name="status",
        description="Status des Bots"
    )
    async def status(self, ctx: interactions.CommandContext):
        if not self._auth.check(ctx.user.id, ctx.command.name):
            return
        await ctx.send("Online auf {} Server".format(len(self._client.guilds)))
    
def setup(client, args):
    Bot(client, args)