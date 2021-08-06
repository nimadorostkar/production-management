from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from extensions.utils import jalali_converter
from mptt.models import MPTTModel, TreeForeignKey





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
class Tag(models.Model):
    name = models.CharField(max_length=300,verbose_name = " نام ")

    class Meta:
        verbose_name = "تگ"
        verbose_name_plural = "تگ ها"

    def __str__(self):
        return self.name




#------------------------------------------------------------------------------
class Product(models.Model):
    name = models.CharField(max_length=300,verbose_name = " نام ")
    synch_to = models.ForeignKey('Material', on_delete=models.CASCADE,verbose_name = " قطعه مربوطه ")
    file = models.FileField(default='media/Default.png', null=True, blank=True,verbose_name ="فایل")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,verbose_name = " تگ ها ")


    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('app:products_detail',args=[self.id])

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.synch_to.image.url))

    @property
    def short_description(self):
        return truncatechars(self.synch_to.description, 70)

    def code(self):
        return self.synch_to.code




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
class Material(models.Model):
    name = models.CharField(max_length=300,null=True, blank=True,verbose_name = " نام ")
    code = models.CharField(max_length=50,null=True, blank=True,verbose_name = "کد ")
    CHOICES = ( ('محصول نهایی','محصول نهایی'), ('نیمه ساخته','نیمه ساخته'), ('سطح اولیه','سطح اولیه'), ('اقلام مصرفی','اقلام مصرفی'))
    position=models.CharField(max_length=15,choices=CHOICES,verbose_name = "وضعیت")
    description = models.TextField(max_length=900,null=True, blank=True,verbose_name = "توضیحات")
    inventory = models.DecimalField(max_digits=30, decimal_places=4, null=True, blank=True, verbose_name = " موجودی ")
    min_inventory = models.DecimalField(max_digits=30, decimal_places=1, null=True, blank=True, verbose_name = " حداقل موجودی ")
    Unit_CHOICES = (('گرم','گرم'), ('عدد','عدد'), ('سانتیمتر','سانتیمتر'))
    unit = models.CharField(max_length=300,null=True, blank=True, choices=Unit_CHOICES, verbose_name = " واحد ")
    image = models.ImageField(upload_to='media', default='media/Default.png', null=True, blank=True,verbose_name = "تصویر")

    class Meta:
        verbose_name = " قطعه "
        verbose_name_plural = " قطعات "

    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html("<img width=50 src='{}'>".format(self.image.url))

    def get_absolute_url(self):
        return reverse('app:materials_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.description, 70)





#------------------------------------------------------------------------------
# MPTT Model -->  https://django-mptt.readthedocs.io/en/latest/index.html
class Bom_material(MPTTModel):
    name = models.ForeignKey(Material, on_delete=models.CASCADE, related_name = "mat_name", verbose_name = " نام قطعه ")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',verbose_name = "والد")
    quantity = models.DecimalField(max_digits=30, decimal_places=4,default='1',verbose_name = " تعداد ")
    relatedProduct=models.ForeignKey(Material, on_delete=models.CASCADE,verbose_name = " قطعه مربوطه ")


    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by = ['name']

    class Meta:
        verbose_name = " BOM قطعه "
        verbose_name_plural = " BOM قطعه ها "

    def __unicode__(self):
        return u"%s" % (self.name)

    def __str__(self):
        return str(self.name)





#------------------------------------------------------------------------------
class Stations_inputs(models.Model):
    material = models.ForeignKey(Material ,on_delete=models.CASCADE, verbose_name = " قطعه ")
    inventory = models.DecimalField(max_digits=30, decimal_places=4, verbose_name = " تعداد ")

    class Meta:
        verbose_name = " ورودی ایستگاه "
        verbose_name_plural = " ورودی ایستگاه ها "

    def __str__(self):
        return str(self.material.name) + " [" + str(self.inventory) + "]"

    def name(self):
        return str(self.material.name) + " [" + str(self.inventory) + "]"




#------------------------------------------------------------------------------
class Bom_product(models.Model):
    material = models.ForeignKey(Material ,on_delete=models.CASCADE, verbose_name = " قطعه ")
    inventory = models.DecimalField(default='1',max_digits=30, decimal_places=4, verbose_name = " تعداد ")
    relatedProduct=models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = "محصول مرتبط")

    class Meta:
        verbose_name = " BOM محصول "
        verbose_name_plural = " BOM محصولات "

    def __str__(self):
        return str(self.material) + " [" + str(self.inventory) + "]"




#------------------------------------------------------------------------------
class Station(models.Model):
    name = models.CharField(max_length=300,verbose_name = " نام ")
    code = models.CharField(max_length=50,null=True, blank=True,verbose_name = "کد ")
    CHOICES = ( ('نیرو خانگی','نیرو خانگی'), ('انبار','انبار'), ('حمل و نقل','حمل و نقل'), ('ایستگاه','ایستگاه'), ('برون سپاری','برون سپاری'))
    position=models.CharField(max_length=15,choices=CHOICES,verbose_name = "وضعیت")
    description = models.TextField(max_length=900,null=True, blank=True,verbose_name = "توضیحات")
    inventory = models.DecimalField(max_digits=30, default='0', decimal_places=4, null=True, blank=True, verbose_name = " موجودی ")
    min_inventory = models.DecimalField(max_digits=30, default='0', decimal_places=4, null=True, blank=True, verbose_name = " حداقل موجودی ")
    manager = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True,verbose_name = "مسئول")
    mother_station = models.ForeignKey(Mother_Station ,on_delete=models.CASCADE ,null=True, blank=True,verbose_name = " ایستگاه مادر ")
    pro_cap_day = models.IntegerField(default='1', null=True,blank=True, verbose_name = " ظرفیت تولید در روز ")
    percent_error = models.DecimalField(max_digits=30, default='0', decimal_places=4, null=True,blank=True, verbose_name = " درصد خطا ")
    process_time = models.DecimalField(max_digits=30, decimal_places=4, null=True, blank=True, verbose_name = " زمان مصرفی به ساعت (برای حمل و نقل و انبار) ")
    input_material = models.ManyToManyField(Stations_inputs, blank=True,related_name='input', verbose_name = " قطعات ورودی ")
    output_material = models.ForeignKey(Material ,on_delete=models.CASCADE ,null=True, blank=True,related_name='output', verbose_name = " قطعه خروجی ")


    class Meta:
        verbose_name = " ایستگاه "
        verbose_name_plural = " ایستگاه ها "

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app:stations_detail',args=[self.id])

    @property
    def short_description(self):
        return truncatechars(self.description, 70)




#------------------------------------------------------------------------------
class Tree(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='station', verbose_name = " ایستگاه ")
    parent_station = models.ForeignKey(Station, on_delete=models.CASCADE, null=True, blank=True, related_name='parent_station', verbose_name = " ایستگاه والد ")
    relatedProduct=models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,verbose_name = "محصول مرتبط")


    class Meta:
        verbose_name = "درخت محصول"
        verbose_name_plural = "درخت محصولات"

    def __str__(self):
        return str(self.station)




#------------------------------------------------------------------------------
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "از طرف")
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="to" ,verbose_name = "ارسال به")
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
class Notice(models.Model):
    title = models.CharField(max_length=200,verbose_name = " عنوان ")
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




#------------------------------------------------------------------------------
class Inventory_history(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE,verbose_name = " قطعه ")
    quantity = models.IntegerField(default='1', verbose_name = " تعداد ")
    manager = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "مسئول")
    time = models.DateTimeField(auto_now_add=True, verbose_name = "زمان")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name = " ایستگاه ")
    description = models.CharField(max_length=300,verbose_name = " توضیحات ")


    class Meta:
        verbose_name = " سابقه افزایش موجودی "
        verbose_name_plural = " سابقه افزایش موجودی ها "

    def j_time(self):
        return jalali_converter(self.time)

    def __str__(self):
        return self.material.name + '-' + self.quantity + '-' + self.j_time




#------------------------------------------------------------------------------
class Station_exit_history(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE,verbose_name = " قطعه ")
    quantity = models.IntegerField(default='1', verbose_name = " تعداد ")
    manager = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name = "مسئول")
    time = models.DateTimeField(auto_now_add=True, verbose_name = "زمان")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, verbose_name = " ایستگاه ")
    order_code = models.CharField(max_length=200, null=True, blank=True, verbose_name = "کد سفارش")
    description = models.CharField(max_length=300,verbose_name = " توضیحات ")


    class Meta:
        verbose_name = " سابقه خروج قطعه "
        verbose_name_plural = "  سابقه خروج قطعه ها "

    def j_time(self):
        return jalali_converter(self.time)

    def __str__(self):
        return self.material.name



#------------------------------------------------------------------------------
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name = " محصول ")
    code = models.CharField(max_length=50,null=True, blank=True,verbose_name = "کد ")
    description = models.TextField(max_length=900,null=True, blank=True,verbose_name = "توضیحات")
    circulation = models.DecimalField(default='1',max_digits=30, decimal_places=4, verbose_name = " تیراژ ")
    confirmed = models.BooleanField(default=False, verbose_name = " تایید شده " )
    completed = models.BooleanField(default=False, verbose_name = " تکمیل شده " )
    start_time = models.DateTimeField(auto_now_add=True,verbose_name = "زمان شروع ")


    def get_absolute_url(self):
        return reverse('app:orders_detail',args=[self.id])

    class Meta:
        verbose_name = " سفارش محصول "
        verbose_name_plural = "سفارشات محصول"

    def __str__(self):
        return self.product.name + ' (' + self.code + ') '

    def image(self):
        return  self.product.synch_to.image

    def j_time(self):
        return jalali_converter(self.start_time)




#------------------------------------------------------------------------------
class Order_confirmation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name = "سفارش")
    station = models.ForeignKey(Station, on_delete=models.CASCADE,verbose_name = "ایستگاه")
    confirmed = models.BooleanField(default=False, verbose_name = " تایید شده " )

    class Meta:
        verbose_name = " تائیدیه "
        verbose_name_plural = " تأییدها "

    def __str__(self):
        return self.order.code















#-------------------------------------------------------- by Nima Dorostkar ---
