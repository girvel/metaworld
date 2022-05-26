# Terms

## Meta ECS

- **Entity** is an object that is a direct part of the game world. F. e., player's character is an entity.
- **Attribute** is a python attribute of an entity holding some game data. F. e., `player.alive` is an attribute.
- **System** is a function-based entity that determines one kind of interaction between entities. F. e., speech is a system.
- **Metasystem** is a system that launches all other systems and handles adding/removing entities.

## Others

- **Player** can be used as a short version of *player's character*
- **Intention** is an attribute starting with `will_`, that exists for a very short period of time and is used to transmit a signal between the systems. F. e., `player.will_go_to` is a player's intention.
- **Order** is an act of creation of a new intention. F. e., `player.will_talk_to = npcs.brian; player.will_talk_about = 'fight'` is an order to player to talk to brian about fight.
