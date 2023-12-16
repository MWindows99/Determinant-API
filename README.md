# Determinant API
This is an API that generates determinant problems.

## Installation
Install the dependencies using `pip install -U -r requirements.txt`.

## Usage
Run the server using `python main.py`.

## Endpoint
Requests to the API are done using JSON. The following endpoints are available:

 - URL: `/matrix/question`  
   Method: `POST`  
   Request Body: `size` (Required)  
   Description: Generate a problem.
 - URL: `/matrix/answer`  
   Method: `POST`  
   Request Body: `uid` (Required), `answer` (Required)  
   Description: Check your answers.

## License
Please watch the [License](https://github.com/MWindows99/Determinant-API/edit/main/LICENSE) file for more information.
