# DjangoCMS FAQ

Frequently asked questions plugin for Django CMS, with an API to load questions from another page!

## Install

1) Install module
   ```bash
   python3 -m pip install djangocms-faq
   ```
   > *Or use this command if you want to add a scoop of [fuzzy-search](#fuzzy-search) in your api:*
   > ```bash
   > python3 -m pip install djangocms-faq[fuzzy_search]
   > ```

2) Add it to your INSTALLED_APPS
   ```
       "djangocms_faq",
   ```

3) Add the API endpoint to your `urls.py` (if you want to use the Faq Search Plugin):
    ```python
        path("djangocms-faq/", include("djangocms_faq.urls")),
    ```

4) Launch your django-cms site, it should be here!

    ![](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/4d774d9e28e4125db633e80234569c2e/image.png)

### Requirements

* `django-cms`: Obviously.
* `django-sekizai`: For default templates (you can uninstall it if you use custom templates without sekizai). Not required in this package (it's a requirement of django-cms).
* [`thefuzz`](https://github.com/seatgeek/thefuzz): If you want to use fuzzy search, optional package.

## Features

### A faq

Add **FAQ Container**s plugins, which have a (hidden and required) name, a (public and optional) title, and can only contain **FAQ Question**s plugins.

![FAQ Container](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/b0b09bd08013029675cff56b766be2f3/image.png)

Then, add **FAQ Question**s plugins that can contain text/image/videos plugins (that provide answers)!

![FAQ Question](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/3efc80d49da74b4f70550da8b8d51e3b/image.png)

You can also add keywords to your FAQ questions, because you may want your users to find a specific answer to a general question.

*You* can *create an alias of a Question and paste if where you want, but it is more coherent to copy the whole Faq Container, or tu put a search bar.*

It is discouraged to create a FAQ on a non-cms page (like a djangocms-blog post) : the search function will *not* work (this plugin does not know how to get the current url if it's not on a placeholder that's on a cms page object).

### A search plugin that uses an API

Ask a question to the FAQ and the plugin will return with the corresponding questions/answers.

*Quick note: since the form uses javascript **and** a simple view, that means that the search works without javascript too!*

*Another quick note: The search results will not include results from aliased plugins, it will only link to original questions.*


### Select in which FAQ the searches will be applied

![Select faq to search into](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/75a02eff991e2f8b3b2221f9fd80d50d/image.png)

Display format is `{FAQ Name} ({Page title})`.

### Fuzzy search!

Users can make mistakes. So this package can use the `token_sort_ratio` function from the package [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy#token-sort-ratio) to return str that are at least (>=) 85% the same (you can change the number).

To activate it, simply install the package like this:

```bash
python3 -m pip install djangocms-faq[fuzzy_search]
```

And add this to your settings :

```python
DJANGOCMS_FAQ_ENABLE_FUZZY_SEARCH = True
```

#### Query detection in question title is still used when fuzzy search is enabled:

![](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/c4fc8952248b9f7481ec3d9a466cbe06/image.png)

#### Fuzzy search:

![](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/7c8ded0983cf32ac2253430a6c229d37/image.png)

Here, "this long string" match "that long string" at [87%](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/98e58ce1b212c76898927c86b0938b2e/image.png), so the question is returned.

## Configuration

* `DJANGOCMS_FAQ_ENABLE_API` (default is `True`): Enable or not the API endpoint and the Faq Search plugins.

    *If you create a Faq Search Plugin and then set this setting to `False`, then you will be greeted with a cool `KeyError 'FaqPluginSearchPublished'` error message. Please do not do this.*

* `DJANGOCMS_FAQ_MAX_QUERY_LENGTH` (default is `60`): Max size of a query to the api. The module will truncate user requests to `DJANGOCMS_FAQ_MAX_QUERY_LENGTH` chars.

* `DJANGOCMS_FAQ_ANSWER_PLUGINS` (default is `["TextPlugin", "FilePlugin", "VideoPlayerPlugin"]`): Add plugins that can be added to your answers!

* `DJANGOCMS_FAQ_SHOW_KEYWORDS_QUESTION` (default is `True`): Display keywords in the questions of a FAQ.

* `DJANGOCMS_FAQ_SHOW_KEYWORDS_ANSWER` (default is `True`): Display keywords in answers (faq search plugin).

* `DJANGOCMS_FAQ_ENABLE_FUZZY_SEARCH` (default is `False`): Wanna use fuzzy search ? (*see [fuzzy-search](#fuzzy-search)*)

* `DJANGOCMS_FAQ_FUZZY_SEARCH_PERCENTAGE` (default is `85`): Score to reach before returning a match between two patterns (query/question or query/keyword) from the api.

* `DJANGOCMS_FAQ_SEARCH_WORD_BY_WORD_KEYWORDS` (default is `False`): If you want to split user queries & keywords in order to return a question if at least *one word* from the query is the same of at least *one word* of it's keywords.

----

[Here's a screenshot](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/ccf1ac04872830729fb6cdae5c77dd5b/image.png) with different examples (configs: `DJANGOCMS_FAQ_ENABLE_FUZZY_SEARCH` and `DJANGOCMS_FAQ_SEARCH_WORD_BY_WORD_KEYWORDS`):


*Warning! Do not use stopwords in keywords, or else you might get [a looot](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/841416fdc4351433e6bafccf8de0426b/image.png) of results!*

## API

When you're searching for something in the input, searches will be made using the API if you don't type anything for 1 second (see `templates/faq_search.html`).

Here's the format:

```json
[
  {
    "question": "question title",
    "slug": "question-title",
    "url": "/page-url/",
    "keywords": ["keyword", "another keyword", "..."]
  },
  {
    "question": "question title 2",
    "slug": "question-title2",
    "url": "/page-url/",
    "keywords": ["keyword", "an other key word", "..."]
  },
]
```

### Api format

```
djangocms-faq/?question=keyword&search_in=aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaaa%20bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbbb&draft=True
```

Where `keyword` is a string, the `uuid`s are valid uuids (strings) of FAQs separated by spaces, and `draft` is the faq to search into (draft or live version of the CMSPlugin).

You can submit requests without the draft parameter, the script will then search only in published (live) version of each faq CMSPlugin (like `draft=False`).


## Customize it!

The templates included in this project are for demonstration purposes only, it is up to you to integrate them into your graphic charter by creating `faq_plugin.html`, `faq_question.html` and `faq_search.html` files in `templates/faq/`.

## How it works

Faq container & questions are classic django-cms plugins, see in `cms_plugins.py` for more informations.

Faq search plugin is a django-cms plugin, and uses on top of that an API endpoint using vanilla javascript (the default template uses `fetch`, which is [not compatible](https://caniuse.com/fetch) with IE).

The API endpoint is a single view that returns json (see `views.py`).

Since the function to get answers from a "question" str is used two times (in the view for the API and in the FaqPluginSearchPublisher plugin), I've put it in a file named `utils.py`.

When using fuzzy search mode, results are returned if the query is a substring of a question, or if the score between the question and the query or a keyword and the query is >= to `DJANGOCMS_FAQ_FUZZY_SEARCH_PERCENTAGE` (default = 85%).

When you publish a page containing a FAQ used in a search form, the `copy_relations` function will update the id of the FAQ using the class named `RelationSearchFaq` (that store the uuids of `FaqPluginModel` & `SearchFaqPluginModel`).

[Here's a bad drawing](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/0870375fc3805ac87296b9f1945adefc/image.png) of the problem, and [here's another bad drawing](https://gitlab.com/kapt/open-source/djangocms-faq/uploads/6bc8e88f2fd7b9af42ff695d260ccd50/image.png) of the current solution.

It's a custom and *dirty* solution to the problem of handling relations *between* CMSPlugins.

> It is much harder to manage the copying of relations when they are from one plugin to another.
>
> *source: Django-cms doc, [
Handling Relations > Relations between plugins](https://docs.django-cms.org/en/latest/how_to/custom_plugins.html#relations-between-plugins)*.
