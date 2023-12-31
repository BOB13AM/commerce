# Generated by Django 4.1.4 on 2023-01-24 03:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('category', models.CharField(blank=True, max_length=64, null=True)),
                ('image', models.URLField(blank=True, null=True)),
                ('bid', models.DecimalField(decimal_places=2, max_digits=1000000000000)),
                ('closedbid', models.CharField(blank=True, max_length=24, null=True)),
                ('currentbid', models.DecimalField(blank=True, decimal_places=2, max_digits=1000000000000, null=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
                ('winninguser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemwin', to=settings.AUTH_USER_MODEL)),
                ('wishlist', models.ManyToManyField(blank=True, related_name='wishlistings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='invalidbid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invalid_biding', models.DecimalField(decimal_places=2, max_digits=1000000000000)),
                ('closed', models.CharField(blank=True, max_length=24, null=True)),
                ('invalid_itembid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invaliditembids', to='auctions.listing')),
                ('invalid_userbid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invaliduserbids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(blank=True, max_length=255, null=True)),
                ('reply', models.CharField(blank=True, max_length=255, null=True)),
                ('itemcomment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemcomments', to='auctions.listing')),
                ('usercomment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usercomments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='commentreply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.CharField(max_length=255)),
                ('old_reply', models.CharField(blank=True, max_length=255, null=True)),
                ('maincomment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commentmain', to='auctions.comments')),
                ('old_replying_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rtor', to=settings.AUTH_USER_MODEL)),
                ('replying_user_main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userreply', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biding', models.DecimalField(decimal_places=2, max_digits=1000000000000)),
                ('closed', models.CharField(blank=True, max_length=24, null=True)),
                ('itembid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itembids', to='auctions.listing')),
                ('userbid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userbids', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
