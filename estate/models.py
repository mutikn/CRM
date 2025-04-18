from django.db import models

STATUS_CHOICES = [
    ('ongoing', 'Ongoing'),
    ('completed', 'Completed'),
    ('pending', 'Pending'),
    ('cancelled', 'Cancelled'),
]

CONDITION_CHOICES = [
    ('good', 'Good'),
    ('bad', 'Bad'),
    ('average', 'Average'),
    ('excellent', 'Excellent'),
    ('unknown', 'Unknown'),
]

OFFER_TYPE_CHOICES = [
    ('room', 'Room'),
    ('sale', 'Sale'),
    ('office', 'Office'),
    ('apartment', 'Apartment'),
    ('garage', 'Garage'),
    ('land', 'Land'),
    ('villa', 'Villa'),
    ('warehouse', 'Warehouse'),
    ('local', 'Local'),
    ('other', 'Other'),
]

class Client(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    nationality = models.CharField(max_length=50)
    comment = models.TextField(blank=True)
    passport_serial = models.CharField(max_length=50, )
    passport_expiry_date = models.DateField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    contract_file = models.FileField(upload_to='contracts/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client"
        verbose_name_plural = "Clients"




class Offer(models.Model):
    host_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    address_text = models.CharField(max_length=200, blank=True, null=True)
    ulica = models.CharField(max_length=200, blank=True, null=True)
    numer_budynku = models.CharField(max_length=20, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=10, blank=True, null=True)
    dzielnica = models.CharField(max_length=200, blank=True, null=True)
    województwo = models.CharField(max_length=200, blank=True, null=True)
    powiat = models.CharField(max_length=200, blank=True, null=True)
    gmina = models.CharField(max_length=200, blank=True, null=True)
    miejscowość = models.CharField(max_length=200, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    active = models.BooleanField(default=True)
    rooms = models.PositiveIntegerField(default=1)
    deposit_price = models.FloatField(blank=True, null=True)
    deposit_duration = models.FloatField(blank=True, null=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default='other')
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='unknown')
    clients = models.ManyToManyField(Client, through='ClientOffer', related_name="offers", blank=True)

    def __str__(self):
        return f"Offer by {self.host_name}"



    class Meta:
        ordering = ['-active', '-price']
        verbose_name = "Offer"
        verbose_name_plural = "Offers"

class ClientOffer(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="client_offers")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="client_offers")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.client.name} - {self.offer.host_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Offer"
        verbose_name_plural = "Client Offers"



import os
import uuid
def rename_offer_image(instance, filename):

    ext = filename.split('.')[-1]
    short_uuid = str(uuid.uuid4())[:8]
    new_filename = f"{instance.offer.host_name}_room_count-{instance.offer.rooms}_{short_uuid}.{ext}"
    return os.path.join('images/', new_filename)

class OfferImage(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=rename_offer_image)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.offer.host_name}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Offer Image"
        verbose_name_plural = "Offer Images"

class ClientOfferComment(models.Model):
    offer = models.ForeignKey(ClientOffer, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.offer.offer.host_name}"



    class Meta:
        ordering = ['-created_at']
        verbose_name = "Client Offer Comment"
        verbose_name_plural = "Client Offer Comments"

class ClientComment(models.Model):
    offer = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.offer.name}"


    class Meta: 
        ordering = ['-created_at']
        verbose_name = "Client Comment"
        verbose_name_plural = "Client Comments"

class DefaultContract(models.Model):
    name = models.CharField(max_length=200, help_text="Enter a name for the contract")
    file = models.FileField(upload_to='default_contracts/', help_text="Upload a PDF file")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Default Contract"
        verbose_name_plural = "Default Contracts"