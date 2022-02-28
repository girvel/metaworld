from lib.ecs import ecs


if __name__ == '__main__':
    ms = ecs.Metasystem()

    @ms.add
    @ecs.create_system
    def input_system():
        s = input("> ")
        print(f"You've said: '{s}'")

    ms.update()
