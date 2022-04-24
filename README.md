# <img src="https://i.imgur.com/dk2jDwY.png" alt="drawing" width="100"/> Survival Machine


![Licence - Loading error (referesh)](https://img.shields.io/github/license/artsergy/survivalmachine) ![GitHub last commit - Loading error (referesh)](https://img.shields.io/github/last-commit/artsergy/survivalmachine)

A script to model interspecies interactions in a simplified environment. Inspired by Richard Dawkins' book "The Selfish Gene".

![Sample gif](https://i.imgur.com/F1KTE19.png)

# Usage

It seems to me that the code is quite self-explanatory and setting your own specifications should not be difficult

```python
map1 = Map(500)
map1.populate_map(Dove, 10)
map1.populate_map(Hawk, 10)
map1.populate_map(Goose, 10)
map1.populate_map(Parrot, 10)
map1.populate_map(Penguin, 10)
map1.populate_map(Puffin, 10)
map1.populate_map(Dodo, 10)
map1.simulate(300)

map1.plot_data("Example", False)
```


