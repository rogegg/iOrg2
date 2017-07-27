
from django.db import models
from django.contrib.auth.models import  User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    count_questions_ok = models.IntegerField(default=0)
    count_questions_fail = models.IntegerField(default=0)
    count_exams_pass = models.IntegerField(default=0)
    count_exams_fail = models.IntegerField(default=0)
    exam_pass_total_score = models.DecimalField(default=0, max_digits=6 , decimal_places=3)
    exam_fail_total_score = models.DecimalField(default=0, max_digits=6, decimal_places=3)

    @receiver(post_save, sender=User)
    def create_user_stats(sender, instance, created, **kwargs):
        if created:
            Stats.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_stats(sender, instance, **kwargs):
        instance.stats.save()

    def add_exam(self,score):
        if(score > 5):
            self.exam_pass_total_score += score
            self.count_exams_pass += 1
            self.save()
        else:
            self.exam_fail_total_score += score
            self.count_exams_fail += 1
            self.save()

