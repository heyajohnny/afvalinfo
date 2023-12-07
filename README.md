## Home Assistant sensor component/integration for waste collectors in the Netherlands

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)
### Supported in 98% of the Dutch 'gemeenten'

## Breaking changes for upgrading from v1.x.x to v2.x.x
If you've just updated from v1.x.x to v2.x.x please remove the afvalinfo sensor from your configuration.yaml and follow [Installation step 2](#installation-step-2)

Before you use this integration you can test if your address is supported and working over [here](https://4fv4l.nl).
If you like my work, please buy me a coffee or donate some crypto currencies. This will keep me awake, asleep, or whatever :wink:

<a href="https://www.buymeacoffee.com/1v3ckWD" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a><details>
  <summary>Crypto currency addresses</summary>
<img width="164px" alt="xmr" src="https://user-images.githubusercontent.com/20553716/210132784-63613225-d9da-427d-a20b-e1003045a1f4.png">
<img width="164px" alt="btc" src="https://user-images.githubusercontent.com/20553716/210132426-6c58d8d1-b351-4ae7-9b61-cd5511cdb4ed.png">
<img width="164px" alt="ada" src="https://user-images.githubusercontent.com/20553716/210132510-b1106b55-c9e3-413d-b8e0-26ba4e24a5de.png">
<img width="164px" alt="iota" src="https://user-images.githubusercontent.com/20553716/210132585-9addbc8f-c293-4f63-b2fb-5f4b59af67fd.png">
</details>

Please also take a look at the <a href="https://play.google.com/store/apps/details?id=com.viezegeitafval" target="_blank">Vieze Geit</a> Android app for trash pickup dates on your Android device.
<a href="https://play.google.com/store/apps/details?id=com.viezegeitafval" target="_blank"></a>

#### Supported gemeenten in the Netherlands

```
"aa en hunze", "aalsmeer", "aalten", "achtkarspelen", "alblasserdam", "albrandswaard", "alkmaar", "almelo", "almere", "alphen aan den rijn", "alphen-chaam", "altena", "ameland", "amersfoort", "amstelveen", "apeldoorn", "arnhem", "assen", "asten", "baarle-nassau", "baarn", "barendrecht", "barneveld", "beek", "beekdaelen", "beesel", "berg en dal", "bergeijk", "bergen op zoom", "bergen", "berkelland", "bernheze", "best", "beuningen", "beverwijk", "bladel", "blaricum", "bloemendaal", "bodegraven-reeuwijk", "boekel", "borger-odoorn", "borne", "borsele", "boxtel", "breda", "bronckhorst", "brummen", "brunssum", "bunnik", "bunschoten", "buren", "capelle aan den ijssel", "castricum", "coevorden", "cranendonck", "culemborg", "dalfsen", "dantumadiel", "de bilt", "de friese meren", "de fryske marren", "de ronde venen", "de wolden", "delft", "den haag", "den helder", "deurne", "deventer", "diemen", "dijk en waard", "dinkelland", "doesburg", "doetinchem", "dongen", "dordrecht", "drechterland", "drimmelen", "dronten", "druten", "duiven", "echt-susteren", "ede", "eemnes", "eemsdelta", "eersel", "eijsden-margraten", "eindhoven", "elburg", "emmen", "enkhuizen", "enschede", "epe", "ermelo", "etten-leur", "geertruidenberg", "geldrop-mierlo", "gemert-bakel", "gennep", "gilze en rijen", "goeree-overflakkee", "goes", "goirle", "gooise meren", "gorinchem", "gouda", "groningen", "gulpen-wittem", "haarlem", "haarlemmermeer", "halderberge", "hardenberg", "harderwijk", "hardinxveld-giessendam", "harlingen", "hattem", "heemskerk", "heemstede", "heerde", "heerenveen", "heerlen", "heeze-leende", "heiloo", "hellendoorn", "helmond", "hendrik-ido-ambacht", "hengelo", "het hogeland", "heumen", "heusden", "hillegom", "hilvarenbeek", "hilversum", "hoeksche waard", "hof van twente", "hollands kroon", "hoogeveen", "hoorn", "horst aan de maas", "houten", "huizen", "hulst", "ijsselstein", "kaag en braassem", "kampen", "kapelle", "katwijk", "kerkrade", "koggenland", "krimpen aan den ijssel", "krimpenerwaard", "laarbeek", "landgraaf", "landsmeer", "land van cuijk", "lansingerland", "laren", "leeuwarden", "leiden", "leiderdorp", "leidschendam-voorburg", "lelystad", "leudal", "leusden", "lingewaard", "lisse", "lochem", "loon op zand", "lopik", "losser", "maasdriel", "maasgouw", "maashorst", "maassluis", "maastricht", "medemblik", "meerssen", "meierijstad", "meppel", "middelburg", "midden-delfland", "midden-drenthe", "midden-groningen", "moerdijk", "molenlanden", "montferland", "montfoort", "mook en middelaar", "neder-betuwe", "nederweert", "nieuwegein", "nieuwkoop", "nijkerk", "nijmegen", "nissewaard", "noardeast-fryslan", "noord-beveland", "noordenveld", "noordoostpolder", "noordwijk", "nuenen", "nunspeet", "oirschot", "oisterwijk", "oldambt", "oldebroek", "oldenzaal", "olst-wijhe", "ommen", "oost gelre", "oosterhout", "ooststellingwerf", "opmeer", "opsterland", "oss", "oude ijsselstreek", "ouder-amstel", "oudewater", "overbetuwe", "papendrecht", "peel en maas", "pekela", "pijnacker-nootdorp", "purmerend", "putten", "raalte", "reimerswaal", "renkum", "renswoude", "reusel-de mierden", "rheden", "rhenen", "ridderkerk", "rijssen-holten", "rijswijk", "roerdalen", "roermond", "roosendaal", "rotterdam rozenburg", "rotterdam", "rucphen", "s-hertogenbosch", "schagen", "scherpenzeel", "schiedam", "schouwen-duiveland", "simpelveld", "sint-michielsgestel", "sittard-geleen", "sliedrecht", "sluis", "smallingerland", "soest", "someren", "son en breugel", "stadskanaal", "staphorst", "stede broec", "steenbergen", "steenwijkerland", "stein", "stichtse vecht", "sudwest-fryslan", "terneuzen", "terschelling", "teylingen", "tholen", "tiel", "tietjerksteradeel", "tilburg", "tubbergen", "twenterand", "tynaarlo", "tytsjerksteradiel", "uitgeest", "uithoorn", "urk", "utrecht", "utrechtse heuvelrug", "vaals", "valkenburg aan de geul", "valkenswaard", "veendam", "veenendaal", "veere", "veldhoven", "velsen", "venlo", "venray", "vijfheerenlanden", "vlaardingen", "vlissingen", "voerendaal", "voorne aan zee", "voorschoten", "voorst", "vught", "waadhoeke", "waalre", "waalwijk", "waddinxveen", "wageningen", "wassenaar", "waterland", "weesp", "west betuwe", "west maas en waal", "westerkwartier", "westerveld", "westervoort", "westerwolde", "westland", "weststellingwerf", "wierden", "wijchen", "wijdemeren", "wijk bij duurstede", "winterswijk", "woensdrecht", "woerden", "wormerland", "woudenberg", "zaanstad", "zaltbommel", "zandvoort", "zeewolde", "zeist", "zevenaar", "zoetermeer", "zoeterwoude", "zuidplas", "zundert", "zutphen", "zwartewaterland", "zwijndrecht", "zwolle"
```

### Important Info
This integration supports Diftar data and Cleanprofs cleaning dates

### Installation step 1
There are 2 ways to install afvalinfo:
1. Download 'afvalinfo' from the HACS store (this is the easiest and preferred way)
2. Copy the files in the /custom_components/afvalinfo/ folder to: [homeassistant]/config/custom_components/afvalinfo/

### Installation step 2
The next step is to add afvalinfo sensors to your Home Assistant:
1. Browse to your Home Assistant config page
2. Press Settings --> Devices & Services

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/b5c9eb17-dd4d-418c-b47e-420de6baf416)

3. Press 'Add Integration' and search for 'afvalinfo' and select the 'afvalinfo' integration

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/02f56b0f-1c01-4d42-b94e-529469545a0d)

4. Fill in the form with your address details.
(Only fill in the Municipality and District and leave Zip code and House number empty when you live in the municipality ['maassluis'](#maassluis) or ['ouder-amstel'](#ouder-amstel))

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/84c52c53-564a-4f40-abf4-a3a79d4f7759)

And at the bottom of the page, add the sensors you'd like to see

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/a724a27b-d238-4ac1-9cf0-0e24c9960d90)

These 2 sensors are special sensors

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/7fb50d3f-6100-419a-8ef2-b79c1c2178f2)

To make these sensors work, you also need to specify one or more of the normal sensors.
These sensors will return one or more (seperated with a comma) of the other sensor names, if of course these trash types will be picked up today/tomorrow. So if you only added PBD and Trash type today under your sensors, you will only get a result of 'PBD' if the trash type PBD has the same date as today. If there is no trash to pick up you'll gwt this value

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/ecd5e4a5-6678-44f2-ba60-de7cbcffeb6f)

### maassluis
For the gemeente maassluis you need to use the 'district'. Here you can see the supported districts (Not case sensitive):
```
"Binnenstad/centrum"
"Componistenwijk"
"Dalenbuurt"
"Dichtersbuurt"
"Drevenbuurt"
"Koningshoek"
"Maasdijk"
"Molenwijk"
"Oranjewijk"
"Sluispolder Oost"
"Vertowijk"
"Vogelwijk"
"Weverskade"
"Wijk 't Hoofd"
"Wilgenrijk"
"Zeeheldenbuurt"
"Zuidbuurt"
```
### ouder-amstel
For the gemeente ouder-amstel you need to use the 'district'. Here you can see the supported districts (Not case sensitive):
```
"Bebouwde kom"
"Buitengebied"
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

### Attributes
There are 3 important attributes:
```
- days_until_collection_date.    This will return the number of days between today and the collection date.
- is_collection_date_today.      This will return true if the collection date is today and false if the collection date is not today.
- whole_year_dates.              This will return all the dates from today to the end of the year when 'getwholeyear' is set to true
```

If your location supports diftar and you've specified a diftarcode, these attributes are also available:
```
- last_collection_date.          This wil return the last diftar collection date.
- total_collections_this_year    This will return the total number of diftar collections for the current year
```

Example for usage of attributes.
This example creates a new sensor with the attribute value 'days_until_collection_date' of the sensor 'sensor.afvalinfo_papier':
```yaml
- platform: template
    sensors:
      paper_days_until_collection:
        value_template: "{{ state_attr('sensor.afvalinfo_home_papier', 'days_until_collection_date') }}"
```

And another template example to only show the first upcoming trashtype and pickup date (Special thanks to <a href="https://github.com/jaydouble" target="_blank">jaydouble</a>)
```yaml
- platform: template
  sensors:
    afvalinfo_home_next_trash_type_and_date:
      value_template: >
        {% set ns = namespace(minimum=365) %}
        {% set list = ['groente_fruit_en_tuinafval', 'kerstboom', 'plastic_blik_en_drankkartons', 'papier', 'restafval', 'takken', 'textiel'] %}
        {% set friendly_list = ['Groente Fruit en Tuinafval', 'Kerstboom', 'Plastic Blik en Drankkartons', 'Papier', 'Restafval', 'Takken', 'Oude Kleding'] %}
        {%- for l in list %}
        {%- set days = state_attr('sensor.afvalinfo_home_' ~l, 'days_until_collection_date')%}
        {%- if days != None and days < ns.minimum %}
        {%- set ns.minimum = days %}
        {%- endif %}
        {%- endfor %}
        {%- for l in list %}
        {%- set days = state_attr('sensor.afvalinfo_home_' ~l, 'days_until_collection_date')%}
        {%- if days == ns.minimum %}
        {{friendly_list[loop.index0]}} · {{ states('sensor.afvalinfo_home_' ~l) }}
        {%- endif %}
        {%- endfor %}
```

### Lovelace UI
Please take a look @ <a href="https://github.com/bafplus/HA-afvalinfo-card" target="_blank">bafplus</a>. He made some awesome Lovelace cards for Afvalinfo.

### Issues
If there are any problems with the integration, please first test your address over [here](https://4fv4l.nl). If it works there, you've done something wrong in your configuration.yaml. You can try generating a new config over [here](https://4fv4l.nl/ha). Otherwise create an issue [here](https://github.com/heyajohnny/afvalinfo/issues)
