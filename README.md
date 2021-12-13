[//]: # (<div style="text-align: center;">)

## Software Requirements Specification
___

### 1. Introduction

FlaskReddit is a minimalist Reddit clone. It is build in Python
with the Flask library. 

---
### 2. Purpose

The purpose is to create a simple CRUD-based application that can be interacted with
via an API client such as Postman or through the web interface via a browser.
This project was built to test my skills and learn the flow of creating a web application from the ground up.


---
### 3. Scope (libraries, dependencies etc)

Two data models are implemented on a PostgreSQL database with one-to-one, one-to-many and many-to-many relationships.
One database for testing/development and another database for production. These are hosted on a single AWS EC2 instance.
Closer to production the code will be hosted on a separate EC2 instance.

I have utilised the following:

* `flask` as the web framework 
* `PostgreSQL` as the database
* `SQLAlchemy` for my Object Relational Mapping (ORM) - How the application interfaces with the database
* `Marshmallow` is used to serialise, deserialise and validate data to and from the database and application
* `flask-migrate` is used to handle database migrations during development, testing and production
* `jwt_entended` handles some authorisation and authentication
* `bootstrap` for the presentation of our front end. 

---
#### 3.1 Database Entity Diagram

---
#### 3.2 Database Tables

---
#### 3.3 API Endpoints
[Raw format](docs/HarryCashel-FlaskReddit-1.0.0-resolved.yaml)

[OpenApi](https://app.swaggerhub.com/apis-docs/HarryCashel/FlaskReddit/1.0.0#/)


---
#### 3.4 Functionalities

* Functionalities

  ##### Users
  * User registration
  * User login
  * User logout
  * View user owned subreddits/threads/comments
  * Update user details
  * Delete user account

  #### Subreddits
  * View all subreddits
  * Show subreddits by id
  * Create a new subreddit
  * Update subreddit (owner/admin)
  * Join a subreddit
  * Leave a subreddit (member only)
  * Delete a subreddit (owner/admin)
  * Get list of user joined subreddits 
  * View all threads of specific subreddit
  
  #### Threads
  * Get all threads (API only)
  * Create thread (member of subreddit)
  * Update thread (owner only)
  * Delete thread (owner only)
  * Get thread by id
  * Create comment
  * Update comment
  * Delete comment



---
### 4. Installation

___
#### 4.1 Project and Environment Setup

---
#### 4.2 File Structure

___
#### 4.3 Set Up Databases (Testing and Development)

---
#### 4.4 Run Migrations

---
#### 4.5 Run Automated Tests

---
#### 4.6 Running the application on an AWS EC2 Instance

---
### 5. Continuous Integration/Continuous Deployment



---



[//]: # (</div>)