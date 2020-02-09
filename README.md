## Home Assistant sensor component for waste collectors in the Netherlands

Provides Home Assistant sensors for the Dutch waste collectors in
--Sliedrecht
- sliedrecht                        (does not support: restafval)

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

--Echt-Susteren
- dieteren                          (does not support: textiel, papier)
- echt                              (does not support: textiel, papier)
- koningsbosch                      (does not support: textiel, papier)
- maria hoop                        (does not support: textiel, papier)
- nieuwstadt                        (does not support: textiel, papier)
- pey                               (does not support: textiel, papier)
- roosteren                         (does not support: textiel, papier)
- sint joost                        (does not support: textiel, papier)
- susteren                          (does not support: textiel, papier)

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
      city: sliedrecht                 (required)
      postcode: 33361AB                (required)
      streetnumber: 1                  (required)
      dateformat: '%d-%m-%Y'           (optional)
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
If you wish to remove the year and the dashes and want to show the name of the month abbreviated, you would provide '%d %b'. Which will result in:
```yaml
21 Sep
```

