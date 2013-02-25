from django.db import models


class Result(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()
    success = models.BooleanField()
    date = models.DateTimeField()

    def short_input(self):
        return unicode(self.input_text[:30])

    def __unicode__(self):
        return unicode(self.date)

class Feedback(models.Model):
    success = models.BooleanField()
    rating = models.IntegerField()
    text = models.CharField(max_length=140)
    result = models.ForeignKey(Result)

    def __unicode__(self):
        return unicode(self.text)
