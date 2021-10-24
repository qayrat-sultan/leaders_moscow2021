from django.db import models


class FileModel(models.Model):
    file = models.FileField()
    returned_file = models.FileField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file}"

