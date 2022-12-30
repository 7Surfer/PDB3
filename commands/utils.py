import interactions
import logging
from utils.authorisation import Authorization
from utils.update import Update
import config

class Bot(interactions.Extension):
    def __init__(self, client, args):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Initialization")

        self._client: interactions.Client = client
        self._auth:Authorization = args[0]
        self._update:Update = args[1]

    @interactions.extension_command(
        name="shutdown",
        description="Schaltet den Bot aus",
        scope=config.devDiscordId

    )
    async def shutdown(self, ctx: interactions.CommandContext):
        self._logger.debug("Command called: %s from %s",ctx.command.name, ctx.user.username)

        if not self._auth.check(ctx.user.id, ctx.command.name):
            await ctx.send(embeds=self._auth.NOT_AUTHORIZED_EMBED, ephemeral=True)
            return

        self._update.stop()
        await ctx.send("Schlafenszeit zZz")
        await self._client._stop()

    @interactions.extension_command(
        name="update",
        description="Startet Aktualisierung der stats",
        scope=config.devDiscordId
    )
    @interactions.autodefer(delay=60)
    async def update(self, ctx: interactions.CommandContext):
        self._logger.debug("Command called: %s from %s",ctx.command.name, ctx.user.username)

        if not self._auth.check(ctx.user.id, ctx.command.name):
            await ctx.send(embeds=self._auth.NOT_AUTHORIZED_EMBED, ephemeral=True)
            return
        
        await ctx.send("Starte Update")
        self._update.force()
        await ctx.message.edit("Update Complete")
    
    @interactions.extension_command(
        name="status",
        description="Status des Bots"
    )
    async def status(self, ctx: interactions.CommandContext):
        self._logger.debug("Command called: %s from %s",ctx.command.name, ctx.user.username)
        
        if not self._auth.check(ctx.user.id, ctx.command.name):
            await ctx.send(embeds=self._auth.NOT_AUTHORIZED_EMBED, ephemeral=True)
            return
        await ctx.send("Online auf {} Server".format(len(self._client.guilds)))
    
    @interactions.extension_command(
        name="features",
        description="Ungeordnete Liste der geplanten Updates"
    )
    async def features(self, ctx: interactions.CommandContext):
        self._logger.debug("Command called: %s from %s",ctx.command.name, ctx.user.username)
        if not self._auth.check(ctx.user.id, ctx.command.name):
            await ctx.send(embeds=self._auth.NOT_AUTHORIZED_EMBED, ephemeral=True)
            return
        
        featureLIst = """
        Geplante Features (ungeordnet):
            - Button zum Aktualisieren von den Stats
            - Chart für Allianzen
            - Liste von potentiell Inaktiven Spielern
            - Chart von 2 Spielern Vergleichen
            - Custom Charts (Typ,Zeitraum,...)"""

        await ctx.send(featureLIst)
    
def setup(client, args):
    Bot(client, args)