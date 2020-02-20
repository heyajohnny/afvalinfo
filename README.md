## Home Assistant sensor component for waste collectors in the Netherlands

If you like my work, please buy me a coffee. This will keep me awake :) 
<a href="https://www.buymeacoffee.com/1v3ckWD" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a>

Provides Home Assistant sensors for the Dutch waste collectors in:

--Boekel, Boxmeer, Buren, Cuijk, Culemborg, Echt-Susteren, Geldermalsen, Grave, Helmond, Lingewaal, Maasdriel, Mill en Sint Hubert, Neder-Betuwe, Neerijnen, Sint Anthonis, Son en Breugel, Terneuzen, Tiel, West Maas en Waal, Zaltbommel (does not support: textiel and in some places also not papier)
- aalst, alem, alphen, altforst, ammerzoden, appeltern, asperen, asch, axel, beers, beneden-leeuwen, beugen, beusichem, biervliet, boekel, boven-leeuwen, boxmeer, brakel, bruchem, buren, buurmalsen, cuijk, culemborg, delwijnen, dieteren, dodewaard, dreumel, echt, echteld, eck en wiel, erichem, est, gameren, geldermalsen, grave, groeningen, haaften, haps, hedel, heerewaarden, heesselt, hellouw, helmond, herwijnen, heukelem, hoek, hoenzadriel, holthees, hurwenen, ijzendoorn, ingen, kapel-avezaath, katwijk, kerk-avezaath, kerkdriel, kerkwijk, koewacht, koningsbosch, landhorst, langenboom, ledeacker, lienden, linden, maasbommel, maashees, maria hoop, maurik, mill, nederhemert-noord, nederhemert-zuid, neerijnen, nieuwaal, nieuwstadt, ochten, oeffelt, ommeren, ophemert, opheusden, opijnen, oploo, overloon, overslag, pey, philippine, poederoijen, ravenswaaij, rijkevoort, rijswijk, roosteren, rossum, sambeek, sas van gent, sint agatha, sint anthonis, sint hubert, sint joost, sluiskil, son en breugel, spijk, spui, stevensbeek, susteren, terneuzen, tiel, tuil, varik, velddriel, vierlingsbeek, vortum-mullem, vuren, waardenburg, wadenoijen, wamel, wanroij, well, wellseind, westerbeek, westdorpe, wilbertoord, zaamslag, zaltbommel, zoelen, zoelmond, zuiddorpe, zuilichem

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
timespanindays: 2
```

### Attributes
There are 3 important attributes:
-days_until_collection_date.    This will return the number of days between today and the collection date.
-is_collection_date_today.      This will return true if the collection date is today and false if the collection date is not today.
-hidden.                        This will return true on error or if the date is outside of range of the 'timespanindays' value. On any other occasion it will return true.
