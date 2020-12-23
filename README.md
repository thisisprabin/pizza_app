# Pizza app

### Note -
> * Migrate command will add the master data.  ``python manage.py migrate``
> * Soft delete applied in case of delete operation.
> * Json schema validation used in input data validation.


##### APIS - 
* ##### Pizza type list API - 
    <h6>This API will provide the list of pizza types. Type - GET</h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/types/`` </h6>

* ##### Pizza size list API - 
    <h6>This API will provide the list of pizza types. Type - GET</h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/size/`` </h6>
    
* ##### Pizza size topping API - 
    <h6>This API will provide the list of pizza topping. Type - GET</h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/topping/`` </h6>
    
* ##### Pizza get API - 
    <h6>This API will provide pizza information. Type - GET</h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/<id>/`` </h6>
    
* ##### Pizza add API - 
    <h6>This API will provide pizza information. Type - POST</h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/`` </h6>
    ```json
        {
            "type": 1,
            "size": 2,
            "toppings": [3, 4, 6]
        }
  
* ##### Pizza update API - 
    <h6>This API will provide pizza information. Type - PATCH</h6>
    * <h6>Only toppings can be updated. </h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/`` </h6>
    ```json
        {
            "id": 1,
            "toppings": [3, 4, 6]
        }
    
* ##### Pizza delete API - 
    <h6>This API will delete pizza information. Type - DELETE</h6>
    *  <h6>``http://127.0.0.1:8000/api/pizza/<id>/`` </h6>