from django.db import models


class Result(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()
    success = models.BooleanField()
    date = models.DateTimeField()

    def __unicode__(self):
        return self.date

class Feedback(models.Model):
    success = models.BooleanField()
    rating = models.IntegerField()
    text = models.CharField(max_length=140)
    result = models.ForeignKey(Result)

    def __unicode__(self):
        return self.text
