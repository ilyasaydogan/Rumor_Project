#########  Importing Library  #########

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import random
import pandas as pd
from datetime import datetime
import re
import locale
locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')

#########  Getting Links and Stocks #########

trade_links_dict = {} # Creating dictionary to store the trade and links information

# Assuming 'table_lines' contains the lines of your table
# You can read the table from a file or any other source
table_lines1 = [
"AEFES\thttps://tr.investing.com/equities/anadolu-efes-commentary\thttps://tr.investing.com/equities/anadolu-efes-commentary/2\thttps://tr.investing.com/equities/anadolu-efes-commentary/3\thttps://tr.investing.com/equities/anadolu-efes-commentary/4\thttps://tr.investing.com/equities/anadolu-efes-commentary/5","AGHOL\thttps://tr.investing.com/equities/yazicilar-holding-commentary\thttps://tr.investing.com/equities/yazicilar-holding-commentary/2\thttps://tr.investing.com/equities/yazicilar-holding-commentary/3\thttps://tr.investing.com/equities/yazicilar-holding-commentary/4\thttps://tr.investing.com/equities/yazicilar-holding-commentary/5","AHGAZ\thttps://tr.investing.com/equities/ahlatci-dogal-gaz-dagitim-enerji-commentary\thttps://tr.investing.com/equities/ahlatci-dogal-gaz-dagitim-enerji-commentary/2\thttps://tr.investing.com/equities/ahlatci-dogal-gaz-dagitim-enerji-commentary/3\thttps://tr.investing.com/equities/ahlatci-dogal-gaz-dagitim-enerji-commentary/4\thttps://tr.investing.com/equities/ahlatci-dogal-gaz-dagitim-enerji-commentary/5","AKBNK\thttps://tr.investing.com/equities/akbank-commentary\thttps://tr.investing.com/equities/akbank-commentary/2\thttps://tr.investing.com/equities/akbank-commentary/3\thttps://tr.investing.com/equities/akbank-commentary/4\thttps://tr.investing.com/equities/akbank-commentary/5","AKCNS\thttps://tr.investing.com/equities/akcansa-commentary\thttps://tr.investing.com/equities/akcansa-commentary/2\thttps://tr.investing.com/equities/akcansa-commentary/3\thttps://tr.investing.com/equities/akcansa-commentary/4\thttps://tr.investing.com/equities/akcansa-commentary/5","AKFYE\thttps://tr.investing.com/equities/akfen-yenilenebilir-enerji-as-commentary\thttps://tr.investing.com/equities/akfen-yenilenebilir-enerji-as-commentary/2\thttps://tr.investing.com/equities/akfen-yenilenebilir-enerji-as-commentary/3\thttps://tr.investing.com/equities/akfen-yenilenebilir-enerji-as-commentary/4\thttps://tr.investing.com/equities/akfen-yenilenebilir-enerji-as-commentary/5","AKSA\thttps://tr.investing.com/equities/aksa-commentary\thttps://tr.investing.com/equities/aksa-commentary/2\thttps://tr.investing.com/equities/aksa-commentary/3\thttps://tr.investing.com/equities/aksa-commentary/4\thttps://tr.investing.com/equities/aksa-commentary/5","AKSEN\thttps://tr.investing.com/equities/aksa-enerji-uretim-commentary\thttps://tr.investing.com/equities/aksa-enerji-uretim-commentary/2\thttps://tr.investing.com/equities/aksa-enerji-uretim-commentary/3\thttps://tr.investing.com/equities/aksa-enerji-uretim-commentary/4\thttps://tr.investing.com/equities/aksa-enerji-uretim-commentary/5","ALARK\thttps://tr.investing.com/equities/alarko-holding-commentary\thttps://tr.investing.com/equities/alarko-holding-commentary/2\thttps://tr.investing.com/equities/alarko-holding-commentary/3\thttps://tr.investing.com/equities/alarko-holding-commentary/4\thttps://tr.investing.com/equities/alarko-holding-commentary/5","ALBRK\thttps://tr.investing.com/equities/albaraka-turk-commentary\thttps://tr.investing.com/equities/albaraka-turk-commentary/2\thttps://tr.investing.com/equities/albaraka-turk-commentary/3\thttps://tr.investing.com/equities/albaraka-turk-commentary/4\thttps://tr.investing.com/equities/albaraka-turk-commentary/5","ALFAS\thttps://tr.investing.com/equities/alfa-solar-enerji-as-commentary\thttps://tr.investing.com/equities/alfa-solar-enerji-as-commentary/2\thttps://tr.investing.com/equities/alfa-solar-enerji-as-commentary/3\thttps://tr.investing.com/equities/alfa-solar-enerji-as-commentary/4\thttps://tr.investing.com/equities/alfa-solar-enerji-as-commentary/5","ARCLK\thttps://tr.investing.com/equities/arcelik-commentary\thttps://tr.investing.com/equities/arcelik-commentary/2\thttps://tr.investing.com/equities/arcelik-commentary/3\thttps://tr.investing.com/equities/arcelik-commentary/4\thttps://tr.investing.com/equities/arcelik-commentary/5","ASELS\thttps://tr.investing.com/equities/aselsan-commentary\thttps://tr.investing.com/equities/aselsan-commentary/2\thttps://tr.investing.com/equities/aselsan-commentary/3\thttps://tr.investing.com/equities/aselsan-commentary/4\thttps://tr.investing.com/equities/aselsan-commentary/5","ASGYO\thttps://tr.investing.com/equities/asce-gayrimenkul-yatirim-ortakligi-commentary\thttps://tr.investing.com/equities/asce-gayrimenkul-yatirim-ortakligi-commentary/2\thttps://tr.investing.com/equities/asce-gayrimenkul-yatirim-ortakligi-commentary/3\thttps://tr.investing.com/equities/asce-gayrimenkul-yatirim-ortakligi-commentary/4\thttps://tr.investing.com/equities/asce-gayrimenkul-yatirim-ortakligi-commentary/5","ASTOR\thttps://tr.investing.com/equities/astor-enerji-as-commentary\thttps://tr.investing.com/equities/astor-enerji-as-commentary/2\thttps://tr.investing.com/equities/astor-enerji-as-commentary/3\thttps://tr.investing.com/equities/astor-enerji-as-commentary/4\thttps://tr.investing.com/equities/astor-enerji-as-commentary/5","BERA\thttps://tr.investing.com/equities/kombassan-holding-as-commentary\thttps://tr.investing.com/equities/kombassan-holding-as-commentary/2\thttps://tr.investing.com/equities/kombassan-holding-as-commentary/3\thttps://tr.investing.com/equities/kombassan-holding-as-commentary/4\thttps://tr.investing.com/equities/kombassan-holding-as-commentary/5","BIENY\thttps://tr.investing.com/equities/bien-yapi-urunleri-sanayi-turizm-commentary\thttps://tr.investing.com/equities/bien-yapi-urunleri-sanayi-turizm-commentary/2\thttps://tr.investing.com/equities/bien-yapi-urunleri-sanayi-turizm-commentary/3\thttps://tr.investing.com/equities/bien-yapi-urunleri-sanayi-turizm-commentary/4\thttps://tr.investing.com/equities/bien-yapi-urunleri-sanayi-turizm-commentary/5","BIMAS\thttps://tr.investing.com/equities/bim-magazalar-commentary\thttps://tr.investing.com/equities/bim-magazalar-commentary/2\thttps://tr.investing.com/equities/bim-magazalar-commentary/3\thttps://tr.investing.com/equities/bim-magazalar-commentary/4\thttps://tr.investing.com/equities/bim-magazalar-commentary/5","BIOEN\thttps://tr.investing.com/equities/biotrend-cevre-ve-enerji-yat-commentary\thttps://tr.investing.com/equities/biotrend-cevre-ve-enerji-yat-commentary/2\thttps://tr.investing.com/equities/biotrend-cevre-ve-enerji-yat-commentary/3\thttps://tr.investing.com/equities/biotrend-cevre-ve-enerji-yat-commentary/4\thttps://tr.investing.com/equities/biotrend-cevre-ve-enerji-yat-commentary/5","BOBET\thttps://tr.investing.com/equities/bogazici-beton-sanayi-ve-ticaret-as-commentary\thttps://tr.investing.com/equities/bogazici-beton-sanayi-ve-ticaret-as-commentary/2\thttps://tr.investing.com/equities/bogazici-beton-sanayi-ve-ticaret-as-commentary/3\thttps://tr.investing.com/equities/bogazici-beton-sanayi-ve-ticaret-as-commentary/4\thttps://tr.investing.com/equities/bogazici-beton-sanayi-ve-ticaret-as-commentary/5","BRSAN\thttps://tr.investing.com/equities/borusan-mannesmann-commentary\thttps://tr.investing.com/equities/borusan-mannesmann-commentary/2\thttps://tr.investing.com/equities/borusan-mannesmann-commentary/3\thttps://tr.investing.com/equities/borusan-mannesmann-commentary/4\thttps://tr.investing.com/equities/borusan-mannesmann-commentary/5","BRYAT\thttps://tr.investing.com/equities/borusan-yat.-paz.-commentary\thttps://tr.investing.com/equities/borusan-yat.-paz.-commentary/2\thttps://tr.investing.com/equities/borusan-yat.-paz.-commentary/3\thttps://tr.investing.com/equities/borusan-yat.-paz.-commentary/4\thttps://tr.investing.com/equities/borusan-yat.-paz.-commentary/5","BUCIM\thttps://tr.investing.com/equities/bursa-cimento-commentary\thttps://tr.investing.com/equities/bursa-cimento-commentary/2\thttps://tr.investing.com/equities/bursa-cimento-commentary/3\thttps://tr.investing.com/equities/bursa-cimento-commentary/4\thttps://tr.investing.com/equities/bursa-cimento-commentary/5","CANTE\thttps://tr.investing.com/equities/can2-termik-as-commentary\thttps://tr.investing.com/equities/can2-termik-as-commentary/2\thttps://tr.investing.com/equities/can2-termik-as-commentary/3\thttps://tr.investing.com/equities/can2-termik-as-commentary/4\thttps://tr.investing.com/equities/can2-termik-as-commentary/5","CCOLA\thttps://tr.investing.com/equities/coca-cola-icecek-commentary\thttps://tr.investing.com/equities/coca-cola-icecek-commentary/2\thttps://tr.investing.com/equities/coca-cola-icecek-commentary/3\thttps://tr.investing.com/equities/coca-cola-icecek-commentary/4\thttps://tr.investing.com/equities/coca-cola-icecek-commentary/5","CIMSA\thttps://tr.investing.com/equities/cimsa-commentary\thttps://tr.investing.com/equities/cimsa-commentary/2\thttps://tr.investing.com/equities/cimsa-commentary/3\thttps://tr.investing.com/equities/cimsa-commentary/4\thttps://tr.investing.com/equities/cimsa-commentary/5","CWENE\thttps://tr.investing.com/equities/cw-enerji-muhendislik-ticaret-ve-commentary\thttps://tr.investing.com/equities/cw-enerji-muhendislik-ticaret-ve-commentary/2\thttps://tr.investing.com/equities/cw-enerji-muhendislik-ticaret-ve-commentary/3\thttps://tr.investing.com/equities/cw-enerji-muhendislik-ticaret-ve-commentary/4\thttps://tr.investing.com/equities/cw-enerji-muhendislik-ticaret-ve-commentary/5","DOAS\thttps://tr.investing.com/equities/dogus-otomotiv-commentary\thttps://tr.investing.com/equities/dogus-otomotiv-commentary/2\thttps://tr.investing.com/equities/dogus-otomotiv-commentary/3\thttps://tr.investing.com/equities/dogus-otomotiv-commentary/4\thttps://tr.investing.com/equities/dogus-otomotiv-commentary/5","DOHOL\thttps://tr.investing.com/equities/dogan-holding-commentary\thttps://tr.investing.com/equities/dogan-holding-commentary/2\thttps://tr.investing.com/equities/dogan-holding-commentary/3\thttps://tr.investing.com/equities/dogan-holding-commentary/4\thttps://tr.investing.com/equities/dogan-holding-commentary/5","ECILC\thttps://tr.investing.com/equities/eczacibasi-ilac-commentary\thttps://tr.investing.com/equities/eczacibasi-ilac-commentary/2\thttps://tr.investing.com/equities/eczacibasi-ilac-commentary/3\thttps://tr.investing.com/equities/eczacibasi-ilac-commentary/4\thttps://tr.investing.com/equities/eczacibasi-ilac-commentary/5","ECZYT\thttps://tr.investing.com/equities/eczacibasi-yatirim-commentary\thttps://tr.investing.com/equities/eczacibasi-yatirim-commentary/2\thttps://tr.investing.com/equities/eczacibasi-yatirim-commentary/3\thttps://tr.investing.com/equities/eczacibasi-yatirim-commentary/4\thttps://tr.investing.com/equities/eczacibasi-yatirim-commentary/5","EGEEN\thttps://tr.investing.com/equities/ege-endustri-commentary\thttps://tr.investing.com/equities/ege-endustri-commentary/2\thttps://tr.investing.com/equities/ege-endustri-commentary/3\thttps://tr.investing.com/equities/ege-endustri-commentary/4\thttps://tr.investing.com/equities/ege-endustri-commentary/5","EKGYO\thttps://tr.investing.com/equities/emlak-konut-gmyo-commentary\thttps://tr.investing.com/equities/emlak-konut-gmyo-commentary/2\thttps://tr.investing.com/equities/emlak-konut-gmyo-commentary/3\thttps://tr.investing.com/equities/emlak-konut-gmyo-commentary/4\thttps://tr.investing.com/equities/emlak-konut-gmyo-commentary/5","ENERY\thttps://tr.investing.com/equities/enerya-enerji-as-commentary\thttps://tr.investing.com/equities/enerya-enerji-as-commentary/2\thttps://tr.investing.com/equities/enerya-enerji-as-commentary/3\thttps://tr.investing.com/equities/enerya-enerji-as-commentary/4\thttps://tr.investing.com/equities/enerya-enerji-as-commentary/5","ENJSA\thttps://tr.investing.com/equities/enerjisa-enerji-commentary\thttps://tr.investing.com/equities/enerjisa-enerji-commentary/2\thttps://tr.investing.com/equities/enerjisa-enerji-commentary/3\thttps://tr.investing.com/equities/enerjisa-enerji-commentary/4\thttps://tr.investing.com/equities/enerjisa-enerji-commentary/5","ENKAI\thttps://tr.investing.com/equities/enka-insaat-commentary\thttps://tr.investing.com/equities/enka-insaat-commentary/2\thttps://tr.investing.com/equities/enka-insaat-commentary/3\thttps://tr.investing.com/equities/enka-insaat-commentary/4\thttps://tr.investing.com/equities/enka-insaat-commentary/5","EREGL\thttps://tr.investing.com/equities/eregli-demir-celik-commentary\thttps://tr.investing.com/equities/eregli-demir-celik-commentary/2\thttps://tr.investing.com/equities/eregli-demir-celik-commentary/3\thttps://tr.investing.com/equities/eregli-demir-celik-commentary/4\thttps://tr.investing.com/equities/eregli-demir-celik-commentary/5","EUPWR\thttps://tr.investing.com/equities/europower-enerji-ve-otomasyon-commentary\thttps://tr.investing.com/equities/europower-enerji-ve-otomasyon-commentary/2\thttps://tr.investing.com/equities/europower-enerji-ve-otomasyon-commentary/3\thttps://tr.investing.com/equities/europower-enerji-ve-otomasyon-commentary/4\thttps://tr.investing.com/equities/europower-enerji-ve-otomasyon-commentary/5","EUREN\thttps://tr.investing.com/equities/europen-endustri-insaat-sanayi-ve-commentary\thttps://tr.investing.com/equities/europen-endustri-insaat-sanayi-ve-commentary/2\thttps://tr.investing.com/equities/europen-endustri-insaat-sanayi-ve-commentary/3\thttps://tr.investing.com/equities/europen-endustri-insaat-sanayi-ve-commentary/4\thttps://tr.investing.com/equities/europen-endustri-insaat-sanayi-ve-commentary/5","FROTO\thttps://tr.investing.com/equities/ford-otosan-commentary\thttps://tr.investing.com/equities/ford-otosan-commentary/2\thttps://tr.investing.com/equities/ford-otosan-commentary/3\thttps://tr.investing.com/equities/ford-otosan-commentary/4\thttps://tr.investing.com/equities/ford-otosan-commentary/5","GARAN\thttps://tr.investing.com/equities/garanti-bankasi-commentary\thttps://tr.investing.com/equities/garanti-bankasi-commentary/2\thttps://tr.investing.com/equities/garanti-bankasi-commentary/3\thttps://tr.investing.com/equities/garanti-bankasi-commentary/4\thttps://tr.investing.com/equities/garanti-bankasi-commentary/5","GESAN\thttps://tr.investing.com/equities/girisim-elektrik-taahhut-commentary\thttps://tr.investing.com/equities/girisim-elektrik-taahhut-commentary/2\thttps://tr.investing.com/equities/girisim-elektrik-taahhut-commentary/3\thttps://tr.investing.com/equities/girisim-elektrik-taahhut-commentary/4\thttps://tr.investing.com/equities/girisim-elektrik-taahhut-commentary/5","GUBRF\thttps://tr.investing.com/equities/gubre-fabrik.-commentary\thttps://tr.investing.com/equities/gubre-fabrik.-commentary/2\thttps://tr.investing.com/equities/gubre-fabrik.-commentary/3\thttps://tr.investing.com/equities/gubre-fabrik.-commentary/4\thttps://tr.investing.com/equities/gubre-fabrik.-commentary/5","GWIND\thttps://tr.investing.com/equities/galata-wind-enerji-anonim-sirket-commentary\thttps://tr.investing.com/equities/galata-wind-enerji-anonim-sirket-commentary/2\thttps://tr.investing.com/equities/galata-wind-enerji-anonim-sirket-commentary/3\thttps://tr.investing.com/equities/galata-wind-enerji-anonim-sirket-commentary/4\thttps://tr.investing.com/equities/galata-wind-enerji-anonim-sirket-commentary/5","HALKB\thttps://tr.investing.com/equities/t.-halk-bankasi-commentary\thttps://tr.investing.com/equities/t.-halk-bankasi-commentary/2\thttps://tr.investing.com/equities/t.-halk-bankasi-commentary/3\thttps://tr.investing.com/equities/t.-halk-bankasi-commentary/4\thttps://tr.investing.com/equities/t.-halk-bankasi-commentary/5","HEKTS\thttps://tr.investing.com/equities/hektas-commentary\thttps://tr.investing.com/equities/hektas-commentary/2\thttps://tr.investing.com/equities/hektas-commentary/3\thttps://tr.investing.com/equities/hektas-commentary/4\thttps://tr.investing.com/equities/hektas-commentary/5","IPEKE\thttps://tr.investing.com/equities/ipek-dogal-enerji-commentary\thttps://tr.investing.com/equities/ipek-dogal-enerji-commentary/2\thttps://tr.investing.com/equities/ipek-dogal-enerji-commentary/3\thttps://tr.investing.com/equities/ipek-dogal-enerji-commentary/4\thttps://tr.investing.com/equities/ipek-dogal-enerji-commentary/5","ISCTR\thttps://tr.investing.com/equities/is-bankasi-(c)-commentary\thttps://tr.investing.com/equities/is-bankasi-(c)-commentary/2\thttps://tr.investing.com/equities/is-bankasi-(c)-commentary/3\thttps://tr.investing.com/equities/is-bankasi-(c)-commentary/4\thttps://tr.investing.com/equities/is-bankasi-(c)-commentary/5","ISDMR\thttps://tr.investing.com/equities/iskenderun-demir-ve-celik-as-commentary\thttps://tr.investing.com/equities/iskenderun-demir-ve-celik-as-commentary/2\thttps://tr.investing.com/equities/iskenderun-demir-ve-celik-as-commentary/3\thttps://tr.investing.com/equities/iskenderun-demir-ve-celik-as-commentary/4\thttps://tr.investing.com/equities/iskenderun-demir-ve-celik-as-commentary/5","ISGYO\thttps://tr.investing.com/equities/is-gmyo-commentary\thttps://tr.investing.com/equities/is-gmyo-commentary/2\thttps://tr.investing.com/equities/is-gmyo-commentary/3\thttps://tr.investing.com/equities/is-gmyo-commentary/4\thttps://tr.investing.com/equities/is-gmyo-commentary/5"
]

table_lines2 = [
"ISMEN\thttps://tr.investing.com/equities/is-y.-men.-deg.-commentary\thttps://tr.investing.com/equities/is-y.-men.-deg.-commentary/2\thttps://tr.investing.com/equities/is-y.-men.-deg.-commentary/3\thttps://tr.investing.com/equities/is-y.-men.-deg.-commentary/4\thttps://tr.investing.com/equities/is-y.-men.-deg.-commentary/5","IZENR\thttps://tr.investing.com/equities/izdemir-enerji-elektrik-uretim-as-commentary\thttps://tr.investing.com/equities/izdemir-enerji-elektrik-uretim-as-commentary/2\thttps://tr.investing.com/equities/izdemir-enerji-elektrik-uretim-as-commentary/3\thttps://tr.investing.com/equities/izdemir-enerji-elektrik-uretim-as-commentary/4\thttps://tr.investing.com/equities/izdemir-enerji-elektrik-uretim-as-commentary/5","IZMDC\thttps://tr.investing.com/equities/izmir-demir-celik-commentary\thttps://tr.investing.com/equities/izmir-demir-celik-commentary/2\thttps://tr.investing.com/equities/izmir-demir-celik-commentary/3\thttps://tr.investing.com/equities/izmir-demir-celik-commentary/4\thttps://tr.investing.com/equities/izmir-demir-celik-commentary/5","KARSN\thttps://tr.investing.com/equities/karsan-otomotiv-commentary\thttps://tr.investing.com/equities/karsan-otomotiv-commentary/2\thttps://tr.investing.com/equities/karsan-otomotiv-commentary/3\thttps://tr.investing.com/equities/karsan-otomotiv-commentary/4\thttps://tr.investing.com/equities/karsan-otomotiv-commentary/5","KAYSE\thttps://tr.investing.com/equities/kayseri-seker-fabrikasi-as-commentary\thttps://tr.investing.com/equities/kayseri-seker-fabrikasi-as-commentary/2\thttps://tr.investing.com/equities/kayseri-seker-fabrikasi-as-commentary/3\thttps://tr.investing.com/equities/kayseri-seker-fabrikasi-as-commentary/4\thttps://tr.investing.com/equities/kayseri-seker-fabrikasi-as-commentary/5","KCAER\thttps://tr.investing.com/equities/kocaer-celik-sanayi-ve-ticaret-as-commentary\thttps://tr.investing.com/equities/kocaer-celik-sanayi-ve-ticaret-as-commentary/2\thttps://tr.investing.com/equities/kocaer-celik-sanayi-ve-ticaret-as-commentary/3\thttps://tr.investing.com/equities/kocaer-celik-sanayi-ve-ticaret-as-commentary/4\thttps://tr.investing.com/equities/kocaer-celik-sanayi-ve-ticaret-as-commentary/5","KCHOL\thttps://tr.investing.com/equities/koc-holding-commentary\thttps://tr.investing.com/equities/koc-holding-commentary/2\thttps://tr.investing.com/equities/koc-holding-commentary/3\thttps://tr.investing.com/equities/koc-holding-commentary/4\thttps://tr.investing.com/equities/koc-holding-commentary/5","KLSER\thttps://tr.investing.com/equities/kaleseramik-canakkale-kalebodur-commentary\thttps://tr.investing.com/equities/kaleseramik-canakkale-kalebodur-commentary/2\thttps://tr.investing.com/equities/kaleseramik-canakkale-kalebodur-commentary/3\thttps://tr.investing.com/equities/kaleseramik-canakkale-kalebodur-commentary/4\thttps://tr.investing.com/equities/kaleseramik-canakkale-kalebodur-commentary/5","KMPUR\thttps://tr.investing.com/equities/kimteks-poliuretan-sanayi-ve-commentary\thttps://tr.investing.com/equities/kimteks-poliuretan-sanayi-ve-commentary/2\thttps://tr.investing.com/equities/kimteks-poliuretan-sanayi-ve-commentary/3\thttps://tr.investing.com/equities/kimteks-poliuretan-sanayi-ve-commentary/4\thttps://tr.investing.com/equities/kimteks-poliuretan-sanayi-ve-commentary/5","KONTR\thttps://tr.investing.com/equities/kontrolmatik-teknoloji-enerji-ve-mu-commentary\thttps://tr.investing.com/equities/kontrolmatik-teknoloji-enerji-ve-mu-commentary/2\thttps://tr.investing.com/equities/kontrolmatik-teknoloji-enerji-ve-mu-commentary/3\thttps://tr.investing.com/equities/kontrolmatik-teknoloji-enerji-ve-mu-commentary/4\thttps://tr.investing.com/equities/kontrolmatik-teknoloji-enerji-ve-mu-commentary/5","KONYA\thttps://tr.investing.com/equities/konya-cimento-commentary\thttps://tr.investing.com/equities/konya-cimento-commentary/2\thttps://tr.investing.com/equities/konya-cimento-commentary/3\thttps://tr.investing.com/equities/konya-cimento-commentary/4\thttps://tr.investing.com/equities/konya-cimento-commentary/5","KORDS\thttps://tr.investing.com/equities/kordsa-global-commentary\thttps://tr.investing.com/equities/kordsa-global-commentary/2\thttps://tr.investing.com/equities/kordsa-global-commentary/3\thttps://tr.investing.com/equities/kordsa-global-commentary/4\thttps://tr.investing.com/equities/kordsa-global-commentary/5","KOZAA\thttps://tr.investing.com/equities/koza-madencilik-commentary\thttps://tr.investing.com/equities/koza-madencilik-commentary/2\thttps://tr.investing.com/equities/koza-madencilik-commentary/3\thttps://tr.investing.com/equities/koza-madencilik-commentary/4\thttps://tr.investing.com/equities/koza-madencilik-commentary/5","KOZAL\thttps://tr.investing.com/equities/koza-altin-commentary\thttps://tr.investing.com/equities/koza-altin-commentary/2\thttps://tr.investing.com/equities/koza-altin-commentary/3\thttps://tr.investing.com/equities/koza-altin-commentary/4\thttps://tr.investing.com/equities/koza-altin-commentary/5","KRDMD\thttps://tr.investing.com/equities/kardemir-(d)-commentary\thttps://tr.investing.com/equities/kardemir-(d)-commentary/2\thttps://tr.investing.com/equities/kardemir-(d)-commentary/3\thttps://tr.investing.com/equities/kardemir-(d)-commentary/4\thttps://tr.investing.com/equities/kardemir-(d)-commentary/5","MAVI\thttps://tr.investing.com/equities/mavi-giyim-sanayi-ve-ticaret-as-commentary\thttps://tr.investing.com/equities/mavi-giyim-sanayi-ve-ticaret-as-commentary/2\thttps://tr.investing.com/equities/mavi-giyim-sanayi-ve-ticaret-as-commentary/3\thttps://tr.investing.com/equities/mavi-giyim-sanayi-ve-ticaret-as-commentary/4\thttps://tr.investing.com/equities/mavi-giyim-sanayi-ve-ticaret-as-commentary/5","MGROS\thttps://tr.investing.com/equities/migros-ticaret-commentary\thttps://tr.investing.com/equities/migros-ticaret-commentary/2\thttps://tr.investing.com/equities/migros-ticaret-commentary/3\thttps://tr.investing.com/equities/migros-ticaret-commentary/4\thttps://tr.investing.com/equities/migros-ticaret-commentary/5","MIATK\thttps://tr.investing.com/equities/mia-teknoloji-as-commentary\thttps://tr.investing.com/equities/mia-teknoloji-as-commentary/2\thttps://tr.investing.com/equities/mia-teknoloji-as-commentary/3\thttps://tr.investing.com/equities/mia-teknoloji-as-commentary/4\thttps://tr.investing.com/equities/mia-teknoloji-as-commentary/5","ODAS\thttps://tr.investing.com/equities/odas-elektrik-commentary\thttps://tr.investing.com/equities/odas-elektrik-commentary/2\thttps://tr.investing.com/equities/odas-elektrik-commentary/3\thttps://tr.investing.com/equities/odas-elektrik-commentary/4\thttps://tr.investing.com/equities/odas-elektrik-commentary/5","OTKAR\thttps://tr.investing.com/equities/otokar-commentary\thttps://tr.investing.com/equities/otokar-commentary/2\thttps://tr.investing.com/equities/otokar-commentary/3\thttps://tr.investing.com/equities/otokar-commentary/4\thttps://tr.investing.com/equities/otokar-commentary/5","OYAKC\thttps://tr.investing.com/equities/mardin-cimento-commentary\thttps://tr.investing.com/equities/mardin-cimento-commentary/2\thttps://tr.investing.com/equities/mardin-cimento-commentary/3\thttps://tr.investing.com/equities/mardin-cimento-commentary/4\thttps://tr.investing.com/equities/mardin-cimento-commentary/5","PENTA\thttps://tr.investing.com/equities/penta-teknoloji-urunleri-commentary\thttps://tr.investing.com/equities/penta-teknoloji-urunleri-commentary/2\thttps://tr.investing.com/equities/penta-teknoloji-urunleri-commentary/3\thttps://tr.investing.com/equities/penta-teknoloji-urunleri-commentary/4\thttps://tr.investing.com/equities/penta-teknoloji-urunleri-commentary/5","PETKM\thttps://tr.investing.com/equities/petkim-commentary\thttps://tr.investing.com/equities/petkim-commentary/2\thttps://tr.investing.com/equities/petkim-commentary/3\thttps://tr.investing.com/equities/petkim-commentary/4\thttps://tr.investing.com/equities/petkim-commentary/5","PGSUS\thttps://tr.investing.com/equities/pegasus-hava-tasimaciligi-commentary\thttps://tr.investing.com/equities/pegasus-hava-tasimaciligi-commentary/2\thttps://tr.investing.com/equities/pegasus-hava-tasimaciligi-commentary/3\thttps://tr.investing.com/equities/pegasus-hava-tasimaciligi-commentary/4\thttps://tr.investing.com/equities/pegasus-hava-tasimaciligi-commentary/5","QUAGR\thttps://tr.investing.com/equities/qua-granite-hayal-commentary\thttps://tr.investing.com/equities/qua-granite-hayal-commentary/2\thttps://tr.investing.com/equities/qua-granite-hayal-commentary/3\thttps://tr.investing.com/equities/qua-granite-hayal-commentary/4\thttps://tr.investing.com/equities/qua-granite-hayal-commentary/5","SAHOL\thttps://tr.investing.com/equities/sabanci-holding-commentary\thttps://tr.investing.com/equities/sabanci-holding-commentary/2\thttps://tr.investing.com/equities/sabanci-holding-commentary/3\thttps://tr.investing.com/equities/sabanci-holding-commentary/4\thttps://tr.investing.com/equities/sabanci-holding-commentary/5","SASA\thttps://tr.investing.com/equities/sasa-polyester-commentary\thttps://tr.investing.com/equities/sasa-polyester-commentary/2\thttps://tr.investing.com/equities/sasa-polyester-commentary/3\thttps://tr.investing.com/equities/sasa-polyester-commentary/4\thttps://tr.investing.com/equities/sasa-polyester-commentary/5","SDTTR\thttps://tr.investing.com/equities/sdt-uzay-ve-savunma-teknolojileri-commentary\thttps://tr.investing.com/equities/sdt-uzay-ve-savunma-teknolojileri-commentary/2\thttps://tr.investing.com/equities/sdt-uzay-ve-savunma-teknolojileri-commentary/3\thttps://tr.investing.com/equities/sdt-uzay-ve-savunma-teknolojileri-commentary/4\thttps://tr.investing.com/equities/sdt-uzay-ve-savunma-teknolojileri-commentary/5","SISE\thttps://tr.investing.com/equities/sise-cam-commentary\thttps://tr.investing.com/equities/sise-cam-commentary/2\thttps://tr.investing.com/equities/sise-cam-commentary/3\thttps://tr.investing.com/equities/sise-cam-commentary/4\thttps://tr.investing.com/equities/sise-cam-commentary/5","SKBNK\thttps://tr.investing.com/equities/sekerbank-commentary\thttps://tr.investing.com/equities/sekerbank-commentary/2\thttps://tr.investing.com/equities/sekerbank-commentary/3\thttps://tr.investing.com/equities/sekerbank-commentary/4\thttps://tr.investing.com/equities/sekerbank-commentary/5","SMRTG\thttps://tr.investing.com/equities/smart-gunes-enerjisi-teknolojileri-commentary\thttps://tr.investing.com/equities/smart-gunes-enerjisi-teknolojileri-commentary/2\thttps://tr.investing.com/equities/smart-gunes-enerjisi-teknolojileri-commentary/3\thttps://tr.investing.com/equities/smart-gunes-enerjisi-teknolojileri-commentary/4\thttps://tr.investing.com/equities/smart-gunes-enerjisi-teknolojileri-commentary/5","SOKM\thttps://tr.investing.com/equities/sok-marketler-commentary\thttps://tr.investing.com/equities/sok-marketler-commentary/2\thttps://tr.investing.com/equities/sok-marketler-commentary/3\thttps://tr.investing.com/equities/sok-marketler-commentary/4\thttps://tr.investing.com/equities/sok-marketler-commentary/5","TATEN\thttps://tr.investing.com/equities/tatlipinar-enerji-uretim-as-commentary\thttps://tr.investing.com/equities/tatlipinar-enerji-uretim-as-commentary/2\thttps://tr.investing.com/equities/tatlipinar-enerji-uretim-as-commentary/3\thttps://tr.investing.com/equities/tatlipinar-enerji-uretim-as-commentary/4\thttps://tr.investing.com/equities/tatlipinar-enerji-uretim-as-commentary/5","TAVHL\thttps://tr.investing.com/equities/tav-havalimanlari-commentary\thttps://tr.investing.com/equities/tav-havalimanlari-commentary/2\thttps://tr.investing.com/equities/tav-havalimanlari-commentary/3\thttps://tr.investing.com/equities/tav-havalimanlari-commentary/4\thttps://tr.investing.com/equities/tav-havalimanlari-commentary/5","TCELL\thttps://tr.investing.com/equities/turkcell-commentary\thttps://tr.investing.com/equities/turkcell-commentary/2\thttps://tr.investing.com/equities/turkcell-commentary/3\thttps://tr.investing.com/equities/turkcell-commentary/4\thttps://tr.investing.com/equities/turkcell-commentary/5","THYAO\thttps://tr.investing.com/equities/turk-hava-yollari-commentary\thttps://tr.investing.com/equities/turk-hava-yollari-commentary/2\thttps://tr.investing.com/equities/turk-hava-yollari-commentary/3\thttps://tr.investing.com/equities/turk-hava-yollari-commentary/4\thttps://tr.investing.com/equities/turk-hava-yollari-commentary/5","TKFEN\thttps://tr.investing.com/equities/tekfen-holding-commentary\thttps://tr.investing.com/equities/tekfen-holding-commentary/2\thttps://tr.investing.com/equities/tekfen-holding-commentary/3\thttps://tr.investing.com/equities/tekfen-holding-commentary/4\thttps://tr.investing.com/equities/tekfen-holding-commentary/5","TOASO\thttps://tr.investing.com/equities/tofas-oto.-fab.-commentary\thttps://tr.investing.com/equities/tofas-oto.-fab.-commentary/2\thttps://tr.investing.com/equities/tofas-oto.-fab.-commentary/3\thttps://tr.investing.com/equities/tofas-oto.-fab.-commentary/4\thttps://tr.investing.com/equities/tofas-oto.-fab.-commentary/5","TSKB\thttps://tr.investing.com/equities/t.s.k.b.-commentary\thttps://tr.investing.com/equities/t.s.k.b.-commentary/2\thttps://tr.investing.com/equities/t.s.k.b.-commentary/3\thttps://tr.investing.com/equities/t.s.k.b.-commentary/4\thttps://tr.investing.com/equities/t.s.k.b.-commentary/5","TTKOM\thttps://tr.investing.com/equities/turk-telekom-commentary\thttps://tr.investing.com/equities/turk-telekom-commentary/2\thttps://tr.investing.com/equities/turk-telekom-commentary/3\thttps://tr.investing.com/equities/turk-telekom-commentary/4\thttps://tr.investing.com/equities/turk-telekom-commentary/5","TTRAK\thttps://tr.investing.com/equities/turk-traktor-commentary\thttps://tr.investing.com/equities/turk-traktor-commentary/2\thttps://tr.investing.com/equities/turk-traktor-commentary/3\thttps://tr.investing.com/equities/turk-traktor-commentary/4\thttps://tr.investing.com/equities/turk-traktor-commentary/5","TUKAS\thttps://tr.investing.com/equities/tukas-commentary\thttps://tr.investing.com/equities/tukas-commentary/2\thttps://tr.investing.com/equities/tukas-commentary/3\thttps://tr.investing.com/equities/tukas-commentary/4\thttps://tr.investing.com/equities/tukas-commentary/5","TUPRS\thttps://tr.investing.com/equities/tupras-commentary\thttps://tr.investing.com/equities/tupras-commentary/2\thttps://tr.investing.com/equities/tupras-commentary/3\thttps://tr.investing.com/equities/tupras-commentary/4\thttps://tr.investing.com/equities/tupras-commentary/5","ULKER\thttps://tr.investing.com/equities/ulker-biskuvi-commentary\thttps://tr.investing.com/equities/ulker-biskuvi-commentary/2\thttps://tr.investing.com/equities/ulker-biskuvi-commentary/3\thttps://tr.investing.com/equities/ulker-biskuvi-commentary/4\thttps://tr.investing.com/equities/ulker-biskuvi-commentary/5","VAKBN\thttps://tr.investing.com/equities/vakiflar-bankasi-commentary\thttps://tr.investing.com/equities/vakiflar-bankasi-commentary/2\thttps://tr.investing.com/equities/vakiflar-bankasi-commentary/3\thttps://tr.investing.com/equities/vakiflar-bankasi-commentary/4\thttps://tr.investing.com/equities/vakiflar-bankasi-commentary/5","VESTL\thttps://tr.investing.com/equities/vestel-commentary\thttps://tr.investing.com/equities/vestel-commentary/2\thttps://tr.investing.com/equities/vestel-commentary/3\thttps://tr.investing.com/equities/vestel-commentary/4\thttps://tr.investing.com/equities/vestel-commentary/5","YEOTK\thttps://tr.investing.com/equities/yeo-teknoloji-enerji-ve-endustri-as-commentary\thttps://tr.investing.com/equities/yeo-teknoloji-enerji-ve-endustri-as-commentary/2\thttps://tr.investing.com/equities/yeo-teknoloji-enerji-ve-endustri-as-commentary/3\thttps://tr.investing.com/equities/yeo-teknoloji-enerji-ve-endustri-as-commentary/4\thttps://tr.investing.com/equities/yeo-teknoloji-enerji-ve-endustri-as-commentary/5","YKBNK\thttps://tr.investing.com/equities/yapi-ve-kredi-bank.-commentary\thttps://tr.investing.com/equities/yapi-ve-kredi-bank.-commentary/2\thttps://tr.investing.com/equities/yapi-ve-kredi-bank.-commentary/3\thttps://tr.investing.com/equities/yapi-ve-kredi-bank.-commentary/4\thttps://tr.investing.com/equities/yapi-ve-kredi-bank.-commentary/5","YYLGD\thttps://tr.investing.com/equities/yayla-agro-gida-sanayi-ve-ticaret-commentary\thttps://tr.investing.com/equities/yayla-agro-gida-sanayi-ve-ticaret-commentary/2\thttps://tr.investing.com/equities/yayla-agro-gida-sanayi-ve-ticaret-commentary/3\thttps://tr.investing.com/equities/yayla-agro-gida-sanayi-ve-ticaret-commentary/4\thttps://tr.investing.com/equities/yayla-agro-gida-sanayi-ve-ticaret-commentary/5","ZOREN\thttps://tr.investing.com/equities/zorlu-enerji-commentary\thttps://tr.investing.com/equities/zorlu-enerji-commentary/2\thttps://tr.investing.com/equities/zorlu-enerji-commentary/3\thttps://tr.investing.com/equities/zorlu-enerji-commentary/4\thttps://tr.investing.com/equities/zorlu-enerji-commentary/5"
]

table_lines = table_lines1 + table_lines2

# Iterate over each line in the table
for line in table_lines:
    # Split the line by tabs ("\t") to separate the Trade and Links information
    elements = line.strip().split("\t")
    
    # Extract the trade name
    trade = elements[0]
    
    # Extract the links and convert them into a list
    links = elements[1:]
    
    # Store the trade and links information in the dictionary
    trade_links_dict[trade] = links

Bist100_part1 = ['AEFES','AGHOL','AHGAZ','AKBNK','AKCNS','AKFYE','AKSA','AKSEN','ALARK','ALBRK','ALFAS','ARCLK','ASELS','ASGYO','ASTOR','BERA','BIENY','BIMAS','BIOEN','BOBET', \
           'BRSAN','BRYAT','BUCIM','CANTE','CCOLA','CIMSA','CWENE','DOAS','DOHOL','ECILC','ECZYT','EGEEN','EKGYO','ENERY','ENJSA','ENKAI','EREGL','EUPWR','EUREN','FROTO', \
           'GARAN','GESAN','GUBRF','GWIND','HALKB','HEKTS','IPEKE','ISCTR','ISDMR','ISGYO','ISMEN']

Bist100_part2 = ['IZENR','IZMDC','KARSN','KAYSE','KCAER','KCHOL','KLSER','KMPUR','KONTR', \
           'KONYA','KORDS','KOZAA','KOZAL','KRDMD','MAVI','MGROS','MIATK','ODAS','OTKAR','OYAKC','PENTA','PETKM','PGSUS','QUAGR','SAHOL','SASA','SDTTR','SISE','SKBNK','SMRTG',\
           'SOKM','TATEN','TAVHL','TCELL','THYAO','TKFEN','TOASO','TSKB','TTKOM','TTRAK','TUKAS','TUPRS','ULKER','VAKBN','VESTL','YEOTK','YKBNK','YYLGD','ZOREN']


#########  Creating web scrapping func. #########

def web_scraping_1 (Bistlist):

    myuseragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument(f"user-agent={myuseragent}")
    # chromeOptions.add_argument("--headless")
    browser = webdriver.Chrome(options=chromeOptions)
    start_time = time.time()
    df_part1 = pd.DataFrame(columns = ["Stock", "User", "Comment", "Comment Time"])

    for stock in Bistlist:
        for x in range(0,5):
            browser.get(trade_links_dict[stock][x])
            browser.delete_all_cookies()
            time.sleep(random.randint(2, 6))

            # Scroll to the middle of the page
            height = browser.execute_script("return document.documentElement.scrollHeight;")
            browser.execute_script(f"window.scrollTo(0, {height // 4});")
            time.sleep(random.randint(2, 4))

            # Scroll to the middle of the page
            height = browser.execute_script("return document.documentElement.scrollHeight;")
            browser.execute_script(f"window.scrollTo(0, {height // 1.4});")
            time.sleep(random.randint(2, 4))

            # Scroll to the end of the page
            browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            source = browser.page_source
            soup = BeautifulSoup(source, "html.parser")
            metinler = soup.find_all("div",attrs={"class":"border-t border-[#E6E9EB]"})
            each_link = []

            for metin in metinler:
                comment = metin.find("div", attrs={"class":"break-words leading-5"})
                time_info = metin.find("span", attrs={"class":"text-[#5B616E]"})
                user_info = metin.find("a", attrs={"class":"mb-1 font-bold hover:text-[#1256A0] hover:underline"})

                if comment:
                    comment_ = comment.text
                    comment_time = time_info.text
                    user = user_info.text
                    each_link.append([stock, user, comment_, comment_time])

            df = pd.DataFrame(each_link, columns = ["Stock", "User", "Comment", "Comment Time"])
            df_part1 = pd.concat([df_part1, df], ignore_index=True)

            time.sleep(random.randint(2, 6))

            # if there are some comment which are not today, we'll not go further
            if not df["Comment Time"].str.contains("saat", case=False, na=False).any():
                break

            x += 1
            
    browser.quit()

    # end_time = time.time()
    # execution_time = (end_time - start_time) / 60
    # print("web_scraping_1 Execution time:", round(execution_time, 2), "minutes")

    df_part1.drop_duplicates(inplace=True)
    return df_part1


def web_scraping_2 (Bistlist):

    myuseragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument(f"user-agent={myuseragent}")
    # chromeOptions.add_argument("--headless")
    browser = webdriver.Chrome(options=chromeOptions)
    start_time = time.time()
    df_part2 = pd.DataFrame(columns = ["Stock", "User", "Comment", "Comment Time"])

    for stock in Bistlist:
        for x in range(0,5):
            browser.get(trade_links_dict[stock][x])
            browser.delete_all_cookies()
            time.sleep(random.randint(2, 6))

            # Scroll to the middle of the page
            height = browser.execute_script("return document.documentElement.scrollHeight;")
            browser.execute_script(f"window.scrollTo(0, {height // 4});")
            time.sleep(random.randint(2, 4))

            # Scroll to the middle of the page
            height = browser.execute_script("return document.documentElement.scrollHeight;")
            browser.execute_script(f"window.scrollTo(0, {height // 1.4});")
            time.sleep(random.randint(2, 4))

            # Scroll to the end of the page
            browser.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
            source = browser.page_source
            soup = BeautifulSoup(source, "html.parser")
            metinler = soup.find_all("div",attrs={"class":"border-t border-[#E6E9EB]"})
            each_link = []

            for metin in metinler:
                comment = metin.find("div", attrs={"class":"break-words leading-5"})
                time_info = metin.find("span", attrs={"class":"text-[#5B616E]"})
                user_info = metin.find("a", attrs={"class":"mb-1 font-bold hover:text-[#1256A0] hover:underline"})

                if comment:
                    comment_ = comment.text
                    comment_time = time_info.text
                    user = user_info.text
                    each_link.append([stock, user, comment_, comment_time])

            df = pd.DataFrame(each_link, columns = ["Stock", "User", "Comment", "Comment Time"])
            df_part2 = pd.concat([df_part2, df], ignore_index=True)

            time.sleep(random.randint(2, 6))

            # if there are some comment which are not today, we'll not go further
            if not df["Comment Time"].str.contains("saat", case=False, na=False).any():
                break

            x += 1
            
    browser.quit()

    # end_time = time.time()
    # execution_time = (end_time - start_time) / 60
    # print("web_scraping_2 Execution time:", round(execution_time, 2), "minutes")

    df_part2.drop_duplicates(inplace=True)
    return df_part2

#########  Merge, Filter and Arrange Result #########

def web_scraping_results ():
    df_part1 = web_scraping_1 (Bist100_part1)
    # filtering last 24 hours comments
    df_part1 = df_part1[df_part1["Comment Time"].str.contains("saat",case=False, na=False)]
    time.sleep(30)
    df_part2 = web_scraping_2 (Bist100_part2)
    # filtering last 24 hours comments
    df_part2 = df_part2[df_part2["Comment Time"].str.contains("saat",case=False, na=False)]
    
    df_final = pd.concat([df_part1, df_part2], ignore_index=True)
    return df_final

# Getting result
df_final = web_scraping_results()

# Lowercase
df_final["Comment"] = df_final["Comment"].apply(lambda x: " ".join(x.lower() for x in x.split()))

# Translation dictionary for Turkish to English characters
translation_dict = {
    'ı': 'i',
    'ğ': 'g',
    'ü': 'u',
    'ş': 's',
    'ö': 'o',
    'ç': 'c',
    'İ': 'I',
    'Ğ': 'G',
    'Ü': 'U',
    'Ş': 'S',
    'Ö': 'O',
    'Ç': 'C'
}

def translate_turkish_to_english(text):
    return text.translate(str.maketrans(translation_dict))
df_final["Comment"] = df_final["Comment"].apply(translate_turkish_to_english)

# Function to remove punctuation
def remove_punctuation(text):
    return re.sub(r'[^\w\s]', '', text)
df_final["Comment"] = df_final["Comment"].apply(remove_punctuation)

# Getting result 2
# Add 'Date' column as the first column
today_date = datetime.today().strftime('%Y-%m-%d')
df_final.insert(0, 'Date', today_date)

# Group by 'Stock' and count the number of rows for each group, then reset index
df_final2 = df_final.groupby(["Date","Stock"]).size().reset_index(name="Count")