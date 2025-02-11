from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from .models import Feedbacks, FAQ, About, News, Contacts, Vac, Sales, Seller, Customer, Car, OrderItem, Order, Shtraf
import requests
from django.shortcuts import render
from django.utils import timezone
from .forms import RegisterUserForm, LoginUserForm, FeedbackForm, SellerForm, CustomerForm, CarForm, AddSpeciesForm, \
    FilterForm, SearchForm, UpdateOrderItemForm
from django.conf import settings
import matplotlib.pyplot as plt
import mpld3
import numpy as np
from collections import Counter
from statistics import mean, median, mode
import base64
from io import BytesIO


import logging


logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='a',
                    format='%(asctime)s, %(levelname)s, %(message)s')


# Create your views here.
def about(request):
    abouts = About.objects.all()
    if abouts.exists():
        for about in abouts:
            logging.info(f'company_info: {about.ustext}')
    else:
        logging.warning('не найдено')
    return render(request, 'about.html', {'abouts': abouts})


def contacts(request):
    contacts = Contacts.objects.all()
    if contacts.exists():
        for contact in contacts:
            logging.info(f'contact_info: {contact.name}')
    else:
        logging.warning('Контакты не найдены')
    return render(request, 'contacts.html', {'contacts': contacts})


def feedback(request):
    feedbacks = Feedbacks.objects.all()
    if feedbacks.exists():
        for feedback in feedbacks:
            logging.info(f'feedback_info: {feedback.name}')
    else:
        logging.warning('Отзывы не найдены')
    return render(request, 'feedback.html', {'feedbacks': feedbacks})





def news(request):
    news_items = News.objects.all()
    if news_items.exists():
        for news in news_items:
            logging.info(f'news_info: {news.newscrat}')
    else:
        logging.warning('Новости не найдены')
    return render(request, 'news.html', {'news': news_items})


def sales(request):
    sales_items = Sales.objects.all()
    if sales_items.exists():
        for sale in sales_items:
            logging.info(f'sale_info: {sale.name}')
    else:
        logging.warning('Скидки не найдены')
    return render(request, 'sales.html', {'sales': sales_items})


def shtraf(request):
    return render(request, 'shtraf.html')


def slovar(request):
    faqs = FAQ.objects.all()
    if faqs.exists():
        for faq in faqs:
            logging.info(f'faq_info: {faq.question}')
    else:
        logging.warning('FAQ не найдено')
    return render(request, 'slovar.html', {'faqs': faqs})


def vac(request):
    vacs = Vac.objects.all()
    if vacs.exists():
        for vac in vacs:
            logging.info(f'vac_info: {vac.vac}')
    else:
        logging.warning('Вакансии не найдены')
    return render(request, 'vac.html', {'vacs': vacs})

class BaseViewContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['title'] = kwargs.get('title', 'Default Title')
        return context


def reversex_lazy(param):
    pass


class RegisterView(BaseViewContextMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reversex_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(BaseViewContextMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')  # Перенаправление на главную страницу после выхода


@login_required
def add_feedback(request):
    error = ''
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            feedback.name = request.user.username  # Используем имя пользователя текущего пользователя
            feedback.save()
            return redirect('feedback')  # Перенаправляем на список отзывов после успешного добавления
        else:
            error = 'Неверное заполнение'
    else:
        form = FeedbackForm()
    data = {'error': error, 'form': form}
    return render(request, 'add_feedback.html', data)

def faq(request):
    faq = FAQ.objects.all()
    return render(request, 'slovar.html', {'faq': faq})


import matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO
from django.shortcuts import render

def foradmin(request):
    # Генерация графиков
    graph_sales = generate_sales_graph()
    graph_age = generate_age_graph()
    graph_popularity = generate_popularity_graph()

    return render(request, 'ProcatCar/foradmin.html', {
        'graph_sales': graph_sales,
        'graph_age': graph_age,
        'graph_popularity': graph_popularity
    })

def generate_sales_graph():
    # Рандомные данные для графика продаж по категориям
    categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
    sales = np.random.randint(100, 1000, size=len(categories))

    plt.figure(figsize=(8, 6))
    plt.bar(categories, sales, color='skyblue')
    plt.xlabel('Categories')
    plt.ylabel('Sales')
    plt.title('Sales by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Кодирование графика в строку base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64

def generate_age_graph():
    # Рандомные данные для графика возраста клиентов
    ages = np.random.randint(18, 70, size=100)

    plt.figure(figsize=(8, 6))
    plt.hist(ages, bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.title('Age Distribution of Customers')
    plt.tight_layout()

    # Кодирование графика в строку base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64

def generate_popularity_graph():
    # Рандомные данные для графика популярности товаров
    products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
    popularity = np.random.randint(50, 500, size=len(products))

    plt.figure(figsize=(8, 6))
    plt.bar(products, popularity, color='skyblue')
    plt.xlabel('Products')
    plt.ylabel('Popularity')
    plt.title('Popularity of Products')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Кодирование графика в строку base64
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()

    return image_base64




def customer(request):
    error = ''
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            cust = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Создаем пользователя с полученными данными
            user = User.objects.create_user(username=username, password=password)
            cust.user = user  # Используем имя пользователя текущего пользователя
            cust.save()
            return redirect('index')  # Перенаправляем на список отзывов после успешного добавления
        else:
            error = 'Введите верное значение'
            # Можно также добавить дополнительную обработку ошибок валидации, если нужно
    else:
        form = CustomerForm()
    data = {'error': error, 'form': form}
    return render(request, 'custom.html', data)


def seller(request):
    error = ''
    if request.method == "POST":
        form = SellerForm(request.POST)
        if form.is_valid():
            sell = form.save(commit=False)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Создаем пользователя с полученными данными
            user = User.objects.create_user(username=username, password=password)
            sell.user = user  # Используем имя пользователя текущего пользователя
            sell.save()
            return redirect('index')  # Перенаправляем на список отзывов после успешного добавления
        else:
            error = 'Неверное заполнение'
    form = SellerForm()
    data = {'error': error, 'form': form}
    return render(request, 'sell.html', data)


def get_joke_of_the_day():
    try:
        request = requests.get('https://icanhazdadjoke.com', headers={'Accept': 'application/json'})
        request.raise_for_status()
        response = request.json()
        return response.get('joke', 'No joke available today.')
    except requests.RequestException:
        return 'No joke available today.'

def get_car_fact():
    try:
        fact_url = "https://api.aakhilv.me/fun/facts"
        response = requests.get(fact_url)
        response.raise_for_status()
        facts = response.json()
        return facts[0] if facts else "No car fact available today."
    except requests.RequestException:
        return "No car fact available today."

def index(request):
    now = timezone.now()

    # Get cat fact
    try:
        cat_fact_url = "https://catfact.ninja/fact"
        cat_fact_response = requests.get(cat_fact_url)
        cat_fact_response.raise_for_status()
        cat_fact_data = cat_fact_response.json()
        cat_fact = cat_fact_data.get("fact", "No cat fact available today.")
    except requests.RequestException:
        cat_fact = "No cat fact available today."

    # Get cat image
    cat_image_url = "https://cataas.com/cat"

    # Get the latest news
    latest_news = News.objects.order_by('-id').first()

    return render(request, "index.html", context={
        'fact': cat_fact,
        'joke': get_joke_of_the_day(),
        'now': now,
        'car_fact': get_car_fact(),
        'cat_image_url': cat_image_url,
        'latest_news': latest_news
    })





class viewnew(DetailView):
    model = News
    template_name = 'onenew.html'
    context_object_name = 'onenew'  # передаем объект по названию context object name-a - onenew

def car(request):
    car= Car.objects.all
    return render(request, 'car.html', {'car': car})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.company = seller  # Убедитесь, что `seller` определен и имеет правильное значение
            car.save()
            return redirect('index') 
    else:
        form = CarForm()
    return render(request, 'add_car.html', {'form': form})


@login_required
def add_to_bron(request, car_id):
    try:
        customer = Customer.objects.get(user=request.user)
    except Customer.DoesNotExist:
        return redirect('index')
    
    car = Car.objects.get(pk=car_id)
    
    if request.method == 'POST':
        count_str = request.POST.get('count')
        if not count_str:
            return render(request, 'add_to_bron.html', {'error': 'Количество не указано'})  # Error message if count is missing
        
        try:
            count = int(count_str)
        except ValueError:
            return render(request, 'add_to_bron.html', {'error': 'Неверное количество'})  # Error message if count is invalid
        
        order_item, created = OrderItem.objects.update_or_create(object=car, defaults={'count': count})
        order, _ = Order.objects.update_or_create(user=request.user)
        order.cars.add(order_item)
        return redirect('car')  # Redirect to the car detail page
    
    return render(request, 'add_to_bron.html')

@login_required
def add_mark(request):
    if request.method == 'POST':
        form = AddSpeciesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddSpeciesForm()
    return render(request, 'add_mark.html', {'form': form})

def foradmin(request):
    customers_by_city = Customer.objects.values('city')
    mebel_with_highest_demand = Car.objects.annotate(total_sales=Sum('price')).order_by('-total_sales').first()
    return render(request, 'foradmin.html', {'_with_highest_demand': mebel_with_highest_demand,'customers_by_city':customers_by_city})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by()
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_cost(request):
    orders = Order.objects.filter(user=request.user).order_by()
    return render(request, 'order_cost.html', {'orders': orders})

@login_required
def orders_view(request):
    user = request.user
    orders = Order.objects.filter(user=user)

    # Получаем активный промокод
    try:
        active_discount = Sales.objects.get(work=True).about
    except Sales.DoesNotExist:
        active_discount = 0

    # Обработка заказов
    for order in orders:
        for car in order.cars.all():
            base_price = car.object.price * car.day
            try:
                fine = Shtraf.objects.get(user=user, car=car.object).cost
            except Shtraf.DoesNotExist:
                fine = 0

            car.total_price = base_price + fine - active_discount

    return render(request, "orders.html", context={'orders': orders, 'active_discount': active_discount})


def calculate_total_price(car_item):
    # Initial price of the car
    total_price = car_item.object.price

    # Check if there's any fine associated with the car
    try:
        fine = Shtraf.objects.get(car=car_item.object)
        total_price += fine.cost
    except Shtraf.DoesNotExist:
        pass

    # Check if there's any active sales or promo code
    try:
        sales = Sales.objects.get(name='promo_code', work=True)
        total_price -= sales.about  # Subtract promo code amount from total price
    except Sales.DoesNotExist:
        pass

    return total_price    


def user_fines(request):
    user = request.user  # Assuming user is authenticated
    fines = Shtraf.objects.filter(user=user)
    return render(request, 'shtraf_list.html', {'fines': fines})

def filter_cars(request):
    form = FilterForm()
    results = []

    if 'mark' in request.GET:
        form = FilterForm(request.GET)
        if form.is_valid():
            selected_mark = form.cleaned_data['mark']
            if selected_mark:
                results = Car.objects.filter(mark=selected_mark)

    return render(request, 'filter.html', {'form': form, 'results': results})

def search_view(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Car.objects.filter(model__icontains=query)

    return render(request, 'search.html', {'form': form, 'query': query, 'results': results})

def update_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    if request.method == 'POST':
        form = UpdateOrderItemForm(request.POST, instance=order_item)
        if form.is_valid():
            form.save()
            return redirect('order_list')  # Adjust the redirect to your cart view
    else:
        form = UpdateOrderItemForm(instance=order_item)
    return render(request, 'update_order_item.html', {'form': form, 'order_item': order_item})

def delete_order_item(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id)
    order_item.delete()
    return redirect('order_list')  # Adjust the redirect to your cart view