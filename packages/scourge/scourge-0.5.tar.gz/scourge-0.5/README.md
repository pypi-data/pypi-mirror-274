# scourge

scourge, named after a group of starlings, lets you get summary tracking
information from various carriers.  currently supported carriers:

* ups
* fedex
* pilot
* metropolitan
* non-stop delivery

used for wismo and wigmo.  powered by angry penguins.

# notes

* the summary tracking results are limited to dates because the ups api 
  only provides localized date/time information and does not provide time
  zone information
* the ups api does not provide invoice information 

# contributing

## getting started

```bash
git clone git@github.com:angry-penguins/scourge
make setup
```

to test you will need an aws sso profile for `angry_penguins` in your aws 
config.  you can read more about the sso setup in confluence.

```bash
aws configure --profile=angry_penguins set region us-east-2
```
