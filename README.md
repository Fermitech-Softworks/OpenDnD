# `rasanahal` (Royalnet version)

This pack is a port of `rasanahal-backend` from plain Starlette to Royalnet Starlette.

## Developing `rasanahal`

To develop `rasanahal`, you need to have [Poetry](https://poetry.eustace.io/) installed on your PC.

After you've installed Poetry, clone the git repo with the command:

```
git clone https://github.com/Fermitech-Softworks/rasanahal-backend
```

Then enter the new directory:

```
cd rasanahal-backend
```

Now, install all the dependencies:

```
poetry install
```

Finally, enter the poetry virtualenv and run the Royalnet server:

```
poetry shell
python -m royalnet -c config.toml
```

The webserver should be available at http://127.0.0.1:44445; documentation for the enabled API methods should be at http://127.0.0.1:44445/docs.
