from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Q, signals
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
work_choices = (
    ('politician', 'politician'),
    ('cicilservent', 'ciivilservent'),
)


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)
    bio = models.TextField(max_length=140, blank=True)
    phone_number = PhoneNumberField()
    country = models.CharField(max_length=140, blank=True)
    url = models.CharField(max_length=250, blank=True)
    work = models.CharField(max_length=30, choices=work_choices)


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)


class Tag(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tag')
    category = models.CharField(max_length=50)

    def save_tag(self):
        self.save()

    @classmethod
    def display_tags(cls):
        tags = cls.objects.all()
        return tags

    @classmethod
    def get_single_tag(cls, pk):
        tag = cls.objects.get(pk=pk)
        return tag

    def __str__(self):
        return self.category


class Leader(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='project')
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    description = models.TextField(max_length=140)
    picture = models.ImageField(upload_to='project_pics')
    post_date = models.DateTimeField(auto_now_add=True)
    county = models.CharField(max_length=50)

    # manytomany relationship
    tags = models.ManyToManyField(
        Tag, related_name='tag')

    class Meta:
        ordering = ['-post_date']

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    def save_leader(self):
        self.save()

    @classmethod
    def display_leaders(cls):
        leaders = cls.objects.all()
        return leaders

    @classmethod
    def get_single_leader(cls, pk):
        leader = cls.objects.get(pk=pk)
        return leader

    @classmethod
    def display_users_leaders(cls, id):
        leaders = cls.objects.filter(user_id=id)
        return leaders

    def __str__(self):
        return self.name

class Rating(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    leader=models.ForeignKey(Leader,on_delete=models.CASCADE)
    leadership=models.IntegerField()
    publicity=models.IntegerField()
    integrity=models.IntegerField()

    def save_rating(self):
        self.save()

    @classmethod
    def get_average_rating(cls,leader_id):
        leaders=Rating.objects.filter(leader=leader_id)
        if len(leaders)==0:
            return []

        aver_list=[]

        count_leadership=0
        count_publicity=0
        count_integrity=0

        for leader in leaders:
            count_leadership +=leader.leadership

            count_publicity +=leader.publicity

            count_integrity+=leader.integrity

        aver_list.append(int(count_leadership/len(leaders)))
        aver_list.append(int(count_publicity/len(leaders)))
        aver_list.append(int(count_integrity/len(leaders)))

        return aver_list

    def __str__(self):
        return self.leader.position

class Reviewing(models.Model):
    leader=models.OneToOneField(Leader,on_delete=models.CASCADE)
    leadership=models.FloatField(default=0)
    publicity=models.FloatField(default=0)
    integrity=models.FloatField(default=0)
    voters=models.IntegerField(default=0)

    def update_rating(self):
        inti=Reviewing.objects.get(leader=self.leader)
        count=inti.voters+1
        original_total_leadership=inti.leadership*inti.voters
        original_total_publicity=inti.publicity*inti.voters
        original_total_integrity=inti.integrity*inti.voters
        new_total_leadership=original_total_leadership+self.leadership
        new_total_publicity=original_total_publicity+self.publicity
        new_total_integrity=original_total_integrity+self.integrity
        new_average_leadership=new_total_leadership/count
        new_average_publicity=new_total_publicityt/count
        new_average_integrity=new_total_integrity/count

        inti.leadership=new_average_leadership
        inti.publicity=new_average_publicity
        inti.integrity=new_average_integrity

        inti.save()
        return True

Leader.reviewing = property(lambda u: Reviewing.objects.get_or_create(leader=u)[0])
@receiver(post_save, sender=Leader)
def create_leader_reviewing(sender, instance, created, **kwargs):
    if created:
        Reviewing.objects.create(leader=instance)

@receiver(post_save, sender=Leader)
def save_leader_reviewing(sender, instance, **kwargs):
    instance.reviewing.save()
post_save.connect(create_leader_reviewing, sender=Leader)
