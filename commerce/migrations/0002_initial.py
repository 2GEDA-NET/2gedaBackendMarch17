# Generated by Django 4.2.5 on 2023-10-26 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('commerce', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='salehistory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.product'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.product'),
        ),
        migrations.AddField(
            model_name='productreview',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productimg',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_imgs', to='commerce.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='business',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.businessaccount'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.productcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='promotion_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='commerce.promotionplan'),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.salelocation'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='commerce.order'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_orders', to='commerce.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_orders', to='commerce.deliveryaddress'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shipping_orders', to='commerce.deliveryaddress'),
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.address'),
        ),
        migrations.AddField(
            model_name='deliveryaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cartId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commerce.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='userId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
