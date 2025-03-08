from django.db import models
from datetime import timedelta,timezone
from django.contrib.auth.models import User

class PollManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def created_within_last_week(self):
        one_week_ago = timezone.now() - timedelta(days=7)
        return self.filter(created_at__gte=one_week_ago)
    
class VoteManager(models.Manager):
    def for_poll(self, poll):
        return self.filter(poll=poll)

    
class Poll(models.Model):
    question_text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text


class Vote(models.Model):
    poll = models.ForeignKey(Poll, related_name="votes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote for {self.poll.question_text} from {self.user}"
