from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _

from setup.models import *

# Create your models here.


class Program(models.Model):
    program = models.ForeignKey(ProgramSetup, on_delete=models.PROTECT)
    category = models.ForeignKey(CategorySetup, on_delete=models.PROTECT)
    published = models.BooleanField(default=False)

    class Meta:
        verbose_name = '1. Program'

    def __str__(self):
        return self.program.title


class Workout(models.Model):
    workout = models.ForeignKey(WorkoutSetup, on_delete=models.PROTECT)
    program = models.ForeignKey(Program, on_delete=models.PROTECT)
    slug = models.SlugField(_("slug"), null=True,
                            blank=True, unique=True, default='')

    class Meta:
        verbose_name = '2. Workout'

    def __str__(self):
        return self.workout.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.program.program.title + '-' + self.workout.title)
        super().save(*args, **kwargs)


class Circuit(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT)
    circuit = models.ForeignKey(CircuitSetup, on_delete=models.PROTECT)
    name = models.CharField(
        max_length=255, help_text='e.g. Circuit 1', default='')

    class Meta:
        verbose_name = '3. Circuit'

    def __str__(self):
        return self.circuit.title


class Exercise(models.Model):
    circuit = models.ForeignKey(Circuit, on_delete=models.PROTECT)
    exercise = models.ForeignKey(ExerciseSetup, on_delete=models.PROTECT)
    duration = models.IntegerField(blank=True, default=0)
    duration_descripion = models.CharField(blank=True, max_length=1000)
    reps = models.IntegerField(blank=True, default=0)
    reps_description = models.CharField(blank=True, max_length=1000)
    slug = models.SlugField(_("slug"), null=True, blank=True, default='')

    class Meta:
        verbose_name = '4. Exercise'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.circuit.circuit.title +
                                '-' + self.exercise.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.exercise.title


class Equipment(models.Model):
    equipment = models.ForeignKey(EquipmentSetup, on_delete=models.PROTECT)
    workout = models.ForeignKey(Workout, on_delete=models.PROTECT)

    def __str__(self):
        return self.equipment.title
