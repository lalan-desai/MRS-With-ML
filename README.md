# Movie Recommendation System with ML

This project is a movie recommendation system built with Django. It uses the `TfidfVectorizer` for content-based filtering and MySQL for database management. Perfect for your final year project :)

## Features

- User authentication and profile management
- Dynamic search functionality using jQuery
- Movie recommendations based on user preferences
- Admin panel with content management
- Visualization various statistics using Chart.js

## Technologies Used

- Django
- TfidfVectorizer
- MySQL
- jQuery
- Chart.js

## Visual Demonstration

### Initial Selection
![Initial Selection](https://github.com/user-attachments/assets/e65b2b88-a627-4905-a63c-002a0da21663)

### Dashboard
![Dashboard](https://github.com/user-attachments/assets/0d99a36e-29da-42fa-8266-63f938ce8a9b)

### Content Page
![Content Page](https://github.com/user-attachments/assets/a7dbb8b1-1a5a-4399-bec0-80730884c79a)

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/lalan-desai/MRS-With-ML.git
   cd MRS-With-ML
   ```
2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Update the database configurations in `MRS_With_ML/settings.py` to match your MySQL setup.
4. Apply the migrations:
	```sh
	python manage.py migrate
	```
5. Import the provided database schema:
	- Use the `dashboard_content.sql` file for movies content (Must!).
	- You can import the SQL file into MySQL using a command like:
	```sh
	mysql -u your_username -p your_database_name < dashboard_content.sql
	```
 
6. Start the development server:
	```sh
	python manage.py runserver
	```

## License

All rights reserved. This project and its contents are the intellectual property of Lalan-Desai. No part of this project may be reproduced, distributed, or transmitted in any form or by any means without the prior written permission of the author.
