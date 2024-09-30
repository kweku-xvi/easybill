from .models import Customer
from .serializers import CustomerSerializer
from accounts.permissions import IsVerified
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
    

@api_view(['POST'])
@permission_classes([IsVerified])
def add_customer(request):
    if request.method == 'POST':
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(added_by=request.user)

            return Response(
                {
                    'success':True,
                    'message':'Customer added successfully',
                    'customer':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
                {
                    'success':False,
                    'message':serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_customer_by_id(request, id:str):
    if request.method == 'GET':
        if Customer.objects.filter(added_by=request.user, id=id).exists():
            customer = Customer.objects.get(id=id)
        else:
            return Response(
                {
                    'success':False,
                    'message':'Customer does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CustomerSerializer(customer)

        return Response(
            {
                'success':True,
                'customer':serializer.data
            }, status=status.HTTP_200_OK
        )

    
@api_view(['GET'])
@permission_classes([IsVerified])
def get_all_customers(request):
    if request.method == 'GET':
        customers = Customer.objects.filter(added_by=request.user)

        serializer = CustomerSerializer(customers, many=True)

        return Response(
            {
                'success':True,
                'customers':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_customer_info(request, id:str):
    if request.method == 'PUT' or request.method == 'PATCH':
        if Customer.objects.filter(added_by=request.user, id=id).exists():
            customer = Customer.objects.get(id=id)
        else:
            return Response(
                {
                    'success':False,
                    'message':'Customer does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CustomerSerializer(customer, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                {
                    'success':True,
                    'message':'Customer info updated successfully',
                    'customer':serializer.data
                }, status=status.HTTP_200_OK
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['DELETE'])
@permission_classes([IsVerified])
def delete_customer(request, id:str):
    if request.method == 'DELETE':
        if Customer.objects.filter(added_by=request.user, id=id).exists():
            customer = Customer.objects.get(id=id)
        else:
            return Response(
                {
                    'success':False,
                    'message':'Customer does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )

        customer.delete()

        return Response (
            {
                'success':True,
                'message':'Customer deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT
        )