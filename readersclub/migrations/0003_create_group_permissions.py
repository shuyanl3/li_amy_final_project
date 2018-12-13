from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    book_permissions = permission_class.objects.filter(content_type__app_label='readersclub',
                                                             content_type__model='book')

    author_permissions = permission_class.objects.filter(content_type__app_label='readersclub',
                                                          content_type__model='author')

    review_permissions = permission_class.objects.filter(content_type__app_label='readersclub',
                                                         content_type__model='review')

    perm_view_book = permission_class.objects.filter(content_type__app_label='readersclub',
                                                           content_type__model='book',
                                                           codename='view_book')

    perm_view_author = permission_class.objects.filter(content_type__app_label='readersclub',
                                                        content_type__model='author',
                                                        codename='view_author')

    perm_view_review = permission_class.objects.filter(content_type__app_label='readersclub',
                                                               content_type__model='review',
                                                               codename='view_review')

    rc_user_permissions = chain(perm_view_book,
                                perm_view_author,
                                review_permissions)

    rc_editor_permissions = chain(book_permissions,
                                  author_permissions,
                                  review_permissions)

    my_groups_initialization_list = [
        {
            "name": "rc_user",
            "permissions_list": rc_user_permissions,
        },
        {
            "name": "rc_editor",
            "permissions_list": rc_editor_permissions,
        },
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    Group = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = Group.objects.get(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    Group = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = Group.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('readersclub', '0002_create_groups'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]
