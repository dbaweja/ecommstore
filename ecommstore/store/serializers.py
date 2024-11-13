from rest_framework import serializers
from .models import Product, Category, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'products']

class OrderItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product.id')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'product_price', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'amount', 'payment_status', 'payment_id', 'items', 'total_amount']
        read_only_fields = ['order_id', 'payment_status', 'payment_id', 'total_amount']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        total_amount = 0

        # Create the order with the calculated total amount
        order = Order.objects.create(amount=total_amount)

        # Process each order item, calculate price, and add to total
        for item_data in items_data:
            product = item_data['product']['id']
            quantity = item_data['quantity']
            item_price = product.price * quantity
            total_amount += item_price

            # Create the OrderItem instance
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item_price
            )

        # Update the order's amount field
        order.amount = total_amount
        order.save()

        return order