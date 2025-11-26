## Home Assistant sensor component/integration for waste collectors in the Netherlands
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/hacs/integration)

![icon_mini](https://github.com/heyajohnny/afvalinfo/assets/20553716/b777f12e-8847-40a8-b5e7-4728378c0a92)
## Breaking changes for upgrading from v1.x.x to v2.x.x
If you've just updated from v1.x.x to v2.x.x please remove the afvalinfo sensor from your configuration.yaml and follow [Installation step 2](#installation-step-2)

### Supported in 98% of the Dutch 'gemeenten'

Before you use this integration you can test if your address is supported and working over [here](https://4fv4l.nl).
If you like my work, please buy me a coffee or donate some crypto currencies. This will keep me awake, asleep, or whatever :wink:

<a href="https://www.buymeacoffee.com/1v3ckWD" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png"></a><details>
  <summary>Crypto currency addresses</summary>
<img width="164px" alt="xmr" src="https://user-images.githubusercontent.com/20553716/210132784-63613225-d9da-427d-a20b-e1003045a1f4.png">
<img width="164px" alt="btc" src="https://user-images.githubusercontent.com/20553716/210132426-6c58d8d1-b351-4ae7-9b61-cd5511cdb4ed.png">
<img width="164px" alt="ada" src="https://user-images.githubusercontent.com/20553716/210132510-b1106b55-c9e3-413d-b8e0-26ba4e24a5de.png">
</details>

#### Not supported gemeenten in the Netherlands

```
"haaksbergen", "oegstgeest", "schiermonnikoog", "terneuzen", "texel", "vlieland", "weert"
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

4. Fill in the form with your address details (Zip code + House Number (+ House number suffix))

(When you live in the municipality <strong>maassluis</strong> or <strong>ouder-amstel</strong> only fill in the Municipality + District and leave Zip code + House number + House number suffix empty. You can find the districts for <strong>ouder-amstel</strong> [here](#ouder-amstel) and the districts for <strong>maassluis</strong> [here](#maassluis))

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/84c52c53-564a-4f40-abf4-a3a79d4f7759)

And at the bottom of the page, add the sensors you'd like to see

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/a724a27b-d238-4ac1-9cf0-0e24c9960d90)

These 2 sensors are special sensors

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/7fb50d3f-6100-419a-8ef2-b79c1c2178f2)

To make these sensors work, you also need to specify one or more of the normal sensors.
These sensors will return one or more (seperated with a comma) of the other sensor friendly names, if of course these trash types will be picked up today/tomorrow. So if you only added PBD and Trash type today under your sensors, you will only get a result of 'PBD' if the trash type PBD has the same date as today. If there is no trash to pick up you'll gwt this value

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/ecd5e4a5-6678-44f2-ba60-de7cbcffeb6f)

### (Optional) Installation step 3 (Change friendly name)
If you want to change the friendly name of the sensors (and also the names you see in the sensors 'Trash type today' and 'Trash type tomorrow') follow these steps.
1. Press Settings --> Devices & Services
2. Press 'x ENTITIES' inside the 'Afvalinfo' card

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/19759df4-a0b5-49d1-8b03-8af4afa1f8ec)

3. Select the sensor whose friendly name you want to change

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/5d415e80-f80f-4969-a48b-aab88f64f0f5)

4. Press the settings button in the upper right corner

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/474dadb0-afff-445d-8d51-1a38f4ef496b)

5. Change the value under 'Name' and press 'Update' in the bottom right corner

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/7f8e4234-508b-4dfb-86c4-a7528021fd67)

That's it! The friendly name should be changed

![image](https://github.com/heyajohnny/afvalinfo/assets/20553716/350f1bdc-4375-467b-8548-3103209c002c)

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
template:
  sensor:
    - name: Days until paper collection
      unique_id: paper_days_until_collection
      state: "{{ state_attr('sensor.afvalinfo_home_papier', 'days_until_collection_date') }}"
```

And another template example to only show the first upcoming trashtype and pickup date (Special thanks to <a href="https://github.com/jaydouble" target="_blank">jaydouble</a>)
```yaml
template:
  sensor:
    - name: Afval info volgende inzameling en datum
      unique_id: afvalinfo_home_next_trash_type_and_date
      state: >-
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
If there are any problems with the integration, please first test your address over [here](https://trashapi.azurewebsites.net/index.html) and try out the /Trash request. If this also doesn't work feel free to create an issue [here](https://github.com/heyajohnny/afvalinfo/issues)
