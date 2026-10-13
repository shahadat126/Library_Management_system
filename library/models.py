from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name}"
class Book(models.Model):
    title= models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE,related_name='book',null=True,blank=True)
   
    def __str__(self):
           return f"{self.title}"
        
class Reviews(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name="reviews")
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating= models.PositiveSmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
            return f"{self.book.title}"
    
        