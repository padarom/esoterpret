# ![Esoterpret](http://i.imgur.com/nNAfkuz.png)
Esoterpret is an extensible esoteric programming language interpreter written in Python. It features a modular setup, debugging features and more. _Contribution is well appreciated!_

I'm currently looking into using PyQt with the project so it can use a graphical user interface instead of the previously planned text-based command-line one. It will still be possible to use the interpreters using the command line, but without the debugging features.

## Feature Set
_Esoterpret is still under active development and by no means finished. These features do not only represent implemented features, but also ones that are still to come (or that might never come at all)._
- Run code in multiple esoteric programming languages using one tool
- Create your own interpreters and incorporate them using the module system
- Debug your code step by step (if supported by interpreter)
- Codegolf Challenge Mode
  - Define test suits with inputs and expected outputs
  - Add golfed code
  - Test every code, verify its validity (with your test suit) and sort by lowest byte count

## Currently Supported Languages
- [Mornington Crescent][Mornington Crescent]

You're free to add your own interpreters if you want to and file a pull request for them. Our contribution guide will help get you started! (_Coming Soon!_)

We're also planning to add the ability to incorporate external interpreters/compilers. They will not necessarily contain the complete feature set offered by Esoterpret, but can still be run by it.

## How to use
Esoterpret requires Python 3. Just download the repository (or clone it) and run `esoterpret.py`:
```sh
$ python esoterpret.py --help
```

Interpreters for specific languages can be found in the `modules` directory. Using the parameter `--list-languages` you can list all languages that include a valid config file:

```sh
$ python esoterpret.py --list-languages
- Brainfuck (brainfuck)
- Mornington Crescent (morningtoncrescent)
```

To run a program, you need to specify the language and the path to the scriptfile:

```sh
$ python esoterpret.py -l morningtoncrescent modules/morningtoncrescent/examples/hello-world.mcresc
Hello, World!
```

[Mornington Crescent]: http://esolangs.org/wiki/Mornington_Crescent
