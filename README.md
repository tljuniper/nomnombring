# nomnombring

Nomnombring is a very simple adapter between a list of recipes (as json) and a
Bring! shopping list.

It includes a frontend, built with Vue.js, that presents a list of recipes.
The backend, built with Python and flask, consolidates the ingredients of all
selected recipes and adds them to Bring! via its API.

Can be deployed with nix (via NixOS module).

## Status

This is a Work in Progress!

TODOs include:

- [ ] Making the backend URL in the webapp configurable (is currently *always* `http://rust:5000`, can be changed in `frontend/public/config.json`)
- [ ] Adding a License
- [ ] Displaying the portions for each recipe in the web app
- [ ] Allowing the user to add an arbitrary number of portions

## backend: config.ini

The backend requires a config file with the following fields:

```ini
[DEFAULT]
recipe_file = path/to/bring_recipes.json

[BRING]
user = mail@example.com
password = super-secret-password
key = used-by-webapp-to-access-bring-api
```

## backend: bring_recipes.json

The recipes file has the following structure:

<!-- cspell: disable -->
```json
[
    {
        "title": "Saure Bohnensuppe",
        "portion": "4 Portionen",
        "time": "40 Minuten",
        "ingredients": [
            {
                "name": "Bohnen",
                "description": "breite",
                "amount": "500 g"
            },
            {
                "name": "Schinkenw\u00fcrfel",
                "description": "",
                "amount": "1"
            }
        ],
        "id": 1
    },
    {
        "title": "Mitternachtssuppe",
        "portion": "6 Portionen",
        "time": "40 Minuten",
        "ingredients": [
            {
                "name": "Gew\u00fcrzgurken",
                "description": "",
                "amount": "1 Glas"
            }
        ],
        "id": 2
    }
]
```
<!-- cspell: enable -->

## Build with nix

The standalone apps can be built with nix:

```sh
nix build .\#packages.x86_64-linux.nomnombring
nix build .\#packages.x86_64-linux.nomnombring-backend
```

On NixOS, the apps can be installed via the included NixOS module:

```nix
nomnombring.nixosModules.nomnombring
{
    tljuniper.services.nomnombring = {
        enable = true;
        configFile = "/var/nomnombring-config.ini";
    };
}
```

## Dev shells

With direnv installed and running:

```sh
cd frontend
npm run dev
```

```sh
cd backend
vim config.ini # fill out template
python3 .

# Or, to run with waitress:
waitress-serve --host 0.0.0.0 --port 5000 --call 'nomnombring.main:create_app'
```

Testing:

```sh
curl localhost:5000/recipes -X POST -d '[28]' -H "Content-Type: application/json"
```

## Initial setup for vue app

```sh
# Create template files
npm create vue@latest
# --> turn on vue-router and pinia but not eslint and vitest. Some dependencies
# didn't work with nix (yocto-queue), so we're trying to reduce the number of
# dependencies.
# Rename folder
mv nomnombring frontend
cd frontend
# Create node_modules/
npm install
# Create package-lock.json
npm run build
# With the package-lock.json in place, we can now run nix build
```

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar).

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).
