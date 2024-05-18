# Game Generators

Game Generators (gage) is a package for efficiently generating games for research and experimentation. It is loosely
based
on [GAMUT](http://gamut.stanford.edu/). Its main features are:

1. Efficiently generate batches of games from a wide range of available game structures that can be used for deep
   learning purposes.
2. Sample random utility functions of widely used classes, such as concave functions, monotonically
   increasing/decreasing functions and more.
3. In-depth documentation that provides references to the literature.
4. Extensive test suite to verify the correctness of the generated games.

## Installation

You can install the package using pip:

```bash
pip install game-generators
```

## Quickstart

To start generating games, simply import the package and use the game generator that you desire. For example, to
generate a batch of 10 Bach-Stravinsky games, use the following code:

```python
import game_generators as gage

# Generate a batch of Bach-Stravinsky games directly.
batch_size = 10
payoff_matrices = gage.nfg.bach_stravinsky(batch_size)
print(payoff_matrices.shape)

# Or alternatively through the generic interface.
payoff_matrices = gage.generate_nfg("bach_stravinsky", batch_size)
print(payoff_matrices.shape)

```

To see all available game generators, see the [documentation](https://wilrop.github.io/gage/) or
check ``gage.available_games``.

## Format

Every game is returned with separate payoff tensors per player. For example, when generating a batch of 10 games with 2
players and 3 actions per player, we return a (10, 2, 3, 3) tensor where the first dimension contains the batch, the
second dimension contains a payoff tensor for an individual player, and the remainder is the joint action dimension.

It is common in game theoretic research to present joint payoff tensors. We provide a function to convert the separate
payoff tensors to a joint payoff tensor. This function is called `to_joint_payoff` and is available in
the `utils.transforms` module. In the example above, it would return a (10, 3, 3, 2) tensor.

## Contributing

We are building a suite of game generators that can be used in modern game theoretic research. If you are working in
this area and want to get involved, contributions are very welcome! For major changes, please open an issue first to
discuss what you would like to change.

## Citation

If you use GAGE in your research, please use the following BibTeX entry:

```
@misc{ropke2023gage,
  author = {Willem Röpke},
  title = {Gage: Game Generators},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/wilrop/mo-game-theory}},
}
```

## License

This project is licensed under the terms of the MIT license.