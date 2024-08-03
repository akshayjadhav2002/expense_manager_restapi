### Expense Manager API Documentation

This documentation covers the various endpoints available in the Expense Manager API. The base URL for the API is `https://expense-manager-w.onrender.com`.

## 1. User Registration
### Endpoint: `/register`
- **Method**: `POST`
- **Description**: Register a new user.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  - **201 Created**: 
    ```json
    {
      "message": "User registered successfully"
    }
    ```
  - **400 Bad Request**: 
    ```json
    {
      "error": "Username already exists"
    }
    ```

## 2. User Login
### Endpoint: `/login`
- **Method**: `POST`
- **Description**: Log in and obtain a JWT token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  - **200 OK**: 
    ```json
    {
      "access_token": "jwt_token"
    }
    ```
  - **401 Unauthorized**: 
    ```json
    {
      "error": "Invalid username or password"
    }
    ```

## 3. Add Expense Category
### Endpoint: `/categories`
- **Method**: `POST`
- **Description**: Add a new expense category.
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`
- **Request Body**:
  ```json
  {
    "name": "string",
    "description": "string",
    "image_url": "string"
  }
  ```
- **Response**:
  - **201 Created**: 
    ```json
    {
      "id": "int",
      "name": "string",
      "description": "string",
      "image_url": "string"
    }
    ```

## 4. Add Expense
### Endpoint: `/expenses`
- **Method**: `POST`
- **Description**: Add a new expense.
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`
- **Request Body**:
  ```json
  {
    "amount": "float",
    "category_id": "int",
    "description": "string",
    "date": "YYYY-MM-DD"
  }
  ```
- **Response**:
  - **201 Created**: 
    ```json
    {
      "id": "int",
      "amount": "float",
      "category_id": "int",
      "description": "string",
      "date": "YYYY-MM-DD",
      "category_image_url": "string",
      "is_deleted": "boolean"
    }
    ```
  - **400 Bad Request**: 
    ```json
    {
      "error": "Category not found"
    }
    ```

## 5. Get All Expenses
### Endpoint: `/expenses`
- **Method**: `GET`
- **Description**: Retrieve all expenses.
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`
- **Response**:
  - **200 OK**: 
    ```json
    [
      {
        "id": "int",
        "amount": "float",
        "category_id": "int",
        "description": "string",
        "date": "YYYY-MM-DD",
        "category_image_url": "string",
        "is_deleted": "boolean"
      },
      ...
    ]
    ```

## 6. Delete Expense
### Endpoint: `/expenses/{id}`
- **Method**: `DELETE`
- **Description**: Mark an expense as deleted.
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`
- **Path Parameters**:
  - `id`: ID of the expense to delete.
- **Response**:
  - **200 OK**: 
    ```json
    {
      "message": "Expense deleted successfully",
      "expense": {
        "id": "int",
        "amount": "float",
        "category_id": "int",
        "description": "string",
        "date": "YYYY-MM-DD",
        "is_deleted": "boolean"
      }
    }
    ```
  - **404 Not Found**: 
    ```json
    {
      "error": "Expense not found"
    }
    ```

## 7. Get Deleted Expenses
### Endpoint: `/expenses/deleted`
- **Method**: `GET`
- **Description**: Retrieve all deleted expenses.
- **Headers**: `Authorization: Bearer <JWT_TOKEN>`
- **Response**:
  - **200 OK**: 
    ```json
    [
      {
        "id": "int",
        "amount": "float",
        "category_id": "int",
        "description": "string",
        "date": "YYYY-MM-DD",
        "category_image_url": "string",
        "is_deleted": "boolean"
      },
      ...
    ]
    ```

### Authentication
All endpoints except `/register` and `/login` require authentication. Obtain a JWT token from the `/login` endpoint and include it in the `Authorization` header of your requests in the format `Bearer <JWT_TOKEN>`.

### Error Handling
The API uses standard HTTP status codes to indicate the success or failure of a request. Responses include descriptive error messages to assist in debugging.

### Testing
Use tools like Postman, Insomnia, or `curl` to interact with the API. Ensure to replace placeholder values (like `<JWT_TOKEN>`) with actual data received from the API.
