from django.db import models

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField(null=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments")
    comment = models.CharField(max_length=500, null=False)

    def __str__(self):
        return self.comment
