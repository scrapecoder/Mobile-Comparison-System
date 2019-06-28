from django.shortcuts import (render,
                              HttpResponse,
                              get_object_or_404,
                              redirect)
from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, PhoneType
from phone.models import (NewPhone,
                          TopRated,
                          Popular,
                          Flagship,
                          SmartPhoneComparison)
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq
from urllib.request import Request
from urllib.error import HTTPError
from django.template.loader import render_to_string
from django.contrib import messages
from users.forms import *
import re
import os
import shutil
import requests, json
from django.http import JsonResponse
from collections import defaultdict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.template import Library


def index(request):
    context = {
        'phone_type': PhoneType.objects.all(),
        'new_phone': NewPhone.objects.all(),
        'top_phone': TopRated.objects.all(),
        'popular_phone': Popular.objects.all(),
        'flagship_phone': Flagship.objects.all(),
        'smart_compare': SmartPhoneComparison.objects.all()
    }
    return render(request, 'prodcutSearch/index.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'prodcutSearch/blog.html'
    context_object_name = 'posts'
    ordering = ['-data_posted']
    paginate_by = 2


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'prodcutSearch/blog_form.html'
    fields = ['title', 'image', 'smallContent', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'prodcutSearch/blog_form.html'
    fields = ['title', 'image', 'smallContent', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/blog/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    comments = Comment.objects.filter(post=post, reply=None).order_by('-id')

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)

        if comment_form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_s = None
            if reply_id:
                comment_s = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content,  reply=comment_s)
            comment.save()

    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
    }
    return render(request, 'prodcutSearch/post_detail.html', context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = None
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes()
    }

    if request.is_ajax():
        html = render_to_string('prodcutSearch/like_section.html', context, request=request)

        return JsonResponse({'form': html})


def blog(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(requests, 'prodcutSearch/blog.html', context)

register = Library()
@register.filter(is_safe=True)
def device_index(request):
        if request.method == 'GET':
            query = request.GET.get('phone_search_bar')
            if query:
                session = requests.Session()
                search = query.lower()
                if 'redmi note 7' == search or 'xiaomi' in search:
                    pass
                else:
                    if re.compile('redmi').search(search) or re.compile('pocophone').search(search):
                        search = 'xiaomi '+search
                p_search = "-".join(search.split())
                url = 'https://www.kimovil.com/en/where-to-buy-'+p_search
                rate_url = "https://www.kimovil.com/en/opinions/" + p_search

                try:
                    myurl = Request(rate_url, headers={'User-Agent': 'Mozilla/5.0'})
                    uReq = ureq(myurl)
                    uRead = uReq.read()
                    uReq.close()
                    soup_rate = bs(uRead, 'lxml')
                    myurl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    uReq = ureq(myurl)
                    uRead = uReq.read()
                    uReq.close()
                    soup = bs(uRead, 'lxml')

                    phone_search_image = soup.find('div', {'class': 'wrapp'}).find('img')['src']
                    device_profile = soup.find('div', {'id': 'device-profile'})
                    if device_profile.findAll('div', {'class': 'row user-opinion-questions'}):
                        unwanted = device_profile.find_all('div', {'class': 'row user-opinion-questions'})
                        for i in unwanted:
                            i.decompose()
                    if device_profile.findAll('div', {'class': 'row sample-photos'}):
                        unwanted = device_profile.find_all('div', {'class': 'row sample-photos'})
                        for i in unwanted:
                            i.decompose()
                    unwanted = device_profile.find('div', {'id': 'country-coverage'})
                    unwanted.extract()
                    unwanted = device_profile.find_all('a')
                    for a in unwanted:
                        a.decompose()
                    model = soup.find('h1', {'class': 'h1'})
                    unwanted = model.find('span')
                    unwanted.extract()
                    phone_model = model.text.strip()

                    key = []
                    table_sub_key = []
                    table_value = []
                    rating = []
                    device_section = device_profile.findAll('div', {'class': 'table'})

                except HTTPError:
                    messages.success(request, f'Page Not Found')
                    return render(request, 'phone/phone_Error.html')

                try:
                    for row in device_section:
                        table_head = row.findAll('div', {'class', 'cell left'})
                        key.append([head.find('h3', {'class': 'h4'}).text for head in table_head])
                        table = row.findAll('div', {'class', 'cell right'})
                        for sub_row in table:
                            sub_table = sub_row.findAll('dl', limit=1)
                            for sub_key in sub_table:
                                subs_key = sub_key.findAll('dt')
                                subs_value = sub_key.findAll('dd')
                                table_sub_key.append([key.text.replace('\n', '').strip() for key in subs_key])
                                table_value.append([value.text.replace('\n', '').strip() for value in subs_value])

                    if soup_rate.find('section', {'class': 'section user-val-opinions clear'}):
                        rate = soup_rate.find('section', {'class': 'section user-val-opinions clear'}).find('div', {
                            'class': 'user-val-block'})
                        left_block = rate.find('div', {'class': 'left'}).find('div', {'class': 'user-val-overall-note'})
                        left_value = left_block.find('span')
                        left_value.decompose()
                        rating.append(left_block.text.replace('\n', '').strip())

                        right_block = rate.find('div', {'class': 'right'}).find('ul')

                        right_value = right_block.findAll('li')
                        for li in right_value:
                            rating.append(li.find('b').text.replace('\n', '').strip())
                    elif soup_rate.find('section', {'class': 'section main-opinions clear'}).find('div', {'class': 'right'}):
                        rate = soup_rate.find('section', {'class': 'section main-opinions clear'}).find('div', {
                            'class': 'right'})
                        left_block = rate.findAll('li', limit=6)
                        for r in left_block:
                            left_value = r.find('div', {'class': 'rating'}).text
                            rating.append(left_value)
                    else:
                        pass

                    media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/'
                    local_filename = search+'.jpg'
                    if os.path.isfile('C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/'+local_filename):
                        pass
                    else:
                        link = 'http:'
                        link = link + phone_search_image
                        r = session.get(link, stream=True, verify=False)
                        with open(local_filename, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=1220):
                                f.write(chunk)

                        current_image_absolute_path = os.path.abspath(local_filename)
                        shutil.move(current_image_absolute_path, media_root)
                    full_path = "/media/phone_search_image/"+local_filename

                    d3 = {}
                    a = 0
                    for k in range(len(key)):
                        for i in range(len(key[k])):
                            if key[k][i] not in d3.keys(): d3[key[k][i]] = {}
                            for j in range(len(table_sub_key[a])):
                                d3[key[k][i]][table_sub_key[a][j]] = table_value[a][j]
                            a = a + 1
                except AttributeError as e:
                    print(e)
                except TypeError as e:
                    print(e)
            return render(request, 'phone/device_profile.html', {'final': d3, 'full_path': full_path, 'Brand': phone_model, 'rating': mark_safe(json.dumps(rating))})

register = Library()
@register.filter(is_safe=True)
def index_phone(request, name=None):
    if name:
        query = name
        session = requests.Session()
        search = query.lower()
        p_search = "-".join(search.split())
        url = 'https://www.kimovil.com/en/where-to-buy-' + p_search
        rate_url = "https://www.kimovil.com/en/opinions/"+p_search
        try:

            myurl = Request(rate_url, headers={'User-Agent': 'Mozilla/5.0'})
            uReq = ureq(myurl)
            uRead = uReq.read()
            uReq.close()
            soup_rate = bs(uRead, 'lxml')
            myurl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            uReq = ureq(myurl)
            uRead = uReq.read()
            uReq.close()
            soup = bs(uRead, 'lxml')
            phone_search_image = soup.find('div', {'class': 'wrapp'}).find('img')['src']

            device_profile = soup.find('div', {'id': 'device-profile'})
            if device_profile.findAll('div', {'class': 'row user-opinion-questions'}):
                unwanted = device_profile.find_all('div', {'class': 'row user-opinion-questions'})
                for i in unwanted:
                    i.decompose()
            if device_profile.findAll('div', {'class': 'row sample-photos'}):
                unwanted = device_profile.find_all('div', {'class': 'row sample-photos'})
                for i in unwanted:
                    i.decompose()
            unwanted = device_profile.find('div', {'id': 'country-coverage'})
            unwanted.extract()
            unwanted_tag = device_profile.findAll('p')
            for span in unwanted_tag:
                span.decompose()

            unwanted = device_profile.find_all('a')
            for a in unwanted:
                a.decompose()
            model = soup.find('h1', {'class': 'h1'})
            unwanted = model.find('span')
            unwanted.extract()
            phone_model = model.text.strip()
            key = []
            table_sub_key = []
            table_value = []
            rating = []

            device_section = device_profile.findAll('div', {'class': 'table'})

        except HTTPError:
            messages.success(request, f'Page Not Found')
            return render(request, 'phone/phone_Error.html')
        try:
            for row in device_section:
                table_head = row.findAll('div', {'class', 'cell left'})
                key.append([head.find('h3', {'class': 'h4'}).text for head in table_head])
                table = row.findAll('div', {'class', 'cell right'})
                for sub_row in table:
                    sub_table = sub_row.findAll('dl', limit=1)
                    for sub_key in sub_table:
                        subs_key = sub_key.findAll('dt')
                        subs_value = sub_key.findAll('dd')
                        table_sub_key.append([key.text.replace('\n', '').strip() for key in subs_key])
                        table_value.append([value.text.strip() for value in subs_value])

            if soup_rate.find('section', {'class': 'section user-val-opinions clear'}):

                rate = soup_rate.find('section', {'class': 'section user-val-opinions clear'}).find('div', {
                    'class': 'user-val-block'})
                left_block = rate.find('div', {'class': 'left'}).find('div', {'class': 'user-val-overall-note'})
                left_value = left_block.find('span')
                left_value.decompose()
                rating.append(left_block.text.replace('\n', '').strip())

                right_block = rate.find('div', {'class': 'right'}).find('ul')

                right_value = right_block.findAll('li')
                for li in right_value:
                    rating.append(li.find('b').text.replace('\n', '').strip())

            elif soup_rate.find('section', {'class': 'section main-opinions clear'}).find('div', {'class': 'right'}):

                    rate = soup_rate.find('section', {'class': 'section main-opinions clear'}).find('div', {
                        'class': 'right'})
                    left_block = rate.findAll('li', limit=6)
                    for r in left_block:
                        left_value = r.find('div', {'class': 'rating'}).text
                        rating.append(left_value)
            else:
                pass

            media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/'
            local_filename = search + '.jpg'
            if os.path.isfile('C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/' + local_filename):
                pass
            else:
                link = 'http:'
                link = link + phone_search_image
                r = session.get(link, stream=True, verify=False)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1220):
                        f.write(chunk)

                current_image_absolute_path = os.path.abspath(local_filename)
                shutil.move(current_image_absolute_path, media_root)
            full_path = "/media/phone_search_image/" + local_filename
            Brand = table_value[0][0]
            d3 = {}
            a = 0
            for k in range(len(key)):
                for i in range(len(key[k])):
                    if key[k][i] not in d3.keys(): d3[key[k][i]] = {}
                    for j in range(len(table_sub_key[a])):
                        d3[key[k][i]][table_sub_key[a][j]] = table_value[a][j]
                    a = a + 1
        except AttributeError as e:
            print(e)
        except TypeError as e:
            print(e)
        except KeyError as e:
            print(e)
        return render(request, 'phone/device_profile.html', {'final': d3, 'full_path': full_path, 'Brand': phone_model, 'rating': mark_safe(json.dumps(rating))})


@method_decorator(csrf_exempt, name='POST')
def compare(request, value=None):
        session = requests.Session()
        if value:
            compare_res = value
            compare_res = list(compare_res.split("-"))

            for item in range(len(compare_res)):
                if 'redmi note 7' == compare_res[item] or 'xiaomi' in compare_res[item]:
                    pass
                else:

                    if re.compile('redmi').search(compare_res[item]) or re.compile('pocophone').search(compare_res[item]):
                        compare_res[item] = 'xiaomi ' + compare_res[item]

            phone_list = ','.join(e.lower() for e in compare_res)
            phone_list = '-'.join(phone_list.split())

        elif request.method == 'POST':
            compare_res = request.POST.getlist('brand')
            request.session['brand_name'] = compare_res
            for item in range(len(compare_res)):
                if 'redmi note 7' == compare_res[item] or 'xiaomi' in compare_res[item]:
                    pass
                else:
                    if re.compile('redmi').search(compare_res[item]) or re.compile('pocophone').search(compare_res[item]):
                        compare_res[item] = 'xiaomi ' + compare_res[item]

            phone_list = ','.join(e.lower() for e in compare_res)
            phone_list = '-'.join(phone_list.split())
        url = 'https://www.kimovil.com/en/compare/'+phone_list
        print(url)
        try:

            myurl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            uReq = ureq(myurl)

            uRead = uReq.read()

            uReq.close()

            soup = bs(uRead, 'lxml')
            table_head = []
            table_key = []
            table_sub_key = []
            table_value = []
            list_value = []
            name = soup.find('div', {'class': 'wrapper'}).find('div', {'class': 'c-table'})
            phone_title = name.findAll('div', {'class', 'h4'})
            title_list = [i.text.strip() for i in phone_title]
            request.session['brand_name'] = title_list

            rating_section = soup.findAll('div', {'class': 'c-table'})[2]
            rating_row = rating_section.findAll('div', {'class': 'c-row'})[1:]

            for value in rating_row:
                V = value.findAll('span')
                list_value.append([v.text for v in V])

            b = [[] for _ in range(len(list_value[0]))]
            for i in range(len(list_value)):
                for j in range(len(list_value[i])):
                    b[j].append(list_value[i][j])

            request.session['rating'] = b

            find_img = soup.find('div', {'class': 'wrapper'})
            title = find_img.findAll('div', {'class': 'h4'})
            image = find_img.findAll('img')

            for img in range(len(image)):
                image_title = title[img].text
                image_src = image[img]['data-src']
                media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/'
                local_filename = image_title + '.jpg'
                if os.path.isfile('C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/' + local_filename):
                    pass
                else:
                    link = 'http:'
                    link = link + image_src
                    r = session.get(link, stream=True, verify=False)
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1220):
                            f.write(chunk)

                    current_image_absolute_path = os.path.abspath(local_filename)
                    shutil.move(current_image_absolute_path, media_root)

            find_comparision_table = soup.find('div', {'class': 'comparisons-tables'})
            table_content = find_comparision_table.findAll('div', {'class': 'white-content clear'})[1:]
        except HTTPError:
            messages.success(request, f'Page Not Found')
            return render(request, 'phone/phone_Error.html')
        try:
            if table_content[len(table_content) - 1]['id'] == 'device-prices':
                table_content = table_content[:len(table_content) - 1]

            for item in table_content[1].find_all(
                    lambda tag: tag.name == 'h4' and ('Photos' in tag.text or 'Prototypes' in tag.text)):
                item.decompose()

            for wrapper in table_content:
                table_content_wrapper = wrapper.find('div', {'class': 'wrapper'})
                table_head.append(table_content_wrapper.find('h3').text)
                table_content_wrapper_key = table_content_wrapper.findAll('h4', {'class': 'h4'})
                table_key.append([table_content_wrapper_subkey.text for table_content_wrapper_subkey in table_content_wrapper_key])

                table_content_wrapper_table_clear = table_content_wrapper.findAll('div', {'class': 'c-table clear'})

                for table_content_wrapper_table_sub_clear in table_content_wrapper_table_clear:
                    table_content_wrapper_table_row = table_content_wrapper_table_sub_clear.findAll('div',
                                                                                                    {'class': 'c-row'})
                    table_sub_key.append(
                        [table_content_wrapper_table_row_key.find('div', {'class': 'c-cell cell-name'}).text for
                         table_content_wrapper_table_row_key in table_content_wrapper_table_row])

                    for table_content_wrapper_table_row_key_value in table_content_wrapper_table_row:
                        res = table_content_wrapper_table_row_key_value.findAll('div', {'class': 'c-cell'})[1:]
                        table_value.append([res_value.text.strip() for res_value in res])

            d3 = {}
            a = 0
            b = 0
            for i in range(len(table_head)):
                if table_head[i] not in d3.keys(): d3[table_head[i]] = {}
                for j in range(len(table_key[i])):
                    d3[table_head[i]][table_key[i][j]] = {}
                    for k in range(len(table_sub_key[a])):
                        d3[table_head[i]][table_key[i][j]][table_sub_key[a][k]] = table_value[b]

                        b = b + 1
                    a = a + 1
                    A = a
                    B = b
                if len(table_key[i]) == 0:
                    for l in range(len(table_sub_key[A])):
                        for m in range(len(table_value[B])):
                            d3[table_head[i]][table_sub_key[A][l]] = table_value[B]

                        B = B + 1
                    A = A + 1
        except TypeError as e:
            print(e)
        request.session['brand'] = d3
        data = {

                'compare_data': compare_res
            }
        if request.is_ajax():
            return JsonResponse(data)
        return redirect('demo')


def demo(request):
    d3 = request.session.get('brand')
    brand_name = request.session.get('brand_name')
    rating = request.session.get('rating')
    return render(request, 'prodcutSearch/demo.html', {'compare': d3, 'brand_name': brand_name, 'rating': mark_safe(json.dumps(rating))})


def filter_result(request, range_val=None):
    print(range_val)
    if request.method == 'GET':
        session = requests.Session()

        if request.GET.get('filter_value'):
            value = request.GET.get('filter_value')
            url = 'https://www.kimovil.com/en/compare-smartphones/f_max_d+inrPrice.' + value

        if request.GET.get('page'):
            page_no = request.GET.get('page')
            url = 'https://www.kimovil.com/en/compare-smartphones/f_max_d+inrPrice.' + value+','+'page.'+page_no

        myurl = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        uReq = ureq(myurl)

        uRead = uReq.read()

        uReq.close()

        soup = bs(uRead, 'lxml')

        container = soup.find('div', {'class', 'lay-wrapper'})

        phone_list = container.find('ul', {'class', 'device-results-list drl-tiles'})

        phone_list_item = phone_list.findAll('div', {'class', 'item-wrap'})

        title = []
        version = []
        status = []
        rating = []
        price = []
        data = []
        i = 0
        for item in phone_list_item:
            image_src = item.find('div', {'class': 'device-image'}).find('img')['src']
            title.append(item.find('div', {'class': 'title'}).text)
            version.append(item.find('div', {'class': 'version'}).text)
            status.append(item.find('div', {'class': 'status'}).text)
            rating.append(item.find('div', {'class': 'ki-rating'}).text)
            data.append(item.find('div', {'class': 'ki-features'}).find('div', {'class': 'data'}).text.replace('\n', ' '))
            price.append(item.find('span', {'class': 'price-buttons'}).find('span', {'class': 'xx_inr'}).text)
            media_root = 'C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/'
            local_filename = title[i].lower() + '.jpg'
            i = i + 1
            if os.path.isfile('C:/Users/Goku/PycharmProjects/mysite/media/phone_search_image/' + local_filename):
                pass
            else:
                link = 'http:'

                link = link + image_src
                r = session.get(link, stream=True, verify=False)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1220):
                        f.write(chunk)

                current_image_absolute_path = os.path.abspath(local_filename)
                shutil.move(current_image_absolute_path, media_root)
            #full_path = "/media/phone_search_image/" + local_filename

        data_dict = defaultdict(list)
        for i in range(len(title)):
            # d3[title[i]] = [version[i],status[i],rating[i],price[i]]
            data_dict[title[i]].append([version[i], status[i], rating[i], data[i], price[i]])

        if request.GET.get('page'):
            return HttpResponse(json.dumps(data_dict))
        data_dict = dict(data_dict)
        return render(request, 'prodcutSearch/under_filter.html', {'data_dict': data_dict, 'value': value})


