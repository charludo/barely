# Blueprints

Back in the [Basics](/README.md/#basics), we have already briefly covered blueprints. They are pretty much exactly what you would expect: re-usable project templates that you can instantiate into new projects. Other frameworks might call them themes.

You can list all available blueprints with:
```console
$ barely blueprints
[barely][  core][ INFO] :: found 2 blueprints:
                        -> default
                        -> blank
```

The help menu hints at a way to also create your own blueprints:
```console
$ barely blueprints --help
Usage: barely blueprints [OPTIONS]

  list all available blueprints, or create a new one

Options:
  -n, --new TEXT  create a reusable blueprint from the current project
  --help          Show this message and exit.
```

Executing `barely blueprints --new "name"` will create a new blueprint out of your current project, and you can freely use it from now on:

```console
$ barely blueprints
[barely][  core][ INFO] :: found 3 blueprints:
                        -> name
                        -> default
                        -> blank
```

[< back](README.md)
