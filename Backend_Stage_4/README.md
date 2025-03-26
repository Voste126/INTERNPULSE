# Stage #4 Task for Backend Developers - Individual Task

## Task: Create a RESTful API for Business Product Management with Rate Limiting

### Objective

Develop a RESTful API to manage a business’s product catalog, incorporating rate limiting to prevent abuse and ensure fair usage. **No user authentication is required** for this task. Implement CRUD operations for products and manage product stock availability.

---

### Endpoints (RESTful Best Practices with Versioning)

- **GET /api/v1/products**  
    Retrieve a list of all products with name, category, price, and stock status. Implement pagination for large collections.

- **GET /api/v1/products/{id}**  
    Get details of a specific product, including availability status, SKU (Stock Keeping Unit), and description.

- **POST /api/v1/products**  
    Add a new product to the business catalog. Validate input for all required fields (e.g., name, price, category).

- **PUT /api/v1/products/{id}**  
    Update details of an existing product, including stock availability. Ensure idempotency.

- **DELETE /api/v1/products/{id}**  
    Remove a product from the catalog when it’s discontinued or out of stock permanently.

---

### Rate Limiting

- Implement rate limiting for all endpoints to restrict the number of requests per client within a time frame (e.g., 100 requests per minute per IP or client ID).
- Use headers in responses to inform clients about their rate limit status:
        - `X-RateLimit-Limit`
        - `X-RateLimit-Remaining`
        - `X-RateLimit-Reset`

#### Example of a RESTful Endpoint Response with Versioning and Rate Limiting

**GET /api/v1/products/{id}**  

```json
{
    "product": {
        "id": "P001",
        "name": "Wireless Mouse",
        "category": "Electronics",
        "price": 29.99,
        "stock_status": "in_stock",
        "sku": "WM-001",
        "description": "A high-precision wireless mouse with ergonomic design."
    },
    "status": "success",
    "message": "Product details retrieved successfully.",
    "headers": {
        "X-RateLimit-Limit": 100,
        "X-RateLimit-Remaining": 99,
        "X-RateLimit-Reset": 1668144600
    }
}
```

---

### Framework-Specific Instructions

#### For Node.js Developers

- Use **Express.js** to set up the API.
- Implement rate limiting with a package like `express-rate-limit`.

#### For Django Developers

- Use **Django REST Framework**.
- Implement rate limiting with Django’s built-in throttling capabilities.

#### For Flask Developers

- Use **Flask** to create the API.
- Implement rate limiting with `Flask-Limiter` or similar middleware.

---

### Deliverables

1. A RESTful API for business product management with integrated rate limiting, no user authentication, and status messages.
2. Documentation on how to set up, run, and interact with the API, including rate limiting behavior.

---

### By Completing This Task, You Will Learn

- **Rate Limiting Implementation**: How to protect APIs from abuse by implementing and configuring rate limits.
- **RESTful API Design**: Structuring APIs for resource management with CRUD operations, versioning, and status messages.
- **Framework Proficiency**: Deepening your understanding of frameworks like Express.js, Django, or Flask, especially in the context of API security.
- **Error Handling**: Providing clear feedback on rate limit violations alongside normal operations.
- **Data Management**: Handling data for a business product catalog, considering real-world scenarios like stock availability.

---

### Deployment

Deploy your API to platforms like:

- **Vercel**
- **Render**
- **PythonAnywhere**
- **Netlify**
- Or any other free or paid platform you know!

---

### Submission

- **Deadline**: Before 5 PM (WAT) on the 31st of March.  
- **Submit Here**: [Submission Link]

---

### RESTful Tips

- Fix your API endpoint URL (follow API naming conventions - e.g., no underscores, no singular collections, etc.).
- Version your APIs (e.g., `/api/v1/products`, `/api/v1/categories/{category_id}`).
- Refactor your functions (use early returns/guard patterns, etc.).
- Add a one-line description for every endpoint in your Swagger docs.
- Add validation.
- Ensure the frontend receives proper RESTful responses.
- Use the right status codes.

---

### Professional RESTful Response Example

### Success Response

```json
{
    "status": "success",
    "code": 200,
    "message": "Products retrieved successfully",
    "data": {
        "products": [
            {
                "id": "P001",
                "name": "Wireless Mouse",
                "category": "Electronics",
                "price": 29.99,
                "stock_status": "in_stock",
                "sku": "WM-001",
                "description": "A high-precision wireless mouse with ergonomic design.",
                "created_at": "2024-10-20T15:32:45Z",
                "updated_at": "2024-10-21T10:15:30Z"
            },
            {
                "id": "P002",
                "name": "Office Chair",
                "category": "Furniture",
                "price": 89.99,
                "stock_status": "out_of_stock",
                "sku": "OC-002",
                "description": "An ergonomic office chair with lumbar support.",
                "created_at": "2024-10-01T09:00:00Z",
                "updated_at": "2024-10-16T12:45:15Z"
            }
        ],
        "pagination": {
            "current_page": 1,
            "per_page": 10,
            "total_pages": 3,
            "total_products": 25
        }
    },
    "links": {
        "self": "/api/v1/products?page=1",
        "next": "/api/v1/products?page=2",
        "prev": null
    }
}
```

### Error Response

```json
{
    "status": "error",
    "code": 404,
    "message": "Product not found",
    "errors": {
        "details": "No product was found with the given ID."
    }
}
```
