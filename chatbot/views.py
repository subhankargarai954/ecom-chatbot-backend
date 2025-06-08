from .models import ChatMessage
from .serializers import RegisterSerializer
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from django.db.models import Q



# This is for debugging purpose only, comment it after check. 
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)


def test_view(request):
    logger.info("Test view called")
    return HttpResponse("Test successful")


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_list(request):
    """
    List all products or search by name/category/price range
    """
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', 0)
    max_price = request.GET.get('max_price', 100000)

    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__icontains=query),
        price__gte=min_price,
        price__lte=max_price
    )

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def product_detail(request, pk):
    """
    Retrieve a single product by ID
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_view(request):
    """
    Accepts a user query and returns matching product list.
    Expected input: {"message": "looking for laptops"}
    """
    query = request.data.get("message", "")

    if not query:
        return Response({"error": "Query message is required."}, status=400)

    results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    )

    serializer = ProductSerializer(results, many=True)
    return Response({
        "message": f"Found {len(results)} products for query: '{query}'",
        "results": serializer.data
    })


# Update chat_view to Save History
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat_view(request):
    query = request.data.get("message", "")

    if not query:
        return Response({"error": "Query message is required."}, status=400)

    results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    )

    serializer = ProductSerializer(results, many=True)
    response_text = f"Found {len(results)} products for query: '{query}'"

    # Save the chat to DB
    ChatMessage.objects.create(
        user=request.user,
        message=query,
        response=response_text
    )

    return Response({
        "message": response_text,
        "results": serializer.data
    })


# Add History and Reset Endpoints
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    messages = ChatMessage.objects.filter(
        user=request.user).order_by('-timestamp')
    data = [
        {
            "message": msg.message,
            "response": msg.response,
            "timestamp": msg.timestamp
        } for msg in messages
    ]
    return Response(data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_chat(request):
    ChatMessage.objects.filter(user=request.user).delete()
    return Response({"message": "Chat history cleared."})


