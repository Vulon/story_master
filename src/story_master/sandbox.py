from story_master.engine import Engine

# db = Memgraph(
#     host="localhost",
#     port=7687
# )


# class Character(Node):
#     name: str
#     description: str

# class Faction(Node):
#     name: str
#     description: str

# class PartOf(Relationship, type="PART_OF"):
#     pass

# john = Character(name="John", description="The first character")
# elves = Faction(name="Elves", description="The elves community")
# relation = PartOf(_start_node_id=john._id, _end_node_id=elves._id)

# db.execute("MATCH (n) DETACH DELETE n")


engine = Engine()
engine.run()
