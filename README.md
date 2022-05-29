# Metaworld

Metaworld is a non-visual novel - an RPG with quest/novel-like text interface. The game focuses on writing/programming-driven features.

## Features

- Open world
- You can talk to people
- People can talk to you

# Manual installation

1. Download [zip-archive with source code](https://github.com/girvel/metaworld/archive/refs/heads/master.zip)
2. Extract it
3. Install python 3.10
4. Install requirements with 
   ```bash
   py -3.10 -m pip install -r requirements.txt
   ```
6. Launch the game with 
   ```
   py -3.10 -O metaworld.py
   ``` 
   (`-O` is used to optimize performance and disable debugging features)

Now you can launch the game with launch.bat.

# What tech is used

- [My own interpretation](https://github.com/girvel/ecs) of ECS pattern
- YAML to configure NPCs and locations
- Python as a scripting language and as a main language
