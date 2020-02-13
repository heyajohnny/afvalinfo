## Home Assistant sensor component for waste collectors in the Netherlands

Provides Home Assistant sensors for the Dutch waste collectors in:

--Echt-Susteren                     (does not support: textiel, papier)
- dieteren
- echt
- koningsbosch
- maria hoop
- nieuwstadt
- pey
- roosteren
- sint joost
- susteren

--Sliedrecht                        (does not support: restafval)
- sliedrecht

--Twente Milieu                     (does not support: textiel)
- almelo
- borne
- enschede
- haaksbergen
- hengelo
- hof van twente
- losser
- oldenzaal
- wierden

--Vijfheerenlanden
- ameide
- everdingen
- hagestein
- hei- en boeicop
- hoef en haag
- kedichem
- leerbroek
- leerdam
- lexmond
- meerkerk
- nieuwland
- oosterwijk
- ossenwaard
- schoonrewoerd
- tienhoven aan de lek
- vianen
- zijderveld

Not yet supported cities:

--Westland                          (does not support: pbd, textiel)
- de lier
- s-gravenzande
- honselersdijk
- kwintsheul
- maasdijk
- monster
- naaldwijk
- poeldijk
- ter heijde
- wateringen

### Add cities
The code is designed to add new cities relatively easy.
Please create an issue in https://github.com/heyajohnny/afvalinfo/issues to request a new city.
If there are any problems with the component, don't hesitate to create an issue here: https://github.com/heyajohnny/afvalinfo/issues

### Install:
- Copy the files in the /custom_components/afvalinfo/ folder to: [homeassistant]/config/custom_components/afvalinfo/

Example config:
```Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:                       (at least 1 required)
        - pbd
      city: sliedrecht                 (required, default = sliedrecht)
      postcode: 33361AB                (required, default = 3361AB)
      streetnumber: 1                  (required, default = 1)
      dateformat: '%d-%m-%Y'           (optional, default = %d-%m-%Y) day-month-year
      timespanindays: 365              (optional, default = 365) number of days to look into the future
```

Above example has 1 resource, but here is a complete list of available waste fractions:
- gft                                  (groente, fruit, tuinafval)
- papier
- pbd                                  (plastic, blik, drinkpakken)
- restafval
- textiel



### Date format
```yaml
dateformat:
```
If you want to adjust the way the date is presented. You can do it using the dateformat option. All [python strftime options](http://strftime.org/) should work.
Default is '%d-%m-%Y', which will result in per example:
```yaml
21-9-2019.
```
### Timespan in days
```yaml
timespanindays:
```
If you only want to see data 2 days ahead of today. You can do it using the timespanindays option. (The default value is 365 days)
```yaml
dateformat: 2
```