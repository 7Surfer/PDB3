
import logging
import datetime
from quickchart import QuickChart
from utils.db import DB

class ChartCreator():
    _rankColor = "#4E79A7"
    _scoreColor = "#F28E2B"
    _buildingScoreColor = "#E15759"
    _researchScoreColor = "#76B7B2"
    _fleetScoreColor = "#59A14F"
    _defensiveScoreColor= "#EDC948"

    #Custom Chart Options
    RANK = "0"
    SCORE = "1"
    RESEARCHRANK = "2"
    RESEARCHSCORE = "3"
    BUILDINGRANK = "4"
    BUILDINGSCORE = "5"
    DEFENSIVERANK = "6"
    DEFENSIVESCORE = "7"
    FLEETRANK = "8"
    FLEETSCORE = "9"
    BATTLESWON = "10"
    BATTLESLOST = "11"
    BATTLESDRAW = "12"
    DEBRISMETAL = "13"
    DEBRISCRYSTAL = "14"
    UNITSDESTROYED = "15"
    UNITSLOST = "16"

    #Group Options to Axis
    _highAxis = [SCORE, RESEARCHSCORE, BUILDINGSCORE, DEFENSIVESCORE, FLEETSCORE,
        DEBRISMETAL, DEBRISCRYSTAL, UNITSDESTROYED, UNITSLOST]
    _lowAxis = [RANK, RESEARCHRANK, BUILDINGRANK, DEFENSIVERANK, FLEETRANK,
        BATTLESWON, BATTLESLOST, BATTLESDRAW]
    
    def __init__(self, db):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Initialization")

        self._db:DB = db
    
    def getAllianceUrl(self, allianceData, allianceName):
        
        chartData = self._getAllianceChartData(allianceData)

        types = [self.SCORE, self.BUILDINGSCORE, self.RESEARCHSCORE, self.FLEETSCORE, 
            self.DEFENSIVESCORE]

        return self._createChartUrl(chartData, allianceName, types)

    def _getAllianceChartData(self, allianceData):
        
        chartData= {
            "rank": [],
            "score": [],
            "researchRank": [],
            "researchScore": [],
            "buildingRank": [],
            "buildingScore": [],
            "defensiveRank": [],
            "defensiveScore": [],
            "fleetRank": [],
            "fleetScore": [],
            "battlesWon": [],
            "battlesLost": [],
            "battlesDraw": [],
            "debrisMetal": [],
            "debrisCrystal": [],
            "unitsDestroyed": [],
            "unitsLost": [],
            "labels": []
        }

        currentDay = -1
        currentHour = -1
        idx = -1
        for datapoint in allianceData:
            timestamp:datetime.datetime = datapoint[7]

            if not (currentDay == timestamp.day and currentHour == timestamp.hour ):
                currentDay = timestamp.day
                currentHour = timestamp.hour
                idx+=1
                chartData["score"].append(0)
                chartData["researchScore"].append(0)
                chartData["buildingScore"].append(0)
                chartData["defensiveScore"].append(0)
                chartData["fleetScore"].append(0)
                chartData["labels"].append(datetime.datetime.strftime(datapoint[-1], "%H-%d.%m.%Y"))
            
            chartData["score"][idx] += datapoint[2]
            chartData["researchScore"][idx] += datapoint[3]
            chartData["buildingScore"][idx] += datapoint[4]
            chartData["defensiveScore"][idx] += datapoint[5]
            chartData["fleetScore"][idx] += datapoint[6]
            

        return chartData

    def _getChartData(self, userData:list):
        
        userChartData = []
        
        for user in userData:
            chartData= {
                "rank": [],
                "score": [],
                "researchRank": [],
                "researchScore": [],
                "buildingRank": [],
                "buildingScore": [],
                "defensiveRank": [],
                "defensiveScore": [],
                "fleetRank": [],
                "fleetScore": [],
                "battlesWon": [],
                "battlesLost": [],
                "battlesDraw": [],
                "debrisMetal": [],
                "debrisCrystal": [],
                "unitsDestroyed": [],
                "unitsLost": [],
                "labels": []
            }

            for datapoint in reversed(user):
                chartData["rank"].append(datapoint[1])
                chartData["score"].append(datapoint[2])
                chartData["researchRank"].append(datapoint[3])
                chartData["researchScore"].append(datapoint[4])
                chartData["buildingRank"].append(datapoint[5])
                chartData["buildingScore"].append(datapoint[6])
                chartData["defensiveRank"].append(datapoint[7])
                chartData["defensiveScore"].append(datapoint[8])
                chartData["fleetRank"].append(datapoint[9])
                chartData["fleetScore"].append(datapoint[10])
                chartData["battlesWon"].append(datapoint[11])
                chartData["battlesLost"].append(datapoint[12])
                chartData["battlesDraw"].append(datapoint[13])
                chartData["debrisMetal"].append(datapoint[14])
                chartData["debrisCrystal"].append(datapoint[15])
                chartData["unitsDestroyed"].append(datapoint[16])
                chartData["unitsLost"].append(datapoint[17])
                chartData["labels"].append(datetime.datetime.strftime(datapoint[-1], "%H-%d.%m.%Y") )

            userChartData.append(chartData)

        return userChartData

    def getChartUrl(self, userData, userName, types):
        chartData = self._getChartData([userData])[0]
        
        return self._createChartUrl(chartData, userName, types)

    def getCompareChart(self, userData:list, userNames:list, type):
        chartData = self._getChartData(userData)

        return self._createCompareChartUrl(chartData, userNames, type)
    
    def _createCompareChartUrl(self, chartData, userNames, type):
        qc = QuickChart()
        qc.width = 720
        qc.height = 480


        #Get correct Type as German Text
        label = ""
        if type == self.RANK:
            label = "Rang",
        elif type == self.SCORE:
            label = "Gesamtpunkte"
        elif type == self.RESEARCHRANK:
            label = "Forschungsrang"
        elif type == self.RESEARCHSCORE:
            label = "Forschungspunkte"
        elif type == self.BUILDINGRANK:
            label = "Geb??uderang"
        elif type == self.BUILDINGSCORE:
            label = "Geb??udepunkte"
        elif type == self.DEFENSIVERANK:
            label = "Verteidigungsrang"
        elif type == self.DEFENSIVESCORE:
            label = "Verteidigungspunkte"
        elif type == self.FLEETRANK:
            label = "Flottenrang"
        elif type == self.FLEETSCORE:
            label = "Flottenpunkte"
        elif type == self.BATTLESWON:
            label = "Gewonnene K??mpfe"
        elif type == self.BATTLESLOST:
            label = "Verlorene K??mpfe"
        elif type == self.BATTLESDRAW:
            label = "Unentschieden"
        elif type == self.DEBRISMETAL:
            label = "Tr??mmerfeld Metall"
        elif type == self.DEBRISCRYSTAL:
            label = "Tr??mmerfeld Kristall"
        elif type == self.UNITSDESTROYED:
            label = "Zerst??rte Einheiten"
        elif type == self.UNITSLOST:
            label = "Verlorene Einheiten"
                 

        #Set Default Config
        qc.config = self._getDefaultConfig(chartData, label)

        #ToDo: Rework with function _createChartUrl
        for user,userName in zip(chartData,userNames):
            if type == self.RANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["rank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.SCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["score"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.RESEARCHRANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["researchRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.RESEARCHSCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["researchScore"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BUILDINGRANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["buildinghRank"],
                    "fill": False}
                )
            elif type == self.BUILDINGSCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["buildingScore"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEFENSIVERANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["defensiveRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEFENSIVESCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["defensiveScore"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.FLEETRANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["fleetRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.FLEETSCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["fleetScore"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BATTLESWON:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["battlesWon"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BATTLESLOST:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["battlesLost"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BATTLESDRAW:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": userName,
                    "data": user["battlesDraw"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEBRISMETAL:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["debrisMetal"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEBRISCRYSTAL:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["debrisCrystal"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.UNITSDESTROYED:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["unitsDestroyed"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.UNITSLOST:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": userName,
                    "data": user["unitsLost"],
                    "fill": False,
                    "pointRadius": 1}
                )
        
        qc.config["options"]["scales"]["yAxes"] = self._getAxisConfig([type])

        return qc.get_short_url()

    def _createChartUrl(self, chartData, label, types):
        qc = QuickChart()
        qc.width = 720
        qc.height = 480

        #Set Default Config
        qc.config = self._getDefaultConfig([chartData], label)

        #Set Datasets
        for type in types:
            if type == self.RANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Rang",
                    "data": chartData["rank"],
                    "fill": False,
                    "pointRadius": 1,
                    "borderColor": self._rankColor}
                )
            elif type == self.SCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Gesamtpunkte",
                    "data": chartData["score"],
                    "fill": False,
                    "pointRadius": 1,
                    "borderColor": self._scoreColor}
                )
            elif type == self.RESEARCHRANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Forschungsrang",
                    "data": chartData["researchRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.RESEARCHSCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Forschungspunkte",
                    "data": chartData["researchScore"],
                    "fill": False,
                    "pointRadius": 1,
                    "borderColor": self._researchScoreColor}
                )
            elif type == self.BUILDINGRANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Geb??uderang",
                    "data": chartData["buildinghRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BUILDINGSCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Geb??udepunkte",
                    "data": chartData["buildingScore"],
                    "fill": False,
                    "pointRadius": 1,
                    "borderColor": self._buildingScoreColor}
                )
            elif type == self.DEFENSIVERANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Verteidigungsrang",
                    "data": chartData["defensiveRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEFENSIVESCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Verteidigungspunkte",
                    "data": chartData["defensiveScore"],
                    "fill": False,
                    "pointRadius": 1,
                    "borderColor": self._defensiveScoreColor}
                )
            elif type == self.FLEETRANK:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Flottenrang",
                    "data": chartData["fleetRank"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.FLEETSCORE:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Flottenpunkte",
                    "data": chartData["fleetScore"],
                    "fill": False,
                    "pointRadius": 1,
                    "borderColor": self._fleetScoreColor}
                )
            elif type == self.BATTLESWON:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Gewonnene K??mpfe",
                    "data": chartData["battlesWon"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BATTLESLOST:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Verlorene K??mpfe",
                    "data": chartData["battlesLost"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.BATTLESDRAW:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "lowAxis",
                    "label": "Unentschieden",
                    "data": chartData["battlesDraw"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEBRISMETAL:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Tr??mmerfeld Metall",
                    "data": chartData["debrisMetal"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.DEBRISCRYSTAL:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Tr??mmerfeld Kristall",
                    "data": chartData["debrisCrystal"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.UNITSDESTROYED:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Zerst??rte Einheiten",
                    "data": chartData["unitsDestroyed"],
                    "fill": False,
                    "pointRadius": 1}
                )
            elif type == self.UNITSLOST:
                qc.config["data"]["datasets"].append({
                    "yAxisID": "highAxis",
                    "label": "Verlorene Einheiten",
                    "data": chartData["unitsLost"],
                    "fill": False,
                    "pointRadius": 1}
                )

        
        qc.config["options"]["scales"]["yAxes"] = self._getAxisConfig(types)
        
        return qc.get_short_url()

    def _getAxisConfig(self,types):
        result = []

        highAxisNotSet = True
        lowAxisNotSet = True
        for type in types:
            if type in self._highAxis and highAxisNotSet:
                highAxisNotSet = False
                result.append(
                    {
                        "id": "highAxis",
                        "display": True,
                        "position": "right",
                        "gridLines": {
                            "drawOnChartArea": False
                        },
                        "ticks": {
                            "beginAtZero": True
                        }
                    }
                )
            if type in self._lowAxis and lowAxisNotSet:
                lowAxisNotSet = False
                result.append(
                    {
                        "id": "lowAxis",
                        "display": True,
                        "position": "left",
                        "ticks": {
                            "beginAtZero": True
                        }
                    }
                )
        return result

    def _getDefaultConfig(self, chartData, label):
        
        defaultConfig = {
            "type": "line",
            "data": {
                "labels": chartData[0]["labels"],
                "datasets": []
            },
            "options": {
                "title": {
                    "display": True,
                    "text": label,
                },
                "scales": {
                    "xAxes": [{
                        "stacked": True
                    }],
                    "yAxes": []
                }
            }
        }
        return defaultConfig
