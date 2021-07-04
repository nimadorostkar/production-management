from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
#from mapbox_location_field.models import LocationField
#from django.contrib.gis.db.models import PointField
from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid
from django.template.defaultfilters import truncatechars
from extensions.utils import jalali_converter






#------------------------------------------------------------------------------
class Supplier(models.Model):
    name=models.CharField(max_length=200,verbose_name = "نام")
    description=models.TextField(max_length=800,null=True, blank=True,verbose_name = "توضیحات")
    link = models.URLField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = "تامین کننده"
        verbose_name_plural = "تامین کنندگان"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:supplier_detail',args=[self.id])




#------------------------------------------------------------------------------
class Mother_Station(models.Model):
    name = models.CharField(max_length=400,verbose_name = "نام")
    description=models.TextField(max_length=1000,null=True, blank=True,verbose_name = "مشخصات")
    manager = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "مسئول")


    class Meta:
        verbose_name = "ایستگاه مادر"
        verbose_name_plural = " ایستگاه های مادر  "

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:mother_station_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.description, 70)





#------------------------------------------------------------------------------
class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE,unique=True,related_name='profile',verbose_name = "کاربر")
  phone = models.CharField(max_length=50,null=True, blank=True,verbose_name = " شماره تماس  ")
  address = models.CharField(max_length=3000,null=True, blank=True,verbose_name = " آدرس  ")
  user_photo = models.ImageField(upload_to='user_uploads/user_photo',default='user_uploads/user_photo/default.png',null=True, blank=True,verbose_name = "تصویر کاربر")


  @receiver(post_save, sender=User)
  def create_user_profile(sender, instance, created, **kwargs):
      if created:
          Profile.objects.create(user=instance)

  @receiver(post_save, sender=User)
  def save_user_profile(sender, instance, **kwargs):
      instance.profile.save()


  def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.user_photo.url))

  def user_name(self):
        return str(self.user)


  class Meta:
      verbose_name = "پروفایل"
      verbose_name_plural = " پروفایل ها "


  def __str__(self):
    return "پروفایل : " + str(self.user)




#------------------------------------------------------------------------------
class Process(models.Model):
    name = models.CharField(max_length=400,verbose_name = "نام")
    CHOICES = ( ('M','Material'), ('R','Repository'), ('T','Transfer'), ('S','Station'),('P','Product') )
    position=models.CharField(max_length=1,choices=CHOICES,verbose_name = "وضعیت")
    description=models.TextField(max_length=1000,null=True, blank=True,verbose_name = "مشخصات")
    inventory = models.IntegerField(null=True,blank=True, verbose_name = " موجودی ")
    min_inventory = models.IntegerField(null=True,blank=True, verbose_name = " حداقل موجودی ")
    manager = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "مسئول")
    supplier = models.ForeignKey(Supplier ,on_delete=models.CASCADE ,null=True, blank=True,verbose_name = "تامین کننده")
    mother_station = models.ForeignKey(Mother_Station ,on_delete=models.CASCADE ,null=True, blank=True,verbose_name = " ایستگاه مادر ")
    pro_cap_day = models.IntegerField(default='1', null=True,blank=True, verbose_name = " ظرفیت تولید در روز ")
    percent_error = models.IntegerField(default='1', null=True,blank=True, verbose_name = " درصد خطا ")
    #location = LocationField(null=True,blank=True)

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

    class Meta:
        verbose_name = "فرآیند"
        verbose_name_plural = " فرآیند ها "

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:processes_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.description, 70)



#------------------------------------------------------------------------------
class Product(models.Model):
    name=models.CharField(max_length=400,verbose_name = "نام")
    code=models.CharField(max_length=50,null=True, blank=True,verbose_name = "کد ")
    description=models.TextField(max_length=900,null=True, blank=True,verbose_name = "توضیحات")
    image=models.ImageField(upload_to='media', default='media/Default.png' ,null=True, blank=True,verbose_name = "تصویر")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:products_detail',args=[self.id])

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    @property
    def short_description(self):
        return truncatechars(self.description, 70)



#------------------------------------------------------------------------------
# MPTT Model -->  https://django-mptt.readthedocs.io/en/latest/index.html
class Tree(MPTTModel):
    name = models.ForeignKey(Process, on_delete=models.CASCADE,verbose_name = "نام")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name = "والد")
    relatedProduct=models.ManyToManyField(Product,verbose_name = "محصول مرتبط")
    quantity = models.IntegerField(default='1',verbose_name = "تعداد در یک محصول")

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = "درخت محصول"
        verbose_name_plural = "درخت محصولات"

    def __str__(self):
        return str(self.name)

    def position(self):
        return  self.name.position

    def station(self):
        return  self.name.name



#------------------------------------------------------------------------------
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "از طرف")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to" ,verbose_name = "ارسال به")
    #ticket_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300,null=True, blank=True,verbose_name = " عنوان ")
    descriptions = models.TextField(max_length=800,null=True, blank=True,verbose_name = "توضیحات")
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)

    def user_name(self):
        return str(self.user)

    class Meta:
        ordering = ['-created_on']

    class Meta:
        verbose_name = " تیکت"
        verbose_name_plural = " تیکت ها "

    def __str__(self):
        return str(self.created_on)

    def j_created_on(self):
        return jalali_converter(self.created_on)





#------------------------------------------------------------------------------
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = " محصول ")
    code = models.CharField(max_length=50,null=True, blank=True,verbose_name = "کد ")
    description = models.TextField(max_length=900,null=True, blank=True,verbose_name = "توضیحات")
    circulation = models.IntegerField(default='1',verbose_name = " تیراژ ")
    order_for = models.CharField(max_length=70,null=True, blank=True,verbose_name = "سفارش برای ")
    start_time = models.DateTimeField(verbose_name = "زمان شروع ")
    confirmed = models.BooleanField(default=False, verbose_name = " تایید شده " )
    completed = models.BooleanField(default=False, verbose_name = " تکمیل شده " )


    def get_absolute_url(self):
        return reverse('app:orders_detail',args=[self.id])

    class Meta:
        verbose_name = " سفارش محصول "
        verbose_name_plural = "سفارشات محصول"

    def __str__(self):
        return self.product.name + ' (' + self.code + ') '

    def image(self):
        return  self.product.image

    def j_created_on(self):
        return jalali_converter(self.start_time)




#------------------------------------------------------------------------------
class Confirmation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "سفارش")
    process = models.ForeignKey(Process, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "فرآیند")
    confirmed = models.BooleanField(default=False, verbose_name = " تایید شده " )

    class Meta:
        verbose_name = " تائیدیه "
        verbose_name_plural = " تأییدها "

    def __str__(self):
        return self.order.code




#------------------------------------------------------------------------------
class Notice(models.Model):
    title = models.CharField(max_length=200,null=True, blank=True,verbose_name = " عنوان ")
    content = models.TextField(null=True, blank=True,verbose_name = " متن ")
    updated_on = models.DateTimeField(auto_now= True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    class Meta:
        verbose_name = "اعلان"
        verbose_name_plural = " اعلانات "

    def __str__(self):
        return self.title

    def j_created_on(self):
        return jalali_converter(self.created_on)















#-------------------------------------------------------- by Nima Dorostkar ---
