from django.db import models
from django.utils.timezone import now


def upload_to(instance, filename):
    if instance._meta.model_name == 'image':
        instance.id = instance.property.id
    return 'assets/images/{}/{}/{}'.format("products", instance.id, filename)


class City(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    population = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = u'City'
        verbose_name_plural = u'Cities'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = u'Area'
        verbose_name_plural = u'Areas'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Property(models.Model):
    objects = None

    class SaleType(models.TextChoices):
        FOR_SALE = 'Sale'
        FOR_RENT = 'Rent'

    class HomeType(models.TextChoices):
        APARTMENT = 'Apartment'
        VILLA = 'Villa',
        COMMERCIAL = 'Commercial',
        PROJECT = 'Project',
        LAND = 'Land',

    title = models.CharField(max_length=255, verbose_name="Title")
    address = models.CharField(max_length=255, verbose_name="Address", blank=True, null=True)
    city = models.ManyToManyField(City, verbose_name="City", blank=True, null=True)
    state = models.CharField(max_length=255, verbose_name="Country", blank=True, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, verbose_name="Area", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    sale_type = models.CharField(max_length=50, choices=SaleType.choices,
                                 default=SaleType.FOR_SALE, verbose_name="action")
    price = models.DecimalField(max_digits=19, decimal_places=2, default=0, verbose_name="Price")
    bedrooms = models.PositiveIntegerField(verbose_name="Number of Bedrooms", blank=True, null=True)
    bathrooms = models.PositiveIntegerField(verbose_name="Number of Bathrooms", blank=True, null=True)
    home_type = models.CharField(max_length=50, choices=HomeType.choices, verbose_name="Home Type", blank=True,
                                 null=True)
    square_fit = models.PositiveIntegerField(verbose_name="Square Feet", blank=True, null=True)
    object_id = models.CharField(max_length=25, verbose_name="Object ID", unique=True, blank=True, null=True)
    photo_main = models.ImageField(upload_to=upload_to, verbose_name="Main Photo", blank=True, null=True)
    is_published = models.BooleanField(default=False, verbose_name="Published")
    list_date = models.DateTimeField(verbose_name="Publication Date", default=now, blank=True, null=True)
    building_year = models.CharField(max_length=4, verbose_name="Year Built", blank=True, null=True)
    best_offer = models.BooleanField(default=False, verbose_name="Best Offer")
    modx_id = models.CharField(max_length=25, verbose_name="ID in MODX Database", unique=True, blank=True, null=True)

    class Meta:
        verbose_name = u'Object'
        verbose_name_plural = u'Objects'

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class Image(models.Model):
    objects = None
    title = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to=upload_to, blank=True, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, blank=True, null=True, related_name='images')

    class Meta:
        verbose_name = u'Image'
        verbose_name_plural = u'Images'

    def __unicode__(self):
        return self.image.name
