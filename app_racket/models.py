from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# 1️ Bảng Brand (Hãng vợt)
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True) # Tên hãng vợt
    country = models.CharField(max_length=100, unique=False) # Quốc gia sản xuất
    image_url = models.URLField(blank=True, null=True)  # Logo hãng vợt

    def __str__(self):
        return self.name

# 2️ Bảng Racket (Thông tin vợt)
class Racket(models.Model):
    name = models.CharField(max_length=150, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    weight = models.IntegerField()  # Trọng lượng vợt (gram)
    balance_point = models.IntegerField()  # Điểm cân bằng (mm)
    stiffness = models.IntegerField()  # Độ cứng (1-10)
    release_year = models.IntegerField()  # Năm ra mắt

    def __str__(self):
        return f"{self.brand.name} {self.name}"
    
# 3 Bảng RacketScore (Điểm đánh giá vợt)
class RacketScore(models.Model):
    racket = models.OneToOneField(Racket, on_delete=models.CASCADE)
    power = models.FloatField()  # Chỉ số Power (0-100)
    speed = models.FloatField()  # Chỉ số Speed (0-100)
    control = models.FloatField()  # Chỉ số Control (0-100)
    ease_of_use = models.FloatField()  # Độ dễ chơi (0-100)
    durability = models.FloatField()  # Độ bền (0-100)
    total_score = models.FloatField()  # Tổng điểm xếp hạng

    def __str__(self):
        return f"Score for {self.racket.name}"
    
# 4 Bảng Shop (Cửa hàng)
class Shop(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField()  # Link đến cửa hàng
    image_url = models.URLField(blank=True, null=True)  # Ảnh cửa hàng

    def __str__(self):
        return self.name
    
class RacketPrice(models.Model):
    racket = models.ForeignKey(Racket, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá vợt
    last_updated = models.DateTimeField(auto_now=True)  # Thời gian cập nhật giá

    def __str__(self):
        return f"{self.racket.name} - {self.shop.name}: ${self.price}"
    
class Player(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class PlayerRacket(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    racket = models.ForeignKey(Racket, on_delete=models.CASCADE)
    year = models.IntegerField()  # Năm sử dụng vợt

    def __str__(self):
        return f"{self.player.name} - {self.racket.name} ({self.year})"
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    racket = models.ForeignKey(Racket, on_delete=models.CASCADE)
    rating = models.FloatField()  # Đánh giá (1-5 sao)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.racket.name}: {self.rating}⭐"

class Comparison(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    racket_1 = models.ForeignKey(Racket, on_delete=models.CASCADE, related_name="racket_1")
    racket_2 = models.ForeignKey(Racket, on_delete=models.CASCADE, related_name="racket_2")
    compared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} compared {self.racket_1.name} & {self.racket_2.name}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    racket = models.ForeignKey(Racket, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} added {self.racket.name} to wishlist"
    
class ClickTracking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    racket = models.ForeignKey(Racket, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} clicked {self.racket.name} on {self.shop.name}"