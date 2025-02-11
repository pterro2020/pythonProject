from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Feedbacks(models.Model):  # отзывы
    name = models.CharField('Имя пользователя', max_length=20)
    rating = models.IntegerField()
    text = models.TextField('Отзыв', max_length=2500)
    date = models.DateField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.rating}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

class FAQ(models.Model):
    question = models.CharField('Вопрос', max_length=100)
    answer = models.CharField('Ответ', max_length=500)
    date = models.DateField('Дата добавления')

    def str(self):
        return self.question

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'

class About(models.Model):
    aboutimg = models.ImageField('Картинка', upload_to='static', default=True)
    ustext = models.CharField('МЫ', max_length=100)
    def str(self):
        return self.ustext


class News(models.Model):
    newscrat = models.CharField('Краткая', max_length=100)
    news = models.CharField('Полная', max_length=300)
    newsimg = models.ImageField('Картинка', upload_to='static')
    def str(self):
        return self.newscrat


class Contacts(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default=True)
    name= models.CharField('Имя', max_length=100)
    mail = models.CharField('Почта', max_length=300)
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Номер телефона"
            )
        ],
        blank=True
    )
    def str(self):
        return self.name




class Vac(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default=True)
    vac = models.CharField('Название', max_length=100)
    vacopis = models.CharField('Полное описание', max_length=300)
    def str(self):
        return self.vac

class Sales(models.Model):
    sales = models.CharField('Название', max_length=100)
    saleopis = models.CharField('Полное описание', max_length=300)
    def str(self):
        return self.sales


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Имя пользователя', max_length=20)
    phone_number = models.CharField('Номер телефона', max_length=15, validators=[RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )], blank=True)
    city = models.CharField('Город', max_length=20)
    adress = models.CharField('Адрес', max_length=100)
    email = models.EmailField('Почта')
    age = models.PositiveIntegerField('Возраст')

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.age is not None and self.age < 18:
            raise ValidationError('Возраст должен быть 18 или больше.')


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField('Имя пользователя', max_length=20)
    companyname = models.CharField('Название компании', max_length=20)
    def __str__(self):
        return self.name


class CarMark(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default=True)
    mark=models.CharField('Вид', max_length=10)
    def __str__(self):
        return self.mark

class Car(models.Model):
    contactimg = models.ImageField('Картинка', upload_to='static', default=True)
    mark=models.ForeignKey(CarMark, related_name='vid', on_delete=models.CASCADE)
    price = models.IntegerField('Цена', max_length=10)
    model=models.CharField('Модель машины', max_length=10)
    def __str__(self):
        return self.model

class Sales(models.Model):
    work = models.BooleanField('Действует или в нет (в архиве)?', default=True)
    name = models.CharField('Промокод', max_length=30)
    about = models.IntegerField('Сколько (в рублях)')

class Shtraf (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    cost = models.IntegerField('Сумма штрафа')

class OrderItem(models.Model):
    count=models.IntegerField('Время')
    object=models.ForeignKey(Car, on_delete=models.CASCADE)


class Order(models.Model):
    user=models.OneToOneField(User, related_name='orders',on_delete=models.CASCADE)
    date=models.DateField('Дата заказа', auto_now_add=True)
    cars=models.ManyToManyField(OrderItem, blank=True)



