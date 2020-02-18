## Home Assistant sensor component for waste collectors in the Netherlands

Provides Home Assistant sensors for the Dutch waste collectors in:

--Boekel, Boxmeer, Buren, Cuijk, Culemborg, Echt-Susteren, Geldermalsen, Grave, Helmond
(does not support: textiel and in some places also not papier)
- asch, beers, beugen, beusichem, boekel, boxmeer, buren, buurmalsen, cuijk, culemborg, dieteren,
echt, eck en wiel, erichem, geldermalsen, grave, groeningen, haps, helmond, holthees, ingen,
kapel-avezaath, katwijk, kerk-avezaath, koningsbosch, lienden, linden, maashees, maria hoop, maurik,
nieuwstadt, oeffelt, ommeren, overloon, pey, ravenswaaij, rijkevoort, rijswijk, roosteren, sambeek,
sint agatha, sint joost, susteren, vianen, vierlingsbeek, vortum-mullem, zoelen, zoelmond

--Sliedrecht                        (does not support: restafval)
- sliedrecht

--Twente Milieu                     (does not support: textiel)
- almelo, borne, enschede, haaksbergen, hengelo, hof van twente, losser, oldenzaal, wierden

--Vijfheerenlanden
- ameide, everdingen, hagestein, hei- en boeicop, hoef en haag, kedichem, leerbroek, leerdam,
lexmond, meerkerk, nieuwland, oosterwijk, ossenwaard, schoonrewoerd, tienhoven aan de lek,
vianen, zijderveld

--Westland                          (does not support: pbd, textiel)
- de lier, s-gravenzande, honselersdijk, kwintsheul, maasdijk, monster, naaldwijk, poeldijk,
ter heijde, wateringen

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

### Attributes
There are 3 important attributes:
-days_until_collection_date.    This will return the number of days between today and the collection date.
-is_collection_date_today.      This will return true if the collection date is today and false if the collection date is not today.
-hidden.                        This will return true on error or if the date is outside of range of the 'timespanindays' value. On any other occasion it will return true.