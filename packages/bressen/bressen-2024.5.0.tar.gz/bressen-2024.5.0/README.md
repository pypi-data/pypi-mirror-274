# Bressen
Voor het werken met bressen


## Python environment
Bressen gebruikt een recente versie (maart 2024) van **geopandas** en een versie van **shapely** en **pandas** groter dan 2.0. De module **pyogrio** wordt gebruikt voor het efficient lezen en schrijven van GeoPackages.

Wij bevelen het gebruik van **Mamba** aan voor het bouwen van Python-environments. Voor het installeren van **MicroMamba**, zie prefix.dev: https://prefix.dev/docs/mamba/overview#installation.

Een `environment.yml` bestand moet in ieder geval de volgende inhoud bevatten:

```yaml
channels:
  - conda-forge
 
dependencies:
  - python<1.13
  - geopandas
  - pandas>2.0
  - pyogrio
  - shapely>2.0
```

Met deze environment.yml en MicroMamba bouw je je environment (we gebruiken hier de naam `bressen`) vanaf de command-line met:

```cmd
micromamba env create -f environment.yml -n bressen
```

## Installatie bressen module
Clone deze repository of download de main-branch lokaal. Vanuit de geactiveerde environment (in dit voorbeeld `micromamba activate bressen`) en de module-folder (waar je `pyproject.toml` vindt) installeer je de bressen-module via de command-line met:

```cmd
pip install .
```

Wanneer je de module hebt gecloned én wilt kunnen bijwerken via Git of GitHub Desktop, kun je de module ook in edit-mode linken aan je Python-environment door:

```cmd
pip install -e .
```

Nu kun je wijzigingen van de module eenvoudig opnemen door de repository bij te werken. En beter nog, actief bijdragen aan de (door)ontwikkeling van deze module!

## Credits
Bressen is ontwikkeld door [D2Hydro](https://d2hydro.nl/) in opdracht van [Waternet](https://www.waternet.nl/) en Open Source beschikbaar onder een [MIT licentie](https://github.com/d2hydro/bressen?tab=MIT-1-ov-file)
