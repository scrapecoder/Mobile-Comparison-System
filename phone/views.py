from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from urllib.request import Request
from urllib.error import HTTPError, URLError
from .models import TopRated, Popular, Flagship, SmartPhoneComparison
import os
import shutil
import requests
import json


def phone_4g(request):
    return render(request, "phone/phone_shortcut/4g_phone.html")


def best_display(request):
    return render(request, "phone/phone_shortcut/Best Display.html")


def gaming_phone(request):
    return render(request, "phone/phone_shortcut/gaming_phone.html")


def greator20(request):
    return render(request, "phone/phone_shortcut/greator_20k_phone.html")


def less10(request):
    return render(request, "phone/phone_shortcut/less_10k_phone.html")


def less20(request):
    return render(request, "phone/phone_shortcut/less_20k_phone.html")


def top_rated(request):
    session = requests.Session()
    try:
        url = 'https://www.kimovil.com/en'
        url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        ureq = uReq(url)

        uRead = ureq.read()

        ureq.close()
        soup = bs(uRead, 'lxml')

        find_Top_Rated = soup.find('div', {'class': 'home-section top-sales clear'}).find('ul', {'class', 'top-device-list clear'})

        for li in find_Top_Rated:
            title = li.find('span', {'class', 'title'}).text
            image_source = li.find('span', {'class', 'image'}).img['data-src']
            try:
                price = li.find('span', {'class', 'xx_inr'}).text
            except AttributeError:
                price = ''
            media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/Popular_phone/'
            local_filename = image_source.split('/')[-1]
            link = 'http:'
            link = link+image_source
            r = session.get(link, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=720):
                    f.write(chunk)

            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)
            rated = TopRated()
            rated.name = title
            rated.price = price
            rated.image = 'Top_Rated/'+local_filename
            rated.save()

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)

    return redirect('index-home')


def top_popular(request):
    session = requests.Session()
    try:
        url = 'https://www.kimovil.com/en'
        url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        ureq = uReq(url)

        uRead = ureq.read()

        ureq.close()
        soup = bs(uRead, 'lxml')

        find_popular_phone = soup.find('div', {'class': 'home-section top-having clear'}).find('ul', {'class', 'top-device-list clear'})

        for li in find_popular_phone:
            title = li.find('span', {'class', 'title'}).text
            image_source = li.find('span', {'class', 'image'}).img['data-src']
            try:
                price = li.find('span', {'class', 'xx_inr'}).text
            except AttributeError:
                price = ''

            media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/Popular_phone/'
            local_filename = image_source.split('/')[-1]
            link = 'http:'
            link = link+image_source
            r = session.get(link, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=720):
                    f.write(chunk)

            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)
            popular = Popular()
            popular.title = title
            popular.price = price
            popular.image = 'Popular_phone/'+local_filename
            popular.save()
    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)
    return redirect('index-home')


def flagship_phone(request):
    session = requests.Session()
    try:
        url = 'https://www.wired.com/gallery/best-android-phones/'
        url = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        ureq = uReq(url)

        uRead = ureq.read()

        ureq.close()
        soup = bs(uRead, 'lxml')
        page = soup.find('div', {'class': 'listicle-main-component__container'})
        head = page.findAll('div', {'class': 'listicle-item-product-component'}, limit=4)
        for flag in head:
            brand = flag.find('div', {'class', 'listicle-item-product-component__make'}).text
            model = flag.find('div', {'class', 'listicle-item-product-component__model'}).text
            image = flag.find('div', {'class', 'listicle-item-product-component__photo'})
            image_source = image.find('div', {'class', 'image-group-component'}).img['src']
            price = flag.find('div', {'class': 'listicle-item-product-component__price-container'}).find('span', {'class': 'listicle-item-product-component__price-value'}).text

            media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/flagship_phone/'
            if not image_source.startswith(("data:image", "javascript")):
                local_filename = image_source.split('/')[-1].split("?")[0]
                r = session.get(image_source, stream=True, verify=False)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=500):
                        f.write(chunk)

                current_image_absolute_path = os.path.abspath(local_filename)
                shutil.move(current_image_absolute_path, media_root)

            flagship = Flagship()
            flagship.brand = brand
            flagship.model = model
            flagship.price = price
            flagship.image = 'flagship_phone/'+local_filename
            flagship.save()

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)
    return redirect('index-home')


def smart_phone_comparison(request):
    session = requests.Session()

    my_url = 'https://versus.com/en'
    url = Request(my_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:

        ureq = uReq(url)

        uRead = ureq.read()

        ureq.close()

        page_soup = bs(uRead, "lxml")

        scripts = page_soup.find_all('script')
        for script in scripts:
            if 'window.__data=' in script.text:
                jsonStr = script.text
                jsonStr = jsonStr.split('window.__data=')[-1]

                jsonData = json.loads(jsonStr)
        phones = jsonData['landing']['trendings']['phone']['list']
        i = 0
        for each in phones:
            print(i)
            i = i + 1
            root_url = 'https://versus.dadi.network'
            popImage = root_url + each['popImage']
            rivalImage = root_url + each['rivalImage']
            split1 = rivalImage.split('/')
            name1 = split1[3].title().replace('-', ' ')
            split2 = popImage.split('/')
            name2 = split2[3].title().replace('-', ' ')
            media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/phone_comparison/'
            comparison = SmartPhoneComparison()
            comparison.name1 = name1
            comparison.name2 = name2
            image_name1 = name1+'.jpg'
            image_name2 = name2+'.jpg'
            if os.path.isfile('C:/Users/Goku/PycharmProjects/mysite/media/phone_comparison/' + image_name1):
                pass
            else:
                r = session.get(rivalImage, stream=True, verify=False)
                with open(image_name1, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=720):
                            f.write(chunk)
                current_image_absolute_path = os.path.abspath(image_name1)
                shutil.move(current_image_absolute_path, media_root)

            comparison.image1 = 'phone_comparison/' + image_name1

            if os.path.isfile('C:/Users/Goku/PycharmProjects/mysite/media/phone_comparison/' + image_name2):
                pass
            else:
                r = session.get(popImage, stream=True, verify=False)
                with open(image_name2, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=720):
                        f.write(chunk)
                current_image_absolute_path = os.path.abspath(image_name2)
                shutil.move(current_image_absolute_path, media_root)
            comparison.image2 = 'phone_comparison/' + image_name2
            comparison.save()

    except HTTPError as e:
        print(e)
    except URLError as e:
        print(e)
    except AttributeError as e:
        print(e)
    except ValueError as e:
        print(e)
    return redirect('index-home')






