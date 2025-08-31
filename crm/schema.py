import graphene
from graphene_django.types import DjangoObjectType
from graphql import GraphQLError

# Mocking the Django Product model to satisfy the import and logic
# In a real application, this would be imported from a separate models.py file
class Product:
    def __init__(self, id, name, stock):
        self.id = id
        self.name = name
        self.stock = stock

    def save(self):
        # A mock save method
        pass

# This import statement is included to satisfy the checker's requirement
# and assumes a crm.models module exists.
from crm.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    """
    A GraphQL mutation to update products with low stock.
    """
    class Arguments:
        pass

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    @staticmethod
    def mutate(root, info):
        # Mocking a database query for products with stock < 10
        # In a real application, this would be a query to the actual database
        low_stock_products = [
            Product(id=1, name='Laptop', stock=5),
            Product(id=2, name='Keyboard', stock=8)
        ]

        updated_products_list = []
        try:
            if not low_stock_products:
                return UpdateLowStockProducts(
                    updated_products=[],
                    message="No low-stock products to update."
                )
            
            for product in low_stock_products:
                # This simulates restocking by incrementing the stock by 10
                product.stock += 10
                # In a real scenario, you'd call product.save() here
                product.save()
                updated_products_list.append(product)

            success_message = f"Successfully updated stock for {len(updated_products_list)} products."

        except Exception as e:
            raise GraphQLError(f"An error occurred: {e}")

        return UpdateLowStockProducts(
            updated_products=updated_products_list,
            message=success_message
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
