from .models import Invoice, InvoiceItem
from .serializers import InvoiceSerializer, InvoiceItemSerializer
from accounts.permissions import IsVerified
from customers.models import Customer
from decimal import Decimal
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['POST'])
@permission_classes([IsVerified])
def create_invoice(request, customer_id:str):
    if request.method == 'POST':
        if Customer.objects.filter(id=customer_id).exists():
            customer = Customer.objects.get(id=customer_id)
        else:
            return Response(
                {
                    'success':True,
                    'message':'Customer does not exist'
                }, status=status.HTTP_404_NOT_FOUND
            )

        serializer = InvoiceSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(customer=customer, sender=request.user)

            return Response(
                {
                    'success':True,
                    'invoice':serializer.data
                }, status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'success':False,
                'message':serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes({IsVerified})
def add_item_to_invoice(request, invoice_id:str):
    if request.method == 'POST':
        if Invoice.objects.filter(id=invoice_id).exists():
            invoice = Invoice.objects.get(id=invoice_id)
        else:
            return Response(
                {
                    'success':False,
                    'message':'Invoice not found'
                }, status=status.HTTP_404_NOT_FOUND
            )

        serializer = InvoiceItemSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(invoice=invoice)

            invoice.sub_total += Decimal(serializer.data['unit_price']) * Decimal(serializer.data['quantity'])
            invoice.save()

            return Response(
                {
                    'success':True,
                    'item':serializer.data
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
def get_invoice_items(request, invoice_id:str):
    if request.method == 'GET':
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response(
                {
                    'success':False,
                    'message':'Invoice not found'
                }, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != invoice.sender and not request.user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You cannot perform this action.'
                }, status=status.HTTP_403_FORBIDDEN
            )

        items = InvoiceItem.objects.filter(invoice=invoice)

        serializer = InvoiceItemSerializer(items, many=True)

        return Response(
            {
                'success':True,
                'items':serializer.data
            }, status=status.HTTP_200_OK
        )


@api_view(['PUT', 'PATCH'])
@permission_classes([IsVerified])
def update_invoice_item(request, item_id:str):
    if request.method == 'PUT' or request.method == 'PATCH':
        if InvoiceItem.objects.filter(id=item_id).exists():
            item = InvoiceItem.objects.get(id=item_id)
        else:
            return Response(
                {
                    'success':False,
                    'message':'Item not found'
                }, status=status.HTTP_404_NOT_FOUND
            )
        
        if item.invoice.sender != request.user and not request.user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You cannot perform this action'
                }, status=status.HTTP_403_FORBIDDEN
            )

        serializer = InvoiceItemSerializer(item, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            invoice = item.invoice
            invoice.sub_total = sum(
                invoice_item.total_price() for invoice_item in invoice.invoiceitem_set.all()
            )
            invoice.save()


            return Response(
                {
                    'success':True,
                    'message':'Updated successful!',
                    'item':serializer.data
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
def remove_invoice_item(request, item_id:str):
    if request.method == 'DELETE':
        if InvoiceItem.objects.filter(id=item_id).exists():
            item = InvoiceItem.objects.get(id=item_id)
        else:
            return Response(
                {
                    'success':False,
                    'message':'Item not found'
                }, status=status.HTTP_404_NOT_FOUND
            )
        
        if item.invoice.sender != request.user and not request.user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You cannot perform this action'
                }, status=status.HTTP_403_FORBIDDEN
            )

        item.delete()

        invoice = item.invoice
        invoice.sub_total = sum(
            invoice_item.total_price() for invoice_item in invoice.invoiceitem_set.all()
        )
        invoice.save()

        return Response(
            {
                'success':True,
                'message':'Item deleted successfully'
            }, status=status.HTTP_201_CREATED
        )


@api_view(['GET'])
@permission_classes([IsVerified])
def get_invoices_by_user(request):
    if request.method == 'GET':
        invoices = Invoice.objects.filter(sender=request.user)

        serializer = InvoiceSerializer(invoices, many=True)

        return Response(
            {
                'success':True,
                'items':serializer.data
            }, status=status.HTTP_200_OK
        )



@api_view(['DELETE'])
@permission_classes({IsVerified})
def delete_invoice(request, invoice_id:str):
    if request.method == 'DELETE':
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response(
                {
                    'success':False,
                    'message':'Invoice not found'
                }, status=status.HTTP_404_NOT_FOUND
            )

        if request.user != invoice.sender and not request.user.is_staff:
            return Response(
                {
                    'success':False,
                    'message':'You cannot perform this action'
                }, status=status.HTTP_403_FORBIDDEN
            )

        invoice.delete()

        return Response(
            {
                'success':True,
                'message':'Invoice deleted successfully'
            }, status=status.HTTP_201_CREATED
        )