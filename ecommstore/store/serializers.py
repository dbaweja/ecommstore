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
    product_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, coerce_to_string=True)

    class Meta:
        model = OrderItem
        fields = ['product_id', 'product_name', 'product_price', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source="orderitem_set")
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, coerce_to_string=True)

    class Meta:
        model = Order
        fields = ['order_id', 'amount', 'payment_status', 'payment_id', 'items', 'total_amount']
        read_only_fields = ['order_id', 'payment_status', 'payment_id', 'total_amount']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['amount'] = str(instance.amount)
        return data
    
    def create(self, validated_data):
        items_data = self.initial_data.get('items', [])
        total_amount = 0

        # Create the order without setting the total amount initially
        order = Order.objects.create(amount=0)

        # Process each item to create OrderItems and calculate total
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {product_id} does not exist.")

            # Calculate price based on quantity
            item_price = product.price * quantity
            total_amount += item_price

            # Create the OrderItem linked to the created order
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=item_price
            )

        # Update the order's total amount
        order.amount = total_amount
        order.save()

        return order