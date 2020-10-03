from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


# models for product catagory
class Catagory(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(max_length=200,
                              db_index=True),
        slug=models.SlugField(max_length=200,
                              db_index=True,
                              unique=True)
    )

    class Meta:
        verbose_name = 'catagory'
        verbose_name_plural = 'catagories'
        # ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_catagory', args=[self.slug])


# model for Product
class Product(TranslatableModel):
    catagory = models.ForeignKey(Catagory,
                                 related_name="products",
                                 on_delete=models.CASCADE)
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=models.TextField(blank=True)
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

    price = models.DecimalField(max_digits=8, decimal_places=2)
    available = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # commenting out, because django-parler doesn't support 'ordering/filter' by of a translated field
    # class Meta:
    #     ordering = ('name',)
    #     index_together = (('id', 'slug'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_details', args=[self.id, self.slug])
