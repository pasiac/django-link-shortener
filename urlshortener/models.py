from hashlib import md5

from django.db import models


class Link(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    full_path = models.URLField(unique=True)
    short_path = models.CharField(max_length=16, unique=True)

    class Meta:
        ordering = ("created",)

    def save(self, *args, **kwargs):
        if not self.id:
            self.short_path = md5(self.full_path.encode()).hexdigest()[:16]
        return super(Link, self).save(*args, **kwargs)

    def __str__(self):
        return f"Full path: {self.full_path} short path: {self.short_path}"
