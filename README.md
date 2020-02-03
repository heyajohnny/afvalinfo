## Home Assisant sensor component for Sliedrecht Afvalinfo

Provides Home Assistant sensors for the Dutch waste collector Sliedrecht Afvalinfo using a scraper.

### Install:
- Copy the files in the /custom_components/afvalinfo/ folder to: [homeassistant]/config/custom_components/afvalinfo/

Example config:
```Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:                       (at least 1 required)
        - pbd
      city: sliedrecht                 (required)
      postcode: 33361AB                (required)
      streetnumber: 1                  (required)
      dateformat: '%d-%m-%Y'           (optional)
```

Above example has 1 resource, but here is a complete list of available waste fractions:
- gft                                  (groente, fruit, tuinafval)
- textiel
- papier
- pbd                                  (plastic, blik, drinkpakken)

### Date format
```yaml
dateformat:
```
If you want to adjust the way the date is presented. You can do it using the dateformat option. All [python strftime options](http://strftime.org/) should work.
Default is '%d-%m-%Y', which will result in per example: 
```yaml
21-9-2019.
```
If you wish to remove the year and the dashes and want to show the name of the month abbreviated, you would provide '%d %b'. Which will result in: 
```yaml
21 Sep
```

### Add cities
The code is designed to add new cities relatively easy. Please create an issue in
https://github.com/heyajohnny/afvalinfo/issues to request a new city.
