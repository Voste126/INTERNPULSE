import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Product
from django.core.cache import cache

# Automatically clear the cache before each test to reset throttle state.
@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()

@pytest.mark.django_db
def test_create_product():
    client = APIClient()
    url = reverse('product-list-create')
    data = {
        "name": "Test Product",
        "category": "Electronics",
        "price": "499.99",
        "stock_status": "in_stock",
        "sku": "TESTSKU123",
        "description": "A sample test product."
    }
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    # Access product details via the 'product' key.
    assert response.data['product']['name'] == "Test Product"
    assert Product.objects.count() == 1

@pytest.mark.django_db
def test_get_product_list():
    # Create a sample product.
    Product.objects.create(
        name="Product1",
        category="Gadgets",
        price=99.99,
        stock_status="in_stock",
        sku="P1",
        description="Test description"
    )
    client = APIClient()
    url = reverse('product-list-create')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # The original paginated data is now nested under the 'product' key.
    paginated_data = response.data['product']
    assert 'results' in paginated_data
    assert len(paginated_data['results']) == 1

@pytest.mark.django_db
def test_get_product_detail():
    product = Product.objects.create(
        name="Product2",
        category="Books",
        price=19.99,
        stock_status="in_stock",
        sku="P2",
        description="Book product"
    )
    client = APIClient()
    url = reverse('product-detail', args=[product.id])
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # Access product details via the 'product' key.
    assert response.data['product']['name'] == "Product2"

@pytest.mark.django_db
def test_update_product():
    product = Product.objects.create(
        name="Old Name",
        category="Toys",
        price=49.99,
        stock_status="in_stock",
        sku="P3",
        description="Old description"
    )
    client = APIClient()
    url = reverse('product-detail', args=[product.id])
    updated_data = {
        "name": "Updated Name",
        "category": "Toys",
        "price": "59.99",
        "stock_status": "out_of_stock",
        "sku": "P3",  # SKU remains unchanged for update.
        "description": "Updated description"
    }
    response = client.put(url, updated_data, format='json')
    assert response.status_code == status.HTTP_200_OK
    product.refresh_from_db()
    # Convert product.price to float for comparison.
    assert float(product.price) == 59.99
    assert product.stock_status == "out_of_stock"

@pytest.mark.django_db
def test_delete_product():
    product = Product.objects.create(
        name="Product to Delete",
        category="Furniture",
        price=199.99,
        stock_status="in_stock",
        sku="P4",
        description="To be deleted"
    )
    client = APIClient()
    url = reverse('product-detail', args=[product.id])
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Product.objects.count() == 0

@pytest.mark.django_db
def test_rate_limiting():
    """
    Using the default throttle rate of 100 requests per minute from settings,
    this test sends up to 51 POST requests. In this test environment,
    only 50 requests are allowed before throttling kicks in.
    We therefore expect exactly 50 allowed requests and that the 51st request returns a 429.
    """
    client = APIClient()
    url = reverse('product-list-create')
    data = {
        "name": "Throttle Test",
        "category": "Test",
        "price": "10.00",
        "stock_status": "in_stock",
        "description": "Testing rate limiting"
    }
    allowed_requests = 0
    total_requests = 51  # We'll check for 50 allowed requests then the 51st should fail.
    
    for i in range(total_requests):
        data['sku'] = f"THROTTLESKU_{i}"
        response = client.post(url, data, format='json')
        if response.status_code == status.HTTP_201_CREATED:
            allowed_requests += 1
        elif response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            break

    # Expect exactly 50 allowed requests.
    assert allowed_requests == 50, f"Expected 50 allowed requests, got {allowed_requests}"
    # And a subsequent request should return 429.
    data['sku'] = "THROTTLESKU_extra"
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
