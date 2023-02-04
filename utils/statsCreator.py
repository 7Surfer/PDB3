
import logging
import interactions
from utils.db import DB
from utils.chartCreator import ChartCreator

class StatsCreator():

    def __init__(self, db:DB, chartCreator:ChartCreator):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Initialization")

        self._db:DB = db
        self._chartCreator:ChartCreator = chartCreator

    def getStatsContent(self, playerName:str):
        playerData = self._db.getPlayerData(playerName)
        if not playerData:
            raise ValueError(f"Spieler nicht gefunden: {playerName}")
        
        playerStats = self._db.getPlayerStats(playerData[1])
        allianceData = self._db.getAllianceById(playerData[5])

        currentPlayerStats = playerStats[0]

        currentPlayerStats = self._getCurrentPlayerStats(playerStats[0])
        diffData = self._getStatsDifference(playerStats)


        #Embed Fields
        statsFields = [
            interactions.EmbedField(
                inline=True,
                name="Type",
                value="Gesamt\nGebäude\nForschung\nFlotte\nVerteidigung\n"
            ),
            interactions.EmbedField(
                inline=True,
                name="Rang",
                value= self._getEmbedValueString(currentPlayerStats[0], diffData[0])
            ),
            interactions.EmbedField(
                inline=True,
                name="Punkte",
                value= self._getEmbedValueString(currentPlayerStats[1], diffData[1])
            )
        ]

        #Add Planet Data
        statsFields += self._getPlanetFields(playerData[1])

        #Add Research Data
        statsFields += self._getResearchFields(playerData[1])

        #Create Embed
        statsEmbed = interactions.Embed(
            title=f"{playerData[2]}",
            description= f"{playerData[1]}\n{allianceData[2]}", #PlayerId and Alliance Name
            fields = statsFields,
            timestamp=playerStats[0][19],
            thumbnail=interactions.EmbedImageStruct(
                url=self._chartCreator.getChartUrl(playerStats,playerData[2],
                        [
                            self._chartCreator.RANK,
                            self._chartCreator.SCORE,
                            self._chartCreator.BUILDINGSCORE,
                            self._chartCreator.RESEARCHSCORE,
                            self._chartCreator.FLEETSCORE,
                            self._chartCreator.DEFENSIVESCORE
                        ]
                    ),
                height=720,
                width=420
            )
        )

        statsComponents = [
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label='Planet Hinzufügen',
                custom_id='btn_planet'
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label='Angriffsforschung ändern',
                custom_id='btn_research_attack'
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label='Triebwerksforschung ändern',
                custom_id='btn_research_drive'
            ),
            interactions.Button(
                style=interactions.ButtonStyle.PRIMARY,
                label='Allianz',
                custom_id='btn_alliance'
            ),
            interactions.Button(
                style=interactions.ButtonStyle.SUCCESS,
                label='Aktualisieren',
                custom_id='btn_reload'
            ),
        ]
        return (statsEmbed, interactions.spread_to_rows(*statsComponents))


    def _getPlanetFields(self, playerId:str):
        planetData = self._db.getPlayerPlanets(playerId)

        planetEmbeds = [
            interactions.EmbedField(
                name="Position",
                value="",
                inline=True
            ),
            interactions.EmbedField(
                name="Mond",
                value="",
                inline=True
            ),
            interactions.EmbedField(
                name="Scannbar",
                value="",
                inline=True
            ),
        ]

        planetData.sort(key=lambda element: (element[2], element[3], element[4]))
        for planet in planetData:
            planetEmbeds[0].value += f"[{planet[2]}\:{planet[3]}\:{planet[4]}](https://pr0game.com/uni2/game.php?page=galaxy&galaxy={planet[2]}&system={planet[3]})\n"
            

            value = "-"
            if planet[5] and planet[6] >=0:
                startSystem, endSystem = self._getPhalanxRange(planet)
                value = f"{planet[6]}  [{startSystem}-{endSystem}]"
            
            planetEmbeds[1].value += f"{value}\n"

            planetEmbeds[2].value += f"{self._getOtherPlanetSymbols(planet)}\n"
        
        if not planetData:
            planetEmbeds[0].value = "-"
            planetEmbeds[1].value = "-"
            planetEmbeds[2].value = "-"

        return planetEmbeds

    def _getOtherPlanetSymbols(self, planet):
        result="-"
        
        galaxyMoons = self._db.getAllGalaxyMoons(galaxy=planet[2])
        
        friendlyPlayerIds = []
        for entry in self._db.getAllianceMember(326): #Allianz mit Poll
            friendlyPlayerIds.append(entry[0])
        for entry in self._db.getAllianceMember(401): #Space Schmuser
            friendlyPlayerIds.append(entry[0])
        friendlyMoon = 0
        enemyMoon = 0

        
        for moon in galaxyMoons:
            if moon[2] == 0:
                continue
            if self.isPlanetInSensorRange(moon[1],moon[2],planet[3]):
                if moon[0] in friendlyPlayerIds:
                    friendlyMoon+=1
                else:
                    enemyMoon+=1
        
        if enemyMoon > 0 or friendlyMoon > 0:
            result =  f":exclamation: {enemyMoon}\u2001\u2001:heart: {friendlyMoon}"

        return result
        

    def _getPhalanxRange(self,planet):
        if planet[6] == 0:
            return planet[3],planet[3]

        range = (planet[6]*planet[6]) -1
        startSystem = (planet[3] - range)
        endSystem = (planet[3] + range)
        if startSystem < 0:
            startSystem += 400
        if endSystem > 400:
            endSystem -= 400
        
        return startSystem,endSystem


    def _getResearchFields(self, playerId:str):

        researchData = self._db.getResearch(playerId)

        if not researchData:
            return []

        researchFields= [
            interactions.EmbedField(
                inline=True,
                name="Angriff",
                value=f":crossed_swords: {researchData[0]}\n:shield: {researchData[1]}\n :flying_saucer: {researchData[2]}\n"
            ),
            interactions.EmbedField(
                inline=True,
                name="Triebwerk",
                value=f":fire: {researchData[3]}\n:zap: {researchData[4]}\n:cyclone: {researchData[5]}\n"
            )
        ]

        return researchFields

    def isPlanetInSensorRange(self, moonSystem, moonLevel, planetSystem):
        if moonLevel == 0:
            return False

        range = (moonLevel*moonLevel) -1
        startSystem = (moonSystem - range)
        endSystem = (moonSystem + range)

        if endSystem > 400 and planetSystem < endSystem-400:
            return 0 < planetSystem < endSystem-400
        
        if startSystem < 0 and planetSystem > startSystem+400:
            return startSystem+400 < planetSystem < 400
            
        return (startSystem <= planetSystem <= endSystem)

    def _getEmbedValueString(self, data, diff):
        #get largest number
        maxLenghtData = len(max(data, key=len))

        result = "`"

        for elementData,elementDiff in zip(data,diff):
            result += elementData.ljust(maxLenghtData) + " " + elementDiff + "\n"

        return result + "`"

    def _getCurrentPlayerStats(self, playerStats):
        currentRank = [
            self.formatNumber(playerStats[1]),
            self.formatNumber(playerStats[5]),
            self.formatNumber(playerStats[3]),
            self.formatNumber(playerStats[9]),
            self.formatNumber(playerStats[7]),
        ]

        currentScore = [
            self.formatNumber(playerStats[2]),
            self.formatNumber(playerStats[6]),
            self.formatNumber(playerStats[4]),
            self.formatNumber(playerStats[10]),
            self.formatNumber(playerStats[8]),
        ]
        return [currentRank, currentScore]

    def _getStatsDifference(self, playerStats):
        if len(playerStats) == 1:
            return [ 
                ["n/a","n/a","n/a","n/a","n/a"],
                ["n/a","n/a","n/a","n/a","n/a",]
            ]

        current = playerStats[0]
        last= playerStats[1]
            
        diffRank = [
            self._formatDiff(int(current[1])-int(last[1])),
            self._formatDiff(int(current[5])-int(last[5])),
            self._formatDiff(int(current[3])-int(last[3])),
            self._formatDiff(int(current[9])-int(last[9])),
            self._formatDiff(int(current[7])-int(last[7]))
        ]

        diffStats = [
            self._formatDiff(int(current[2])-int(last[2])),
            self._formatDiff(int(current[6])-int(last[6])),
            self._formatDiff(int(current[4])-int(last[4])),
            self._formatDiff(int(current[10])-int(last[10])),
            self._formatDiff(int(current[8])-int(last[8]))
        ]

        return [diffRank, diffStats]

    def _formatDiff(self, number):
        return f"({number:+,})".replace(",",".")

    def formatNumber(self, number):
        return f"{number:,}".replace(",",".")
