# sentier_glossary

[![PyPI](https://img.shields.io/pypi/v/sentier_glossary.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/sentier_glossary.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/sentier_glossary)][pypi status]
[![License](https://img.shields.io/pypi/l/sentier_glossary)][license]

[![Read the documentation at https://sentier_glossary.readthedocs.io/](https://img.shields.io/readthedocs/sentier_glossary/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/Depart-de-Sentier/sentier_glossary/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Depart-de-Sentier/sentier_glossary/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/sentier_glossary/
[read the docs]: https://sentier_glossary.readthedocs.io/
[tests]: https://github.com/Depart-de-Sentier/sentier_glossary/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Depart-de-Sentier/sentier_glossary
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _sentier_glossary_ via [pip] from [PyPI]:

```console
$ pip install sentier_glossary
```

## Usage

There is a single class, `GlossaryAPI`, which wraps the [Sentier glossary API endpoints](https://api.g.sentier.dev/latest/docs#/):

```python
from sentier_glossary import GlossaryAPI, CommonSchemes
api = GlossaryAPI()
```

With this class, you can retrieve the collections (logical organization of concept schemes into products, processes, places, and units), [concept schemes](https://www.w3.org/TR/2005/WD-swbp-skos-core-guide-20051102/#secscheme), and [concepts](https://www.w3.org/TR/2005/WD-swbp-skos-core-guide-20051102/#secconcept). For example:

```python
> api.schemes()
[{'iri': 'http://data.europa.eu/z1e/icstcom2009/icst',
  'notation': 'ICST-COM 2009',
  'prefLabel': 'International Classification of Ship by Type (ICST-COM)',
  'scopeNote': ''},
...]
> [
>    concept
>    for concept in api.concepts_for_scheme('http://data.europa.eu/z1e/icstcom2009/icst')
>    if 'passenger' in concept['prefLabel'].lower()
> ]
[{'iri': 'http://data.europa.eu/z1e/icstcom2009/35',
  'identifier': '35',
  'notation': '35',
  'prefLabel': '35 Passenger ship',
  'altLabel': 'Passenger ship',
  'scopeNote': 'Ship categories included: passengers (excluding cruise passengers)...'},
 {'iri': 'http://data.europa.eu/z1e/icstcom2009/36',
  'identifier': '36',
  'notation': '36',
  'prefLabel': '36 Cruise Passenger',
  'altLabel': 'Cruise Passenger',
  'scopeNote': 'Ship categories included: cruise ships only '}]
> api.concept('http://data.europa.eu/z1e/icstcom2009/35')
{'iri': 'http://data.europa.eu/z1e/icstcom2009/35',
 'notation': '35',
 'prefLabel': '35 Passenger ship',
 'identifier': '35',
 'scopeNote': 'Ship categories included: passengers (excluding cruise passengers)...',
 'altLabel': 'Passenger ship',
 'concept_schemes': ['http://data.europa.eu/z1e/icstcom2009/icst'],
 'relations': []}
```

The Sentier glossary uses vocabularies built on [SKOS](https://www.w3.org/TR/2005/WD-swbp-skos-core-guide-20051102/), and uses SKOS terms like `prefLabel`, `altLabel`, `broader`, `narrower`, and `scopeNote`.

### Language of Results

The results returned from the API will depend on your language preferences. By default, the glossary client uses the default [language in your locale](https://en.wikipedia.org/wiki/Locale_(computer_software)). You can change it when instantiating the API:

```python
api = GlossaryAPI(language_code="fr")
```

Language codes follow [ISO 639-1](https://en.wikipedia.org/wiki/ISO_639-1), and are two lowercase letters, e.g. `en`, `es`, and `zh`.

You can also use `set_language_code()` to change the language of an existing `GlossaryAPI` client. For example:

```python
> api.set_language_code('fr')
> api.concept('http://data.europa.eu/z1e/icstcom2009/35')
{'iri': 'http://data.europa.eu/z1e/icstcom2009/35',
 'notation': '35',
 'prefLabel': '35 Passagers',
 'identifier': '35',
 'scopeNote': 'Catégories incluses dans chaque type de navire: Passagers (sauf passagers de navires de croisière)',
 'altLabel': 'Passagers',
 'concept_schemes': ['http://data.europa.eu/z1e/icstcom2009/icst'],
 'relations': []}
```

The default fallback language of the glossary is `en`.

### Semantic Search

The API search endpoint is under revision; for the time being we can use local semantic search. This only works with concept schemes given in `CommonSchemes`, currently:

* cn2024 (http://data.europa.eu/xsp/cn2024/cn2024)
* nace21 (http://data.europa.eu/ux2/nace2.1/nace2.1)
* low2015 (http://data.europa.eu/6p8/low2015/scheme)
* icst2009 (http://data.europa.eu/z1e/icstcom2009/icst)
* prodcom2023 (http://data.europa.eu/qw1/prodcom2023/prodcom2023)
* isic4 (https://unstats.un.org/classifications/ISIC/rev4/scheme)

To make a search query, pass the search query and the concept scheme. For example:

```python
> api.semantic_search("piggies", CommonSchemes.cn2024)
[[{'iri': 'http://data.europa.eu/xsp/cn2024/080291000080',
   'identifier': '080291000080',
   'notation': '0802 91 00',
   'prefLabel': '0802 91 00 -- Pignons, en coques',
   'altLabel': '-- Pignons, en coques',
   'scopeNote': 'Pignons, frais ou secs, en coques'}],
...]
```

The first time you run this it might take a while as it downloads the data needed for [semantic search](https://www.sbert.net/examples/applications/semantic-search/README.html), and vectorizes the API vocabularies.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [MIT license][License],
_sentier_glossary_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://sentier_glossary.readthedocs.io/en/latest/usage.html
[License]: https://github.com/Depart-de-Sentier/sentier_glossary/blob/main/LICENSE
[Contributor Guide]: https://github.com/Depart-de-Sentier/sentier_glossary/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/Depart-de-Sentier/sentier_glossary/issues
