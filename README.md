# IoT Devices
A simple application for managing IoT devices in Python.
## Idea
The main goal of this IoT device management application is to provide a streamlined and efficient platform for managing various IoT devices. The application will facilitate operations such as adding, updating, retrieving, and deleting devices, along with managing their associated locations and API users. By leveraging a robust stack including aiohttp for asynchronous operations, Peewee for ORM, and PostgreSQL for database management, the application aims to offer a scalable and maintainable solution for managing IoT devices in different environments.
# Technological stack
- aiohttp
- peewee
- loguru
- PostgreSQL
- Docker
- PyTests
- Postman
# Starting a project
- Run the Docker container:
```
docker compose up -d
```
# API Endpoints:
## Locations
- Create a location<br>
POST /locations<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "Boston"<br>
}
## API Users
- Create an API User<br>
POST /api_users<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "John Doe",<br>
&nbsp;&nbsp;&nbsp;"email": "john.doe@example.com",<br>
&nbsp;&nbsp;&nbsp;"password": "securepassword"<br>
}
## Devices:
- Retrieve all devices<br>
GET /devices
- Create a device<br>
POST /devices<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "Thermostat",<br>
&nbsp;&nbsp;&nbsp;"type": "Temperature Sensor",<br>
&nbsp;&nbsp;&nbsp;"login": "admin"<br>
&nbsp;&nbsp;&nbsp;"password": "password",<br>
&nbsp;&nbsp;&nbsp;"location_id": 1,<br>
&nbsp;&nbsp;&nbsp;"api_user_id": 1<br>
}
- Update device<br>
PUT /device/{id}<br>
Content-Type: application/json<br>
{<br>
&nbsp;&nbsp;&nbsp;"name": "iPhone",<br>
&nbsp;&nbsp;&nbsp;"type": "15 Pro Max",<br>
&nbsp;&nbsp;&nbsp;"login": "admin"<br>
&nbsp;&nbsp;&nbsp;"password": "newpassword",<br>
&nbsp;&nbsp;&nbsp;"location_id": 3,<br>
&nbsp;&nbsp;&nbsp;"api_user_id": 2<br>
}
- Delete device<br>
DELETE /device/{id}
# Future plans:
- User Authentication: Implement secure authentication for API users to ensure only authorized access.
- Integrate a message broker like RabbitMQ or Kafka for handling real-time data streams and event processing.
- Role-Based Access Control: Introduce roles and permissions to manage user access to different parts of the application.
## Developer
- Sviatoslav Baranetskyi<br>
  Email: svyatoslav.baranetskiy738@gmail.com
