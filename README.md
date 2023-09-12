# PasspressoSecure ☕️ Backend

## How to Run the Server Locally

1. Install [Node.js](https://nodejs.org/en/download/).
2. Clone this repository.
3. Run `npm install` in the root directory of the repository.
4. Run `npm start` to start the server.
5. Go to `http://localhost:3000` in your browser to check if the server is running.

## API Documentation

### Base URL

The base URL for accessing the PasspressoSecure API is `http://localhost:3000`.

### Endpoints

#### 1. Check Server Status

- **URL:** `/`
- **Method:** GET
- **Description:** Get a message indicating that the PasspressoSecure server is running.
- **Response:**
    - **Status Code:** 200 OK
    - **Response Body:**
      ```
      PasspressoSecure server is running!
      ```

#### 2. Retrieve All Users

- **URL:** `/api/users`
- **Method:** GET
- **Description:** Retrieve information about all users stored in the database.
- **Response:**
    - **Status Code:** 200 OK
    - **Response Body:**
      ```
      {
          "message": "success",
          "data": [Array of user objects]
      }
      ```
- **Example Python Request:**
  ```python
  import requests

  response = requests.get("http://localhost:3000/api/users")
  data = response.json()
  ```

#### 3. Retrieve All Passwords

- **URL:** `/api/passwords`
- **Method:** GET
- **Description:** Retrieve information about all passwords stored in the database.
- **Response:**
    - **Status Code:** 200 OK
    - **Response Body:**
      ```
      {
          "message": "success",
          "data": [Array of password objects]
      }
      ```
- **Example Python Request:**
  ```python
  import requests

  response = requests.get("http://localhost:3000/api/passwords")
  data = response.json()
  ```

#### 4. Retrieve User's Password with Score

- **URL:** `/api/user/:uId/password`
- **Method:** GET
- **Description:** Retrieve a random password associated with a user, along with the user's score.
- **URL Parameters:**
    - `uId`: The user's ID.
- **Response:**
    - **Status Code:** 200 OK
    - **Response Body:**
      ```
      {
          "message": "success",
          "data": {
              "score": User's score,
              "password": {
                  "serviceUrl": Password's service URL,
                  "username": Password's username
              }
          }
      }
      ```
- **Example Python Request:**
  ```python
  import requests

  uId = "sampleUid"  # Replace with the desired user's ID
  response = requests.get(f"http://localhost:3000/api/user/{uId}/password")
  data = response.json()
  ```

#### 5. Add Passwords and Update User's Score

- **URL:** `/api/passwords/add`
- **Method:** POST
- **Description:** Add passwords to a user's account and update the user's score.
- **Request Body:**
  ```
  {
      "passwords": JSON array of password objects,
      "uId": User's ID,
      "score": User's new score
  }
  ```
- **Response:**
    - **Status Code:** 200 OK
    - **Response Body:**
      ```
      {
          "message": "success"
      }
      ```
- **Example Python Request:**
  ```python
  import requests

  data = {
      "passwords": [
          {
              "serviceUrl": "example.com",
              "username": "user123"
          },
          {
              "serviceUrl": "test.com",
              "username": "testuser"
          }
      ],
      "uId": "sampleUid",
      "score": 100
  }

  response = requests.post("http://localhost:3000/api/passwords/add", json=data)
  result = response.json()
  ```

### Error Responses

If an error occurs, the API will respond with an error message in the following format:

```
{
    "error": "Error message"
}
```
