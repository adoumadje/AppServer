from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language


# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)
# admin.site.register(User, UserAdmin)


# Create user and save to the database
# user = User.objects.create_user('caleb', 'caleb@example.com', 'password')

# Update fields and then save again
# user.first_name = 'Caleb'
# user.last_name = 'Adoumadje'
# user.save()


# Define the admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

    fieldsets = (
        ('General Information', {
            'fields': ('first_name', 'last_name')
        }),
        ('Dates', {
            'fields': ('date_of_birth', 'date_of_death')
        }),
    )

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

# Register the Admin classes for Book using the decorator
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_genre')

    inlines = [BooksInstanceInline]


# Register the Admin classes for BookInstance using the decorator
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )