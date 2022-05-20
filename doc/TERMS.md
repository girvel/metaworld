# Terms

## Meta ECS

- **Entity** is an object that is a direct part of the game world.
- **Attribute** is a python attribute of an entity holding some game data.
- **System** is a function-based entity that determines one kind of interaction between entities.
- **Metasystem** is a system that launches all other systems and handles adding/removing entities.

## Others

- **Intention** is an attribute starting with `will_`, that exists for a very short period of time and is used to transmit a signal between the systems.
