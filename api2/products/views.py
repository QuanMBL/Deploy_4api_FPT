from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.all()
    
    def list(self, request):
        """Get all products"""
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({
            'message': 'Products retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request):
        """Create a new product"""
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Product created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
