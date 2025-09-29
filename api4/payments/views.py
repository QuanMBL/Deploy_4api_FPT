from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    
    def get_queryset(self):
        return Payment.objects.all()
    
    def list(self, request):
        """Get all payments"""
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response({
            'message': 'Payments retrieved successfully',
            'data': serializer.data
        })
    
    def create(self, request):
        """Create a new payment"""
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Payment created successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
