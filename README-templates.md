# Templates

This section must be included in the main README.md
somewhere.


### List available templates

```sh
kb template list
```

```sh
kb template list "theory"
```


### Create a new template

```sh
kb template new lisp-cheatsheets
```

### Delete a template

```sh
kb template delete lisp-cheatsheets
```

### Edit a template

```sh
kb template edit lisp-cheatsheets
```

### Add a template

To add a template from a toml configuration file, just do:
```sh
kb template add ~/path/to/myconfig.toml --title myconfig
```
