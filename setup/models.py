import os
from pydoc import describe
from uuid import uuid4

from django.db import models, transaction
from django.template.defaultfilters import slugify
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

from sorl.thumbnail import get_thumbnail

from setup.validators import validate_number_min

# Create your models here.
Text003 = (
    "It is not possible to assign numbers automatically. If you want the program to assign numbers "
    "automatically, please activate {} in {} {}."
)
Text004 = "You cannot assign new numbers from the number series {} on {}."
Text005 = "You cannot assign new numbers from the number series {}."


class NumberSeries(models.Model):
    describe("A Number Series Setup")
    ID = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now=True, editable=False)
    default_no = models.BooleanField(default=True)
    manual_no = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Number Series")
        verbose_name_plural = _("Number Series")

    def __str__(self) -> str:
        return self.name

    @transaction.atomic
    def get_next_no(self) -> str:
        if not self.default_no:
            raise Exception(Text003.format("Default Nos", "Setups", self.name))

        no_series_line = NumberSeriesLine.objects.filter(no_series=self)
        if not no_series_line:
            raise Exception(Text005.format(self.name))
        no_series_line = no_series_line.filter(
            starting_date__range=[self.date_created, datetime.today()]
        ).last()
        if not no_series_line:
            raise Exception(Text004.format(self.name, datetime.today()))
        return no_series_line.get_next_no()

    def sample_no(self) -> str:
        no_series_line = NumberSeriesLine.objects.filter(
            no_series=self, starting_date__range=[self.date_created, datetime.today()]
        ).last()
        if not no_series_line:
            return ""
        return no_series_line.get_sample_no()

    def last_date_used(self):
        no_series_line = NumberSeriesLine.objects.filter(
            no_series=self, starting_date__range=[self.date_created, datetime.today()]
        ).last()
        if not no_series_line:
            return ""
        return no_series_line.last_date_used

    def last_used_no(self) -> str:
        no_series_line = NumberSeriesLine.objects.filter(
            no_series=self, starting_date__range=[self.date_created, datetime.today()]
        ).last()
        if not no_series_line:
            return ""
        return no_series_line.get_last_used_no()


class NumberSeriesLine(models.Model):
    describe("A Number Series Lines")
    no_series = models.ForeignKey(NumberSeries, on_delete=models.CASCADE)
    prefix = models.CharField(max_length=50, null=True, blank=True)
    suffix = models.CharField(max_length=50, blank=True, null=True)
    starting_date = models.DateField(default=datetime.today)
    number_of_fills = models.IntegerField(
        _("Number of Fill-ins"),
        default=5,
        validators=[
            validate_number_min,
        ],
    )
    starting_no = models.IntegerField(
        _("Starting No."),
        default=1,
        validators=[
            validate_number_min,
        ],
    )
    warning_no = models.IntegerField(
        _("Warning No."),
        default=0,
        validators=[
            validate_number_min,
        ],
    )
    last_no_used = models.IntegerField(
        _("Last Used Number"),
        default=0,
        validators=[
            validate_number_min,
        ],
    )
    allow_gaps_in_nos = models.BooleanField(_("Allow Gaps In Nos."))
    increment_by = models.IntegerField(
        verbose_name=_("Increment By"),
        validators=[
            validate_number_min,
        ],
        default=1,
    )
    date_created = models.DateTimeField(auto_now=True, editable=False)
    last_date_used = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = _("Number Series Line")
        verbose_name_plural = _("Number Series Lines")
        ordering = ("-starting_date",)

    def __str__(self) -> str:
        return f"{self.no_series.name} - {self.get_sample_no()}"

    def save(self, *args, **kwargs) -> None:
        if self.prefix is not None:
            self.prefix = self.prefix.upper()
        if self.suffix is not None:
            self.suffix = self.suffix.upper()
        return super().save(args, kwargs)

    def get_next_no(self) -> str:
        if self.starting_date:
            if self.starting_date > datetime.today().date():
                raise (
                    "Cannot Use No. Series Line, Start Date is {}".format(
                        self.starting_date
                    )
                )

        if self.last_no_used == 0:
            last_used = self.starting_no
        else:
            last_used = self.last_no_used + self.increment_by

        if last_used == self.warning_no and self.warning_no != 0:
            # Send A notification that the number has reached the level for warning
            pass

        self.last_no_used = last_used
        self.save()
        return self.format_no(last_used, self.prefix, self.number_of_fills, self.suffix)

    def get_sample_no(self) -> str:
        return self.format_no(1, self.prefix, self.number_of_fills, self.suffix)

    def get_last_used_no(self) -> str:
        if self.last_no_used == 0:
            return ""
        return self.format_no(
            self.last_no_used, self.prefix, self.number_of_fills, self.suffix
        )

    def format_no(self, no: int, prefix: str, fill_ins: int, suffix: str) -> str:
        if prefix is None:
            prefix = ""
        if suffix is None:
            suffix = ""
        return "{}{}{}".format(prefix, str(no).zfill(fill_ins + 1), suffix)


class Setup(models.Model):
    describe("A General Application Setup")

    ID = models.CharField(
        primary_key=True, default="setup", editable=False, max_length=5
    )
    site_name = models.CharField(max_length=250, null=True)
    front_end_domain = models.CharField(
        verbose_name=_("Front End Domain"), null=True, max_length=250
    )
    front_end_port = models.IntegerField(
        verbose_name=_("Front End Port"), null=True, blank=True
    )
    registration_allowed = models.BooleanField(
        verbose_name=_("Registration Allowed"), default=False
    )
    member_nos = models.ForeignKey(
        NumberSeries,
        verbose_name=_("Member Nos"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="member_no_series",
    )
    invoice_nos = models.ForeignKey(
        NumberSeries,
        verbose_name=_("Invoice Nos"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="invoice_no_series",
    )

    def __str__(self):
        return self.ID


class IntensitySetup(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class LevelSetup(models.Model):
    title = models.CharField(max_length=255)
    # noinspection SpellCheckingInspection
    decscription = models.TextField(verbose_name="Description", blank=True)
    # intensity = models.ForeignKey(IntensitySetup, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class CategorySetup(models.Model):
    title = models.CharField(max_length=255)
    level = models.ForeignKey(LevelSetup, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class ProgramSetup(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class WorkoutSetup(models.Model):
    title = models.CharField(max_length=255)
    description = HTMLField()
    image = models.FileField()

    def __str__(self):
        return self.title


class CircuitSetup(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class ExerciseSetup(models.Model):
    title = models.CharField(max_length=255)
    description = HTMLField()
    image = models.FileField()

    class Meta:
        ordering = ["title"]

    def thumbnail(self):
        if self.image:
            thumbnail = get_thumbnail(self.image, '150x150', crop='center')
            return thumbnail.url
        return None

    thumbnail.short_description = 'Thumbnail'
    thumbnail.allow_tags = True

    def __str__(self):
        return self.title

    def extension(self):
        title, extension = os.path.splitext(self.image.name)
        
        return extension


class EquipmentSetup(models.Model):
    title = models.CharField(max_length=255)
    image = models.FileField()

    def __str__(self):
        return self.title


# class EmailLog(models.Model):
#     describe('A Model For storing Email Logs that have been sent through the server')
#
#     from_email = models.CharField(max_length=250)
#     subject = models.CharField(max_length=250)
#     message = models.TextField()
#     html_message = models.TextField()
#     recipients = models.CharField(max_length=250)
#     cc = models.CharField(max_length=250, null=True, blank=True)
#     bcc = models.CharField(max_length=250, null=True, blank=True)
#     fail_silently = models.BooleanField()
#     success = models.BooleanField()
#     datetime = models.DateTimeField(_("Date Time"), auto_now=True)
#     user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Email Log'
#         verbose_name_plural = 'Email Logs'
#         ordering = ('-datetime',)
#
#     def __str__(self) -> str:
#         return f'{self.subject} - {self.recipients}'


class Policy(models.Model):
    title = models.CharField(max_length=500, unique=True)
    slug = models.SlugField(_("slug"), null=True, blank=True, default="")
    content = HTMLField()

    class Meta:
        verbose_name_plural = "Policies"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
