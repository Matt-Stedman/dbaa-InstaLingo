[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

# dbaa-InstaLingo
A DuoLingo hack on Instagram (for Don't Build an App!).

## Usage

1. Make an [instagram account](https://www.instagram.com/accounts/emailsignup/) (if you don't already have one you're happy to use)
2. Make a [DeepL API account[(https://www.deepl.com/en/docs-api) (it's free!) 
3. Create a "secrets.toml" file containing:

```toml
[INSTAGRAM]
USER = <YOUR_USERNAME>
PASS = <YOUR_PASSWORD>

[DEEPL]
AUTH_KEY = <YOUR_DEEPL_AUTH_KEY>
```

4. Run the code in Python 3.8 or higher.

## Features

Sets translation tasks and responds to your answers. More details on the [Don't Build an App website](https://dont-build-an-app.super.site/better-duolingo-but-on-instagram)
