# HotelScraping

![python logo](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)  

## Description

Scraping project made in python using selenium.  
Project main goal is to scrap datas from different website for study.
The python scripts create bots that navigates through the different hotels website (hotels.com, booking, trivago and kayak). It will use the research system and it will scrap all hotels' data on every available pages (the data gathered are stored into differente csv files, one csv file for each website).  
Those data can be used by the GUI app website to search for the hotel that best suit you or for analysis.
There is specific section on the gui app that allow you to study the price of the hotel and locate them on a map.

## Website scraped

- <hotels.com>
- <booking.com>
- <trivago.com>
- <kayak.fr>

## Hotels' data gathered

- Name
- Adress
- Price
- Number of stars
- Coordinates
- Number of persons (adults, children)
- Number of chambers

## GUI application

We implemented a GUI application made in dash and hosted on pythonanywhere.  
The website is in French. No english translation has been made.

### GUI description

On the website you can search an hotel by differents caracteristics. You can also summarize check the mean and variance price per month of all the hotels.  
Giving you informations about the most expensive month for sleeping at the hotels.

### GUI Images

| Main page | Research page |
| --- | --- |
| ![Image1](Readme_files/image1.png) | ![Image2](Readme_files/image2.png) |

| Statistics page | Map page |
| --- | --- |
| ![Image3](Readme_files/image3.png) | ![Image4](Readme_files/image4.png) |

## Other sources

The source code of the website can be found here :  
<https://github.com/maaelle/InterfaceHotel>

Flutter GUI prototype projetc :  
<https://github.com/clementreiffers/hotel-scraper-interface>

## Contributors

Maëlle MARCELIN :  

- @maaelle
- <https://github.com/maaelle>

Clément REIFFERS :

- @clementreiffers
- <https://github.com/clementreiffers>

Quentin MOREL :

- @Im-Rises
- <https://github.com/Im-Rises>

Adrien Tirlemont :

- @Meatisdelicious
- <https://github.com/Meatisdelicious>

## APIs

Selenium :  
<https://www.selenium.dev>

Pythonanywhere :  
<http://maaelle.pythonanywhere.com>

Dash :  
<https://plotly.com/dash/>