## Home Assistant sensor component/integration for waste collectors in the Netherlands
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
### Number of supported 'gemeenten' in The Netherlands (without Bonaire, Sint Eustatius and Saba): 332 of 339 = 98%

If you like my work, please buy me a coffee or donate some crypto currencies. This will keep me awake :)

<a href="https://www.buymeacoffee.com/1v3ckWD" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a><details>
  <summary>Crypto currency addresses</summary>
<img width="164px" alt="xmr" src="https://user-images.githubusercontent.com/20553716/210132784-63613225-d9da-427d-a20b-e1003045a1f4.png">
<img width="164px" alt="btc" src="https://user-images.githubusercontent.com/20553716/210132426-6c58d8d1-b351-4ae7-9b61-cd5511cdb4ed.png">
<img width="164px" alt="ada" src="https://user-images.githubusercontent.com/20553716/210132510-b1106b55-c9e3-413d-b8e0-26ba4e24a5de.png">
<img width="164px" alt="iota" src="https://user-images.githubusercontent.com/20553716/210132585-9addbc8f-c293-4f63-b2fb-5f4b59af67fd.png">
</details>

Please also take a look at the <a href="https://play.google.com/store/apps/details?id=com.viezegeitafval" target="_blank">Vieze Geit</a> Android app for trash pickup dates on your Android device.
<a href="https://play.google.com/store/apps/details?id=com.viezegeitafval" target="_blank"></a>

#### Provides Home Assistant sensors for the Dutch waste collectors in:

###### "aa en hunze", "aalsmeer", "aalten", "achtkarspelen", "alblasserdam", "albrandswaard", "alkmaar", "almelo", "almere", "alphen aan den rijn", "alphen-chaam", "altena", "ameland", "amersfoort", "amstelveen", "apeldoorn", "arnhem", "assen", "asten", "baarle-nassau", "baarn", "barendrecht", "barneveld", "beek", "beekdaelen", "beesel", "berg en dal", "bergeijk", "bergen op zoom", "bergen", "berkelland", "bernheze", "best", "beuningen", "beverwijk", "bladel", "blaricum", "bloemendaal", "bodegraven-reeuwijk", "boekel", "borger-odoorn", "borne", "borsele", "boxtel", "breda", "bronckhorst", "brummen", "brunssum", "bunnik", "bunschoten", "buren", "capelle aan den ijssel", "castricum", "coevorden", "cranendonck", "culemborg", "dalfsen", "dantumadeel f", "dantumadiel", "de bilt", "de friese meren", "de ronde venen", "de wolden", "delft", "den haag", "den helder", "deurne", "deventer", "diemen", "dijk en waard", "dinkelland", "doesburg", "doetinchem", "dongen", "dordrecht", "drechterland", "drimmelen", "dronten", "druten", "duiven", "echt-susteren", "ede", "eemnes", "eemsdelta", "eersel", "eijsden-margraten", "eindhoven", "elburg", "emmen", "enkhuizen", "enschede", "epe", "ermelo", "etten-leur", "geertruidenberg", "geldrop-mierlo", "gemert-bakel", "gennep", "gilze en rijen", "goeree-overflakkee", "goes", "goirle", "gooise meren", "gorinchem", "gouda", "groningen", "gulpen-wittem", "haarlem", "haarlemmermeer", "halderberge", "hardenberg", "harderwijk", "hardinxveld-giessendam", "harlingen", "hattem", "heemskerk", "heemstede", "heerde", "heerenveen", "heerlen", "heeze-leende", "heiloo", "hellendoorn", "helmond", "hendrik-ido-ambacht", "hengelo", "het hogeland", "heumen", "heusden", "hillegom", "hilvarenbeek", "hilversum", "hoeksche waard", "hof van twente", "hollands kroon", "hoogeveen", "hoorn", "horst aan de maas", "houten", "huizen", "hulst", "ijsselstein", "kaag en braassem", "kampen", "kapelle", "katwijk", "kerkrade", "koggenland", "krimpen aan den ijssel", "krimpenerwaard", "laarbeek", "landgraaf", "landsmeer", "land van cuijk", "lansingerland", "laren", "leeuwarden", "leiden", "leiderdorp", "leidschendam-voorburg", "lelystad", "leudal", "leusden", "lingewaard", "lisse", "lochem", "loon op zand", "lopik", "losser", "maasdriel", "maasgouw", "maashorst", "maassluis", "maastricht", "medemblik", "meerssen", "meierijstad", "meppel", "middelburg", "midden-delfland", "midden-drenthe", "midden-groningen", "moerdijk", "molenlanden", "montferland", "montfoort", "mook en middelaar", "neder-betuwe", "nieuwegein", "nieuwkoop", "nijkerk", "nijmegen", "nissewaard", "noardeast-fryslan", "noord-beveland", "noordenveld", "noordoostpolder", "noordwijk", "nuenen", "nunspeet", "oirschot", "oisterwijk", "oldambt", "oldebroek", "oldenzaal", "olst-wijhe", "ommen", "oost gelre", "oosterhout", "ooststellingwerf", "opmeer", "opsterland", "oss", "oude ijsselstreek", "oude pekela", "oudewater", "overbetuwe", "papendrecht", "peel en maas", "pijnacker-nootdorp", "purmerend", "putten", "raalte", "reimerswaal", "renkum", "renswoude", "reusel-de mierden", "rheden", "rhenen", "ridderkerk", "rijssen-holten", "rijswijk", "roerdalen", "roermond", "roosendaal", "rotterdam rozenburg", "rotterdam", "rucphen", "s-hertogenbosch", "schagen", "scherpenzeel", "schiedam", "schouwen-duiveland", "simpelveld", "sint-michielsgestel", "sittard-geleen", "sliedrecht", "sluis", "smallingerland", "soest", "someren", "son en breugel", "stadskanaal", "staphorst", "stede broec", "steenbergen"(only route2), "steenwijkerland", "stein", "stichtse vecht", "terneuzen", "terschelling", "teylingen", "tholen", "tiel", "tietjerksteradeel", "tilburg", "tubbergen", "twenterand", "tynaarlo", "uitgeest", "uithoorn", "urk", "utrecht", "utrechtse heuvelrug", "vaals", "valkenburg aan de geul", "valkenswaard", "veendam", "veenendaal", "veere", "veldhoven", "velsen", "venlo", "venray", "vijfheerenlanden", "vlaardingen", "vlissingen", "voerendaal", "voorne aan zee", "voorschoten", "voorst", "vught", "waadhoeke", "waalre", "waalwijk", "waddinxveen", "wageningen", "wassenaar", "waterland", "weesp", "west betuwe", "west maas en waal", "westerkwartier", "westerveld", "westervoort", "westerwolde", "westland", "weststellingwerf", "wierden", "wijchen", "wijdemeren", "wijk bij duurstede", "winterswijk", "woensdrecht", "woerden", "wormerland", "woudenberg", "zaanstad", "zaltbommel", "zandvoort", "zeewolde", "zeist", "zevenaar", "zoetermeer", "zoeterwoude", "zuidplas", "zuidwest-friesland", "zundert", "zutphen", "zwartewaterland", "zwijndrecht", "zwolle"

### Add 'gemeente'
The code is designed to add new 'gemeenten' relatively easy.
Please create an issue in https://github.com/heyajohnny/afvalinfo/issues to request a new 'gemeente'.
If there are any problems with the integration, please test your address on http://4fv4l.nl. If it works there, you've done something wrong in your configuration.yaml. Otherwise create an issue here: https://github.com/heyajohnny/afvalinfo/issues

### Install:
- Copy the files in the /custom_components/afvalinfo/ folder to: [homeassistant]/config/custom_components/afvalinfo/

Example config:
(Or use the lazy and easier route and just copy paste the values from this [configuration.yaml](https://github.com/heyajohnny/afvalinfo/blob/master/example/configuration.yaml))
#### Don't forget to remove the comments from the example config (everything between and after the parentheses)
```Configuration.yaml:
  sensor:
    - platform: afvalinfo
      id: vakantiehuis                 (optional, default = '') add some extra naming to make identification of multiple afvalinfo sensors easier
      resources:                       (at least 1 required)
        - type: gft                                   (type is required)
          friendly_name: Groente Fruit en Tuinafval   (friendly_name is optional)
        - type: kerstboom
          friendly_name: Kerstboom
        - type: pbd
          friendly_name: Plastic Blik en Drankkartons
        - type: papier
          friendly_name: Papier
        - type: restafval
          friendly_name: Restafval
      - type: takken                  (also matches 'GFT in emmers' for some 'gemeenten')
          friendly_name: Takken
        - type: textiel
          friendly_name: Oude Kleding
        - type: trash_type_today
          friendly_name: Afval voor vandaag
        - type: trash_type_tomorrow
          friendly_name: Afval voor morgen
      location: sliedrecht             (required, default = sliedrecht) name of the 'gemeente'
      postcode: 3361AB                 (required, default = 3361AB)
      streetnumber: 1                  (required, default = 1)
      streetnumbersuffix: ''           (optional, default = '')
      district: ''                     (optional, default = '') only needed for location maassluis
      diftarcode: 12345678             (optional, default = '') some 'gemeentes' have diftar codes
      dateformat: '%d-%m-%Y'           (optional, default = %d-%m-%Y) day-month-year
      locale: 'nl'                     (optional, default = 'en')
      timespanindays: 365              (optional, default = 365) number of days to look into the future
      notrashtext: 'geen'              (Optional, default = 'none') the text to show for the today and tomorrow sensor when there is no trash to collect
      getwholeyear: false              (Optional, default = false) (if supported by gemeente) sets the trash dates for the whole year in the 'whole_year_dates' attribute when true
```

Here are the supported districts for the 'gemeente' maassluis (These are not case sensitive):
"binnenstad/centrum", "Componistenwijk", "Dalenbuurt", "Dichtersbuurt", "Drevenbuurt", "Koningshoek", "Maasdijk", "Molenwijk", "Oranjewijk", "Sluispolder Oost",
"Vertowijk", "Vogelwijk", "Weverskade", "Wijk 't Hoofd", "Wilgenrijk", "Zeeheldenbuurt", "Zuidbuurt"

Here is the complete list of available waste types:
- gft                                  (groente, fruit, tuinafval)
- kerstboom                            (supported in +- 50% of the waste collectors)
- papier
- pbd                                  (plastic, blik, drinkpakken)
- restafval
- takken                               (supported by a small amount of waste collectors) (also matches 'GFT in emmers' for some 'gemeenten')
- textiel

Here is a complete list of special resources. To make these resources work, you also need to specify one or more of the normal resources (waste types) from above.
These resources will return one or more (seperated with a comma) of the following results (gft, kerstboom, papier, pbd, restafval, takken, textiel) or if you specified a friendly_name, it will return one or more of the friendly_name values
- trash_type_today                      (gives the result "none" if none of the normal resources dates is today)
- trash_type_tomorrow                   (gives the result "none" if none of the normal resources dates is tomorrow)

So if you only specify -pbd and -trash_type_today under your resources, you will only get a result if the trash type 'pbd' has the same date as today. If you also want to know if -gft has the same date as today, you also need to specify - gft under resources, as shown below.
```Configuration.yaml:
  sensor:
    - platform: afvalinfo
      resources:
        - type: pbd
          friendly_name: Plastic Blik en Drankkartons
        - type: gft
          friendly_name: Groente Fruit en Tuinafval
        - type: trash_type_today
          friendly_name: Afval voor vandaag
      location: sliedrecht
      postcode: 3361AB
      streetnumber: 1
```

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
- whole_year_dates.              This will return all the dates from today to the end of the year when 'getwholeyear' is set to true

If your location supports diftar and you've specified a diftarcode, these attributes are also available:
- last_collection_date.          This wil return the last diftar collection date.
- total_collections_this_year    This will return the total number of diftar collections for the current year

Example for usage of attributes.
This example creates a new sensor with the attribute value 'days_until_collection_date' of the sensor 'sensor.afvalinfo_papier':
```yaml
- platform: template
    sensors:
      paper_days_until_collection:
        value_template: "{{ state_attr('sensor.afvalinfo_papier', 'days_until_collection_date') }}"
```

And another template example to only show the first upcoming trashtype and pickup date (Special thanks to <a href="https://github.com/jaydouble" target="_blank">jaydouble</a>)
```yaml
- platform: template
  sensors:
    afvalinfo_next_trash_type_and_date:
      value_template: >
        {% set ns = namespace(minimum=365) %}
        {% set list = ['groente_fruit_en_tuinafval', 'kerstboom', 'plastic_blik_en_drankkartons', 'papier', 'restafval', 'takken', 'oude_kleding'] %}
        {% set friendly_list = ['Groente Fruit en Tuinafval', 'Kerstboom', 'Plastic Blik en Drankkartons', 'Papier', 'Restafval', 'Takken', 'Oude Kleding'] %}
        {%- for l in list %}
        {%- set days = state_attr('sensor.afvalinfo_' ~l, 'days_until_collection_date')%}
        {%- if days != None and days < ns.minimum %}
        {%- set ns.minimum = days %}
        {%- endif %}
        {%- endfor %}
        {%- for l in list %}
        {%- set days = state_attr('sensor.afvalinfo_' ~l, 'days_until_collection_date')%}
        {%- if days == ns.minimum %}
        {{friendly_list[loop.index0]}} · {{ states('sensor.afvalinfo_' ~l) }}
        {%- endif %}
        {%- endfor %}
```

### Lovelace UI
Please take a look @ <a href="https://github.com/bafplus/HA-afvalinfo-card" target="_blank">bafplus</a>. He made some awesome Lovelace cards for Afvalinfo.
