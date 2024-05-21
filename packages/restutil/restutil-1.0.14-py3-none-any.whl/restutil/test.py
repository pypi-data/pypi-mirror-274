

monster = ["godzilla", "king kong"]
more_monster = ["cthulu"]

print(monster + more_monster)

monster.extend(more_monster)
monster.extend("la suegra")

print(monster)