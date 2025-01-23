# :shopping_cart: Order Processing System
simplified Order Processing System for an online store.

## :sparkles: Features

- **Stock Management**: Validate product availability and update stock counts after successful orders.
- **Payment Processing**: Integrate a mock payment gateway to simulate payment transactions.
- **Order Confirmation Emails**: Send detailed order confirmation emails to customers upon successful purchase.
- **Error Handling**: Gracefully handle issues such as stock unavailability or payment failures.
- **User Authentication**: Ensure only registered users can place orders (Bonus).
- **Logging**: Record important events and errors during order processing (Bonus).
- **Containerization**: Package the application into a Docker container for easy deployment.
- **Container Registry Integration**: Push Docker images to a container registry like Docker Hub.

## :hammer_and_wrench: Setup Instructions

### :framed_picture: Ready Docker Imgage
- [https://hub.docker.com/r/dohaelsawi/order-processing-system-flask-app](https://hub.docker.com/r/dohaelsawi/order-processing-system-flask-app)

---
### :seedling: **create .env**
- first create a `.env` file in the root of the project
- attach the following environment variables
```
SECRET_KEY=super_difficult_secret_key
MONGO_URI=mongodb://mongo:27017/order_processing_system
JWT_SECRET_KEY=super_secure_token
JWT_ACCESS_TOKEN_EXPIRES=1
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USE_SSL=False
MAIL_USERNAME=dohaelsawy18@gmail.com
MAIL_PASSWORD=efiktolvvsbcmsrt 
```
You can set up the application using **Docker Compose** or a **Python virtual environment**.

---

### :whale: **Setup via Docker Compose**
1. **Ensure Docker and Docker Compose are installed**:
   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

2. **Build and Start the Application**:
   - Navigate to the project directory.
   - Run the following command to build and start the services:
     ```bash
     docker-compose up --build
     ```

3. **Access the Application**:
   - The app will run on [http://0.0.0.0:5000](http://0.0.0.0:5000) (adjust if the `docker-compose.yml` specifies a different port).

4. **Stop the Application**:
   - Use the following command to stop the services:
     ```bash
     docker-compose down
     ```

---

### :snake: **Setup via Python Virtual Environment**
1. **Install Python and Virtual Environment**:
   - Ensure Python (3.x) is installed: [Download Python](https://www.python.org/downloads/)
   - Install `virtualenv` if not already installed:
     ```bash
     pip install virtualenv
     ```

2. **Set Up the Virtual Environment**:
   - Navigate to the project directory.
   - Create a virtual environment:
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - On Linux/Mac:
       ```bash
       source venv/bin/activate
       ```
     - On Windows:
       ```bash
       venv\Scripts\activate
       ```

3. **Install Dependencies**:
   - Install the required Python packages:
     ```bash
     pip install -r requirements.txt
     ```

  
4. **Run the Application**:
   - Start the Flask app:
     ```bash
     flask run
     ```
   - The app will run at [http://127.0.0.1:5000](http://127.0.0.1:5000) by default.

---


Both methods will get the application up and running, so choose the one that best suits your environment. :tada:
