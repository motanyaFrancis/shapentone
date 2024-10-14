from django.contrib import admin

from dashboard.models import *


class workoutLines(admin.TabularInline):
    model = Workout
    readonly_fields = ['slug', ]
    extra = 1


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['program', 'category', 'published']
    inlines = [workoutLines]
    list_editable = ['published', ]


admin.site.register(Program, ProgramAdmin)


class CircuitLines(admin.TabularInline):
    model = Circuit
    extra = 1


class EquipmentLines(admin.TabularInline):
    model = Equipment
    extra = 1


class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['program', 'workout']
    list_filter = ['program', ]
    search_fields = ['program', 'workout']
    inlines = [EquipmentLines, CircuitLines]
    readonly_fields = ['slug', ]


admin.site.register(Workout, WorkoutAdmin)


class ExerciseLines(admin.TabularInline):
    model = Exercise
    readonly_fields = ['slug', ]
    autocomplete_fields = ['exercise']
    extra = 1


class CircuitAdmin(admin.ModelAdmin):
    list_display = ['workout', 'name']
    list_filter = ['workout', ]
    search_fields = ['workout', ]
    inlines = [ExerciseLines]


admin.site.register(Circuit, CircuitAdmin)


class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'circuit', 'duration', 'reps']
    readonly_fields = ['slug', ]
    autocomplete_fields = ['exercise']


# admin.site.register(Exercise, ExerciseAdmin)


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['workout', 'equipment']
    list_filter = ['equipment', ]
    search_fields = ['workout', 'equipment']


admin.site.register(Equipment, EquipmentAdmin)


class UserProgramAdmin(admin.ModelAdmin):
    list_display = ['user', 'program', 'active', 'custom']
    list_filter = ['active', 'custom']
    search_fields = ['user', 'program']


# admin.site.register(UserPrograms, UserProgramAdmin)
