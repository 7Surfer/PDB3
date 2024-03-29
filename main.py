import interactions
import logging
import datetime
from utils.authorisation import Authorization
from utils.db import DB
from utils.update import Update
from utils.chartCreator import ChartCreator
from utils.statsCreator import StatsCreator
from utils.notify import Notify
from utils.playerResolve import PlayerResolve
import config



def main():
    #Setup Logger
    logging.basicConfig(
        filename= datetime.datetime.now().strftime("%Y-%m-%d_%H-%M.log"),
        encoding='utf-8',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG
    )
    logger = logging.getLogger(__name__)

    logger.info("Startup")
    
    #Create Bot
    client = interactions.Client(token=config.prodToken)

    #Utils
    db = DB(prod = True)
    playerResolve = PlayerResolve(db)
    notify = Notify(client, db)
    update = Update(db, notify)
    authroization = Authorization(db)
    chartCreator = ChartCreator(db)
    statsCreator = StatsCreator(db, chartCreator)

    #Load Commands
    client.load("commands.utils", args=(authroization, update, notify, db))
    client.load("commands.auth", args=(authroization))
    client.load("commands.stats", args=(authroization, db, statsCreator, chartCreator, playerResolve))
    client.load("commands.planet", args=(authroization, db, statsCreator, notify, playerResolve))
    client.load("commands.chart", args=(authroization, db, chartCreator, playerResolve))
    client.load("commands.manageNotify", args=(authroization, db))

    #Start Bot
    logger.info("Initialization complete, starting client")
    
    @client.event
    async def on_start():
        await notify.notify(Notify.CHANNEL, "Ich Online")

    client.start()

if __name__ == "__main__":
    main()