from enum import Enum, unique


@unique
class CardinalityShortNames(Enum):
    central = "c"
    north = "n"
    south = "s"
    east = "e"
    west = "w"
    northeast = "ne"
    northwest = "nw"
    southeast = "se"
    southwest = "sw"
    northcentral = "nc"
    southcentral = "sc"
    eastcentral = "ec"
    westcentral = "wc"


@unique
class RegionShortNames(Enum):
    africa = "af"
    asiapacific = "ap"
    asia = "as"
    australia = "au"
    brazil = "br"
    canada = "ca"
    germany = "de"
    europe = "eu"
    france = "fr"
    israel = "il"
    india = "in"
    italy = "it"
    japan = "jp"
    jioindia = "ji"
    korea = "kr"
    northamerica = "na"
    norway = "no"
    newzealand = "nz"
    poland = "pl"
    qatar = "qa"
    southamerica = "sa"
    singapore = "sg"
    southafrica = "za"
    sweden = "se"
    switzerland = "ch"
    uae = "ae"
    unitedkingdom = "uk"
    unitedstates = "us"


def get_cardinality_short_name(cardinality: str) -> str:
    return CardinalityShortNames[cardinality].value


def get_region_short_name(region_name: str) -> str:
    if len(region_name) == 2:
        return region_name.lower()
    for region in RegionShortNames:
        if region_name == region.name:
            return region.value
    raise ValueError(f"Region name {region_name} not found in RegionShortNames enum")
