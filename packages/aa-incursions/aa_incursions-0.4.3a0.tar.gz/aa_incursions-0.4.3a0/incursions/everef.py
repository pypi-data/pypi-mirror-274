import bz2
import datetime
import json
import lzma
import os

from eveuniverse.models import EveConstellation, EveSolarSystem

from django.db import IntegrityError

from allianceauth.eveonline.models import EveFactionInfo
from allianceauth.services.hooks import get_extension_logger

from incursions.models import Incursion, IncursionInfluence

from .static_data import incursion_constellations

logger = get_extension_logger(__name__)


EVEREF_STAGING_FOLDER = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'data.everef.net/incursions/history/')


def import_staging_history(dir: str = EVEREF_STAGING_FOLDER):
    for entry in os.scandir(dir):
        if entry.name.startswith('incursions-') and entry.is_file():
            with bz2.open(entry) as f:
                for incursion in f.read().decode():
                    print(incursion)
        elif entry.is_dir():
            import_staging_history(entry)
# [{"constellation_id":20000651,"faction_id":500019,"has_boss":false,"infested_solar_systems":[30004459,30004460,30004461,30004462,30004463,30004464],"influence":0.0,"staging_solar_system_id":30004464,"state":"mobilizing","type":"Incursion"},{"constellation_id":20000520,"faction_id":500019,"has_boss":true,"infested_solar_systems":[30003565,30003566,30003567,30003568,30003569,30003570,30003571,30003572],"influence":1.0,"staging_solar_system_id":30003572,"state":"mobilizing","type":"Incursion"},{"constellation_id":20000173,"faction_id":500019,"has_boss":false,"infested_solar_systems":[30001184,30001185,30001186,30001187,30001182,30001183],"influence":0.0,"staging_solar_system_id":30001186,"state":"mobilizing","type":"Incursion"},{"constellation_id":20000618,"faction_id":500019,"has_boss":false,"infested_solar_systems":[30004224,30004225,30004226,30004227,30004228,30004229,30004222,30004223],"influence":0.32516667656600473,"staging_solar_system_id":30004227,"state":"established","type":"Incursion"}]


def import_staging_backfill(dir: str = EVEREF_STAGING_FOLDER):
    with lzma.open(os.path.join(EVEREF_STAGING_FOLDER, "backfills/eve-incursions-de-2023-10-12.json.xz")) as f:
        data = f.read()
        for incursion in json.loads(data):
            eve_constellation = EveConstellation.objects.get_or_create_esi(id=incursion['spawn']["constellation"]["id"])[0]
            if incursion['spawn']['endedAt'] is None:
                # dont handle any ongoing incursions.
                continue
            try:
                i = Incursion.objects.get(
                    established_timestamp__date=datetime.datetime.strptime(str(incursion['spawn']["establishedAt"]), "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                    ended_timestamp__date=datetime.datetime.strptime(str(incursion['spawn']["endedAt"]), "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                    constellation=eve_constellation)
            except Incursion.DoesNotExist:
                try:
                    i = Incursion.objects.create(
                        constellation=eve_constellation,
                        faction=EveFactionInfo.objects.get_or_create(faction_id=500019)[0],
                        staging_solar_system=EveSolarSystem.objects.get(name=incursion_constellations[eve_constellation.name]["Staging"]),
                        state=Incursion.States.ENDED,
                        established_timestamp=datetime.datetime.strptime(str(incursion['spawn']["establishedAt"]), "%Y-%m-%dT%H:%M:%S.%fZ"),
                        ended_timestamp=datetime.datetime.strptime(str(incursion['spawn']["endedAt"]), "%Y-%m-%dT%H:%M:%S.%fZ")
                    )
                except EveSolarSystem.DoesNotExist:
                    logger.error(eve_constellation.name)
            # Save an extra timestamps we can gather from this data
            try:
                if incursion['state'] == "Mobilizing":
                    i.mobilizing_timestamp = datetime.datetime.strptime(str(incursion['date']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    i.save()
                elif incursion['state'] == "Withdrawing":
                    i.withdrawing_timestamp = datetime.datetime.strptime(str(incursion['date']), "%Y-%m-%dT%H:%M:%S.%fZ")
                    i.save()
            except Exception as e:
                logger.exception(e)
            # Moving onto IncursionInfluence before we close the loop
            for ilog in incursion["spawn"]["influenceLogs"]:
                try:
                    IncursionInfluence.objects.create(
                        incursion=i,
                        influence=ilog['influence'],
                        timestamp=datetime.datetime.strptime(str(ilog["date"]), "%Y-%m-%dT%H:%M:%S.%fZ"))
                except IntegrityError:
                    # We already have this data
                    pass

#   {
#     "id": "1",
#     "date": "2015-02-06T18:13:45.000Z",
#     "state": "Established",
#     "spawn": {
#       "id": "12",
#       "establishedAt": "2015-02-06T18:13:45.000Z",
#       "endedAt": "2015-02-09T16:00:01.000Z",
#       "state": "Ended",
#       "constellation": {
#         "id": "20000011"
#       },
#       "influenceLogs": [
#         {
#           "id": "293702",
#           "date": "2021-10-30T09:00:00.000Z",
#           "influence": 0
#         },
#         {
#           "id": "293707",
#           "date": "2021-10-30T10:00:00.000Z",
#           "influence": 0
#         },
#         {
#           "id": "293712",
#           "date": "2021-10-30T11:00:00.000Z",
#           "influence": 0.048
#         },
#         {
#           "id": "293717",
#           "date": "2021-10-30T12:00:00.000Z",
#           "influence": 0.175333
#         },
#     }
#   },
