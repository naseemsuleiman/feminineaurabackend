from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, display_name=instance.username)


class BudgetSetup(models.Model):
    """One budget setup per user per month."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    month = models.CharField(max_length=7, help_text="Format: YYYY-MM")

    # Optional context — helps with progress display
    monthly_income = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        help_text="Optional. Used only for % context."
    )

    # The locked savings commitment
    savings_goal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'month')

    @property
    def savings_pct(self):
        if not self.monthly_income:
            return None
        return round(float(self.savings_goal) / float(self.monthly_income) * 100, 2)

    def __str__(self):
        return f"{self.user.username} - {self.month}"


class DailyEntry(models.Model):
    budget = models.ForeignKey(BudgetSetup, on_delete=models.CASCADE, related_name='entries')
    day = models.PositiveIntegerField()  # 1-30
    date = models.DateField(null=True, blank=True)
    essentials = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    wants = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('budget', 'day')
        ordering = ['day']

    @property
    def daily_total(self):
        return self.essentials + self.wants

    def __str__(self):
        return f"Day {self.day} - {self.budget}"


class Article(models.Model):
    CATEGORY_CHOICES = [
        ('mental', 'Mental Aura'),
        ('physical', 'Physical Aura'),
        ('financial', 'Financial Aura'),
        ('wisdom', 'Daily Wisdom'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    cover_image = models.ImageField(upload_to='articles/', null=True, blank=True)
    published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class DailyQuote(models.Model):
    text = models.CharField(max_length=300)
    author = models.CharField(max_length=100, blank=True, default='Feminine Aura')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:60]