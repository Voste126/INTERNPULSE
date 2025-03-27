from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Product
from .serializers import ProductSerializer
from .mixins import RateLimitBodyMixin  # Import the mixin

# List and Create View with RateLimitBodyMixin
class ProductListCreateAPIView(RateLimitBodyMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle]

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of products.",
        operation_summary="Retrieve a paginated list of products.",
        responses={200: ProductSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        self.initial(request, *args, **kwargs)  # Trigger throttle checks.
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Add a new product to the catalog.",
        operation_summary="Add a new product to the catalog.",
        request_body=ProductSerializer,
        responses={201: ProductSerializer()}
    )
    def post(self, request, *args, **kwargs):
        self.initial(request, *args, **kwargs)  # Trigger throttle checks.
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": e.detail},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Retrieve, Update, Delete View with RateLimitBodyMixin
class ProductRetrieveUpdateDestroyAPIView(RateLimitBodyMixin, generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    throttle_classes = [AnonRateThrottle]
    lookup_field = 'id'

    @swagger_auto_schema(
        operation_description="Retrieve product details by id.",
        operation_summary="Retrieve product details by id.",
        responses={200: ProductSerializer()}
    )
    def get(self, request, *args, **kwargs):
        self.initial(request, *args, **kwargs)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update product details (idempotent).",
        operation_summary="Update product details (idempotent).",
        request_body=ProductSerializer,
        responses={200: ProductSerializer()}
    )
    def put(self, request, *args, **kwargs):
        self.initial(request, *args, **kwargs)
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": e.detail},
                            status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a product from the catalog.",
        operation_summary="Delete a product from the catalog.",
        responses={204: 'No Content'}
    )
    def delete(self, request, *args, **kwargs):
        self.initial(request, *args, **kwargs)
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

