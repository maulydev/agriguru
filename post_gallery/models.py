from django.db import models


class PostGallery(models.Model):
    post = models.ForeignKey('posts.Post', on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='post_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post Gallery for {self.post.produce.name}"