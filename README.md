## Home Assistant sensor component for waste collectors in the Netherlands
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
### Number of supported 'gemeenten' in The Netherlands: 326,5 of 352 = 92,75%

If you like my work, please buy me a coffee. This will keep me awake :)

<a href="https://www.buymeacoffee.com/1v3ckWD" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a>

Please take a look at the <a href="https://play.google.com/store/apps/details?id=com.viezegeitafval" target="_blank">Vieze Geit</a> Android app for trash pickup dates on your Android device.

#### Provides Home Assistant sensors for the Dutch waste collectors in:

##### -- Alkmaar
##### -- Alphen aan den Rijn
##### -- Beesel
##### -- Berkelland
##### -- Borsele
##### -- Cranendonck
##### -- Den Haag
##### -- Drimmelen
##### -- Goeree-Overflakkee
##### -- Hoeksche Waard
##### -- Katwijk
##### -- Midden-Drenthe
##### -- Peel en Maas
##### -- Purmerend, Beemster
##### -- Schouwen-Duiveland
##### -- Sliedrecht
##### -- Uden
##### -- Veldhoven
##### -- Venlo
##### -- Venray
##### -- Waalre
##### -- Westerkwartier
##### -- Westerwolde
##### -- Westland
##### --(Afvalstoffendienstkalender) Haaren, Heusden, Oisterwijk, s-Hertogenbosch, Vught
##### --(Avalex) Delft, Leidschendam-Voorburg, Midden-Delfland, Pijnacker-Nootdorp, Rijswijk, Wassenaar
##### --(Blink) Asten, Deurne, Gemert-Bakel, Heeze-Leende, Laarbeek, Nuenen, Someren
##### --(Circulus-Berkel) Apeldoorn, Bronckhorst, Brummen, Deventer, Doesburg, Epe, Lochem, Voorst, Zutphen
##### --(Cyclus) Bodegraven-Reeuwijk, Gouda, Kaag en Braassem, Krimpenerwaard, Montfoort, Nieuwkoop, Waddinxveen, Zuidplas
##### --(Dar) Berg en Dal, Beuningen, Druten, Heumen, Nijmegen, Wijchen
##### --(De Fryske Marren) De Friese Meren
##### --(DeAfvalApp) Boekel, Boxmeer, Buren, Cuijk, Culemborg, Echt-Susteren, Grave, Helmond, Maasdriel, Mill en Sint Hubert, Neder-Betuwe, Sint Anthonis, Son en Breugel, Terneuzen, Tiel, West Betuwe, West Maas en Waal, Zaltbommel
##### --(GAD) Blaricum, Gooise Meren, Hilversum, Huizen, Laren, Weesp, Wijdemeren
##### --(Groningen) Groningen, Het Hogeland BW(Bedum, Winsum), Loppersum
##### --(HVC) Alblasserdam, Bergen, Beverwijk, Den Helder, Dordrecht, Drechterland, Enkhuizen, Hendrik-Ido-Ambacht, Heemskerk, Hollands Kroon, Hoorn, Koggenland, Lelystad, Medemblik, Noordoostpolder, Opmeer, Papendrecht, Schagen, Stede Broec, Velsen, Wormerland, Zaanstad, Zeewolde, Zwijndrecht
##### --(Irado) Capelle aan den IJssel, Rotterdam Rozenburg, Schiedam, Vlaardingen
##### --(MijnAfvalWijzer) AA en Hunze, Alphen-Chaam, Assen, Altena, Amstelveen, Baarle-Nassau, Barneveld, Beek, Bergeijk, Bergen op Zoom, Bernheze, Best, Bladel, Borger-Odoorn, Boxtel, Breda, Brielle, Castricum, De Ronde Venen, De Wolden, De Bilt, Doetinchem, Dongen, Dronten, Duiven, Eersel, Eindhoven, Elburg, Ermelo, Etten-Leur, Geertruidenberg, Geldrop-Mierlo, Gilze en Rijen, Goirle, Halderberge, Harderwijk, Heerhugowaard, Heiloo, Hilvarenbeek, Horst aan de Maas, Houten, Kampen, Krimpen aan den IJssel, Langedijk, Lansingerland, Leiden, Leiderdorp, Leudal, Leusden, Lingewaard, Loon op Zand, Lopik, Maasgouw, Meierijstad, Midden-Groningen, Moerdijk, Nijkerk, Noordenveld, Nunspeet, Oirschot, Oldambt, Oldebroek, Oosterhout, Oss, Oude IJsselstreek, Oude Pekela, Putten, Oudewater, Overbetuwe, Rheden, Rhenen, Rijssen-Holten, Roerdalen, Roermond, Roosendaal, Rotterdam, Rucphen, Scherpenzeel, Sint-Michielsgestel, Sittard-Geleen, Smallingerland, Stadskanaal, Stein, Stichtse Vecht, Teylingen, Tilburg, Tynaarlo, Uitgeest, Utrecht, Utrechtse Heuvelrug, Valkenswaard, Veendam, Waalwijk, Waterland, Wijk bij Duurstede, Westervoort, Westvoorne, Woensdrecht, Woerden, Zevenaar, Zoetermeer, Zoeterwoude  ###### WARNING! Might not work well at the end of the year / beginning of the next year
##### --(Omrin) Achtkarspelen, Ameland, Appingedam, Dantumadeel(Ferwerderadiel), Harlingen, Heerenveen, Het Hogeland(De Marne, Eemsmond), Leeuwarden, Noardeast Fryslan, Ooststellingwerf, Opsterland, Terschelling, Tietjerksteradeel, Waadhoeke, Weststellingwerf
##### --(Rd4) Beekdaelen, Brunssum, Eijsden-Margraten, Gulpen-Wittem, Heerlen, Kerkrade, Landgraaf, Maastricht, Meerssen, Simpelveld, Vaals, Valkenburg aan de Geul, Voerendaal  ###### WARNING! Might not work well at the end of the year / beginning of the next year
##### --(Rmn) Baarn, Bunnik, IJsselstein, Nieuwegein, Soest, Zeist
##### --(Rova) Aalten, Amersfoort, Bunschoten, Dalfsen, Dinkelland, Hardenberg, Hattem, Heerde, Olst-Wijhe, Ommen, Oost Gelre, Raalte, Staphorst, Steenwijkerland, Tubbergen, Twenterand, Urk, Westerveld, Winterswijk, Woudenberg, Zwartewaterland, Zwolle  ###### WARNING! Might not work well at the end of the year / beginning of the next year
##### --(Spaarnelanden) Haarlem, Zandvoort
##### --(Suez) Arnhem
##### --(Súdwest-Fryslân) Zuidwest-Friesland
##### --(Ximmio) Aalsmeer, Albrandswaard, Almelo, Almere, Barendrecht, Bloemendaal, Borne, Coevorden, Diemen, Ede, Emmen, Enschede, Gorinchem, Haaksbergen, Haarlemmermeer, Hardinxveld-Giessendam, Heemstede, Hellendoorn, Hengelo, Hillegom, Hof van Twente, Hoogeveen, Lisse, Losser, Meppel, Molenlanden, Nissewaard, Noordwijk, Oldenzaal, Renkum, Renswoude, Ridderkerk, Veenendaal, Vijfheerenlanden, Wageningen, Wierden
##### --(Zrd) Hulst, Kapelle, Noord-Beveland, Reimerswaal, Sluis, Tholen, Veere

### Add 'gemeente'
The code is designed to add new 'gemeenten' relatively easy.
Please create an issue in https://github.com/heyajohnny/afvalinfo/issues to request a new 'gemeente'.
If there are any problems with the component, don't hesitate to create an issue here: https://github.com/heyajohnny/afvalinfo/issues

### Install:
- Copy the files in the /custom_components/afvalinfo/ folder to: [homeassistant]/config/custom_components/afvalinfo/

Example config:
```Configuration.yaml:
  sensor:
    - platform: afvalinfo
      id: huis van ouders              (optional, default = '') add some extra naming to make identification of multiple afvalinfo sensors easier
      resources:                       (at least 1 required)
        - pbd
        - trash_type_today
      location: sliedrecht             (required, default = sliedrecht) name of the 'gemeente'
      postcode: 3361AB                 (required, default = 3361AB)
      streetnumber: 1                  (required, default = 1)
      dateformat: '%d-%m-%Y'           (optional, default = %d-%m-%Y) day-month-year
      locale: 'nl'                     (optional, default = 'en')
      timespanindays: 365              (optional, default = 365) number of days to look into the future
```

Above example has 1 normal resource and one special resource. Here is a complete list of available waste fractions:
- gft                                  (groente, fruit, tuinafval)
- papier
- pbd                                  (plastic, blik, drinkpakken)
- restafval
- textiel

Here is a complete list of special resources. To make these resources work, you also need to specify one or more of the normal resources from above.
So if you only specify -pbd and -trash_type_today under your resources, you will only get a result if the trash type 'pbd' has the same date as today. If you also want to know if -gft has the same date as today, you also need to specify - gft under resources, as shown below.
```Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:
        - pbd
        - gft
        - trash_type_today
        - trash_type_tomorrow
      location: sliedrecht
      postcode: 3361AB
      streetnumber: 1
```
These resources will return one or more (seperated with a space) of the following results (gft, papier, pbd, restafval, textiel).
- trash_type_today                      (gives the result "none" if none of the normal resources dates is today)
- trash_type_tomorrow                   (gives the result "none" if none of the normal resources dates is tomorrow)

### Date format
```yaml
dateformat:
```
If you want to adjust the way the date is presented. You can do it using the dateformat option. All [python strftime options](http://strftime.org/) should work.
Default is '%d-%m-%Y', which will result in per example:
```yaml
21-9-2019
```
```yaml
locale:
```
With locale you can present the date in any language you want (this only works for the day of the week (%a or %A) and the name of the month (%b or %B)). [Here](http://www.localeplanet.com/icu/iso639.html) is a list of locales. If you use '%A %d %B %Y' for dateformat and 'nl' for locale, the date will be presented as:
```yaml
zaterdag 21 september 2019
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
- days_until_collection_date.    This will return the number of days between today and the collection date.
- is_collection_date_today.      This will return true if the collection date is today and false if the collection date is not today.
- hidden.                        This will return true on error or if the date is outside of range of the 'timespanindays' value. On any other occasion it will return true.

Example for usage of attributes.
This example creates a new sensor with the attribute value 'days_until_collection_date' of the sensor 'sensor.afvalinfo_papier':
```yaml
- platform: template
    sensors:
      paper_days_until_collection:
        value_template: "{{ state_attr('sensor.afvalinfo_papier', 'days_until_collection_date') }}"
```

And another template example to only show the first upcoming trashtype and pickup date.
```yaml
- platform: template
  sensors:
    next_trash_type_and_date:
      value_template: >
        {%- set gft = state_attr('sensor.afvalinfo_gft', 'days_until_collection_date') | float -%}
        {%- set pbd = state_attr('sensor.afvalinfo_pbd', 'days_until_collection_date') | float -%}
        {%- set papier = state_attr('sensor.afvalinfo_papier', 'days_until_collection_date') | float -%}
        {%- set restafval = state_attr('sensor.afvalinfo_restafval', 'days_until_collection_date') | float -%}
        {%- set textiel = state_attr('sensor.afvalinfo_textiel', 'days_until_collection_date') | float -%}
        {%- set minimum = (gft,pbd,papier,restafval,textiel)|min -%}
        {% if gft == minimum  %}
          gft · {{ states('sensor.afvalinfo_gft') }}
        {% elif pbd == minimum  %}
          pbd · {{ states('sensor.afvalinfo_pbd') }}
        {% elif papier == minimum  %}
          papier · {{ states('sensor.afvalinfo_papier') }}
        {% elif restafval == minimum  %}
          restafval · {{ states('sensor.afvalinfo_restafval') }}
        {% elif textiel == minimum  %}
          textiel - {{ states('sensor.afvalinfo_textiel') }}
        {% else %}
          n/a
        {% endif %}
```
