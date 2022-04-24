import abc
from enum import IntEnum
import random
import matplotlib.pyplot as plt, mpld3
from tqdm import tqdm


class Outcome(IntEnum):
    WIN = 75
    DRAW = 65
    LOSS = -25
    BIG_LOSS = -65
    WAITING = -200


colors = {
    "Dove": "blue",
    "Hawk": "red",
    "Parrot": "green",
    "Goose": "orange",
    "Puffin": "purple",
    "Penguin": "black",
    "Dodo": "pink",
}


def get_birds_list(specie, sample_size):
    return [specie() for _ in range(sample_size)]


class SM:

    def __str__(self):
        return type(self).__name__ + ": " + str(self.points)

    def __init__(self, points=0, temperature_vul=1, humidity_vul=1):
        self.points = points
        self.temperature_vul = temperature_vul
        self.humidity_vul = humidity_vul

    @abc.abstractmethod
    def get_strategy(self, opponent) -> bool:
        return

    def assign_points(self, gain: Outcome, opponent_move):
        self.points += gain

    def death(self):
        return self.points <= -100

    def reproduction(self):
        if self.points >= 100:
            self.points = 0
            return True
        else:
            return False


class Dove(SM):

    def get_strategy(self, opponent):
        return False


class Hawk(SM):

    def get_strategy(self, opponent):
        return True


class Parrot(SM):

    def __init__(self):
        super().__init__()
        self.last_encounter = False

    def get_strategy(self, opponent):
        return self.last_encounter

    def assign_points(self, gain: Outcome, opponent_move):
        super().assign_points(gain, opponent_move)
        if opponent_move is not None:
            self.last_encounter = opponent_move


class Goose(Parrot):

    def get_strategy(self, opponent):
        return not self.last_encounter


class Puffin(SM):

    def get_strategy(self, opponent) -> bool:
        if type(opponent) != Puffin:
            return random.random() < 0.1

        return type(opponent) != Puffin


class Penguin(SM):

    def get_strategy(self, opponent) -> bool:
        return bool(random.randint(0, 1))


class Dodo(Parrot):

    def get_strategy(self, opponent):
        random_bird = random.choice(all_species)()
        if type(random_bird) == Parrot or type(random_bird) == Goose:
            random_bird.last_encounter = self.last_encounter

        return random_bird.get_strategy(opponent)


all_species = [Dove, Hawk, Parrot, Goose, Puffin, Penguin, Dodo]


class Map:

    def __init__(self, map_size):
        self.map_size = map_size
        self.bird_list = []
        self.population_history = {bird.__name__: [] for bird in all_species}
        self.dead = set()
        self.new_birds = []
        self.population = self.get_population()

    def get_population(self):
        populations = {}

        for bird_type in all_species:
            populations[bird_type.__name__] = 0

        for bird in self.bird_list:
            bird_name = type(bird).__name__
            if bird_name not in populations:
                populations[bird_name] = 0
            populations[bird_name] += 1

        return populations

    def populate_map(self, species, count):
        self.bird_list += get_birds_list(species, count)

    def simulate(self, simulation_time):
        for day in tqdm(range(simulation_time)):
            random.shuffle(self.bird_list)
            for i in range(min(self.map_size, len(self.bird_list) // 2)):
                bird1 = self.bird_list[2 * i]
                bird2 = self.bird_list[2 * i + 1]

                fight(bird1, bird2)

            for bird in self.bird_list[self.map_size:]:
                bird.assign_points(Outcome.WAITING, None)

            self.dead = set()
            self.new_birds = []

            for i, bird in enumerate(self.bird_list):
                if bird.death():
                    self.dead.add(i)
                elif bird.reproduction():
                    self.new_birds.append(type(bird)())

            self.bird_list = [bird for i, bird in enumerate(self.bird_list) if i not in self.dead] + self.new_birds
            self.population = self.get_population()
            for bird_name, bird_population in self.population.items():
                self.population_history[bird_name].append(bird_population)

    def plot_data(self, title="Default title", interactive=False):

        for species, population in self.population_history.items():
            plt.plot(range(len(population)), population, label=species, color=colors[species])

        plt.legend(loc="upper left")
        plt.title(title)
        if interactive:
            mpld3.show()
        else:
            plt.show()


def fight_outcome(does_fight1: bool, does_fight2: bool):
    if not does_fight1 and not does_fight2:
        return Outcome.DRAW, Outcome.DRAW
    if does_fight1 and does_fight2:
        return Outcome.BIG_LOSS, Outcome.BIG_LOSS
    if does_fight1 and not does_fight2:
        return Outcome.WIN, Outcome.LOSS
    if not does_fight1 and does_fight2:
        return Outcome.LOSS, Outcome.WIN


def fight(bird1: SM, bird2: SM):
    strategy1 = bird1.get_strategy(bird2)
    strategy2 = bird2.get_strategy(bird1)
    outcome1, outcome2 = fight_outcome(strategy1, strategy2)
    bird1.assign_points(outcome1, strategy2)
    bird2.assign_points(outcome2, strategy1)


map1 = Map(500)
map1.populate_map(Dove, 10)
map1.populate_map(Hawk, 10)
map1.populate_map(Goose, 10)
map1.populate_map(Parrot, 10)
map1.populate_map(Penguin, 10)
map1.populate_map(Puffin, 10)
map1.populate_map(Dodo, 10)
map1.simulate(300)

map1.plot_data("Default Title")
