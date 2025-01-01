from story_master.storage.map.map_model import Location, Map, Route, RouteType

SWORD_COAST = Location(
    id=0,
    name="The Sword Coast",
    description="""
The Sword Coast is the region in western Faerûn that lay along the coast of the Sea of Swords and extends inward into to the vale.
The Sword Coast was an expansive tract of wilderness, dotted with independent cities and overrun by bands of monstrous creatures,
that some saw as merely a place through which you had to travel in order to reach an actual meaningful destination.
It was much more than that of course, a rich and vibrant land with a long and storied history that encompassed some of the most important cities in all the Realms.
It was considered one of the rougher locales of Faerûn, both geographically and by virtue of its people.

While scholars disagreed as to the exact borders of the Sword Coast,
it was generally considered to have been bordered by the merchant nation of Amn in the south, and in the north by Waterdeep the Delimbiyr Vale.
Some guides considered it to begin south at Candlekeep and continued all the way north until the city of Luskan,
though most other cartographers and writers shared the former opinion on the matter, designating the coastal lands north of Waterdeep as the separate Sword Coast North.
Because much of the coastland was still relatively untamed wilderness, it was rich with game: rabbits and fowl including grouse, bustards, and rock doves, could be hunted in abundance
    """,
    short_description="The Sword Coast is the region in western Faerûn that lay along the coast of the Sea of Swords and extends inward into to the vale.",
    parent_location=None,
)

BALDURS_GATE = Location(
    id=1,
    name="Baldur's Gate",
    description="""
Baldur's Gate was a metropolis and city-state on the Sword Coast and Western Heartlands on the continent of Faerûn.
It was a crowded city of commerce and opportunity, and one of the most prosperous and influential merchant cities on the western coast of Faerûn.
Despite its long-standing presence as a neutral power, the leaders of Baldur's Gate were members of the Lords' Alliance of powers in the west.

The strong peace-keeping force known as the Watch, along with the presence of the powerful Flaming Fists mercenary company, kept the city generally peaceful and safe.
This inherent sense of security allowed the Gate to keep a tolerant and welcoming attitude towards outsiders, whether they were wealthy merchants,
poor refugees or, as it historically attracted, less-scrupulous individuals such as pirates and smugglers.

Baldur's Gate was located to the south of the great city-state of Waterdeep, north of Amn along the well-traveled Coast Way road,
that passed over the Wyrm's Crossing, through the Outer City and into the Gate proper.
It was nestled on a stretch of poor soil, within a natural bay that formed on the north bank of the River Chionthar about 40 miles (64.4 km) east from its mouth on the Sea of Swords.

As the minstrels of the 14th century described it, the city was a crescent moon that wrapped around the great harbor,
though in the century that followed it grew well beyond that form.
While the terrain of the Upper City was flat and level, the Lower City was built over steep bluffs that overlooked the Gray Harbor.

The region surrounding Baldur's Gate received an abundance of drizzling rain and sleet with frequent-occurring fog that rolled through the city's streets.
This excessive precipitation was well-mitigated with an advanced water system where underground basins collected the run off rainwater,
maneuvering it through subterranean aqueducts that emptied it into massive cistern beneath the Temples District.
Despite the city's engineering and cleanliness, this continual rain led to regular growth of mildew accompanied by a musky smell that permeated the city's cellars.
To abate the slippery stone streets, it was sometimes necessary to spread straw or gravel along the wet cobblestones
    """,
    short_description="Baldur's Gate was a metropolis and city-state on the Sword Coast and Western Heartlands on the continent of Faerûn.",
    parent_location=SWORD_COAST.id,
)

TROLL_CLAWS = Location(
    id=2,
    name="The Troll Claws",
    description="""
The Trollclaws was a region of troll-infested hills along the Sword Coast.
The Trollclaws lay along the northern edge of the Fields of the Dead.
Both the Winding Water and the Coast Way ran through the area.
The region often seemed shrouded in mist, and was characterized by steep, grassy hills, and dense foliage.
The Trollclaws were home to a seemingly inexhaustible population of trolls.
Repeated attempts by mercenaries and adventuring bands to clear the area seemed to have little effect.
A colony of these trolls regularly communicated with the trolls that inhabited the Trollbark Forest in the east.
    """,
    short_description="The Trollclaws was a region of troll-infested hills along the Sword Coast",
    parent_location=SWORD_COAST.id,
)

FIELDS_OF_THE_DEAD = Location(
    id=3,
    name="The Fields of The Dead",
    description="""
The Fields of the Dead was a region of grasslands and rolling hills in the Western Heartlands.
Centuries after the fighting, by the mid–14th century DR, bones still littered the field and cairns of the dead were everywhere.
Now used for farming and ranching, plows occasionally turned up skeletons in rusting armor, weapons, and other detritus
    """,
    short_description="The Fields of the Dead was a region of grasslands and rolling hills in the Western Heartlands.",
    parent_location=SWORD_COAST.id,
)


ROUTES = [
    Route(
        type=RouteType.LAND,
        start=BALDURS_GATE.id,
        end=TROLL_CLAWS.id,
        distance=180,
        description="A straight route through The Fields of The Dead. Rough terrain, no road.",
    ),
    Route(
        type=RouteType.LAND,
        start=BALDURS_GATE.id,
        end=FIELDS_OF_THE_DEAD.id,
        distance=120,
        description="A straight route through The Fields of The Dead. Rough terrain, no road.",
    ),
    Route(
        type=RouteType.LAND,
        start=TROLL_CLAWS.id,
        end=FIELDS_OF_THE_DEAD.id,
        distance=90,
        description="A straight route through The Fields of The Dead. Rough terrain, no road.",
    ),
]


DEFAULT_MAP = Map(
    locations=[SWORD_COAST, BALDURS_GATE, TROLL_CLAWS, FIELDS_OF_THE_DEAD],
    routes=ROUTES,
)
