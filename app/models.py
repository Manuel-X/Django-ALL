from django.db import models


#import reverse function used in get_absolute_url
from django.urls import reverse


#import django User model
from django.contrib.auth.models import User


from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify


# Create your models here.

class Store(models.Model):
	CUISINES = (
		('indian','Indian'),
		('oriental', 'Oriental'),
		('italian', 'Italian'),
		('other','Other')
	)
	name = models.CharField(max_length = 30)
	location = models.CharField(max_length = 30)
	description = models.TextField()
	category = models.CharField(choices=CUISINES,max_length=30,default='other')
	# null=True allows migration with no picture to previous created objects
	# blank=True allows creating a new object with no picture
	image = models.ImageField(null = True, blank = True)  
	owner = models.ForeignKey(User, on_delete = models.CASCADE)  #one user many stores
	slug = models.SlugField(unique=True,blank=True) #blank as auto assigned
	


	#function to auto generate url for store detail page
	def get_absolute_url(self):
		return reverse('app:detail', kwargs={'store_slug':self.slug})


	#display name of store in admin page instead of its slug
	def __str__(self):
		return self.name



class Item(models.Model):
	name = models.CharField(max_length = 30)
	price = models.DecimalField(decimal_places=3,max_digits=6)
	image = models.ImageField(null = True, blank = True)  
	store = models.ForeignKey(Store,on_delete=models.CASCADE,related_name="items")  #one store many items
	slug = models.SlugField(unique=True,blank=True) #blank as auto assigned

	class Meta:
		ordering = ('name','-price')

	#display name of store in admin page instead of its id
	def __str__(self):
		return self.name

	def price_range(self):
		if self.price < 2:
			return "cheap"
		elif self.price < 5:
			return "average"
		elif self.price < 10:
			return "expensive"
		else:
			return "elite"


def create_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Store.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
            else:
                new_slug = "%s-1" % (slug)
        except:
            new_slug = "%s-1" % (slug)
        return create_slug(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Store)
def generate_slug(instance, *args, **kwargs):
    if not instance.slug:
        instance.slug=create_slug(instance)




def create_slug_2(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Item.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
            else:
                new_slug = "%s-1" % (slug)
        except:
            new_slug = "%s-1" % (slug)
        return create_slug_2(instance, new_slug=new_slug)
    return slug

@receiver(pre_save, sender=Item)   #@ is decorator of function
def generate_slug_2(instance, *args, **kwargs):  #slug should go after model
    if not instance.slug:   #assign slug only if there is no existing one
        instance.slug=create_slug_2(instance)




