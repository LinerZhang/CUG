CREATE TYPE gender_type AS ENUM ('male', 'female');
CREATE TYPE ticket_class AS ENUM ('VIP', 'Basic');
CREATE TYPE order_status AS ENUM ('pending', 'paid', 'cancelled');

CREATE TABLE actors (
actor_id SERIAL PRIMARY KEY, 
actor_name VARCHAR(50) NOT NULL,
gender gender_type NOT NULL,  
birthday DATE NOT NULL,
biography TEXT
);

CREATE TABLE theaters (
theater_id SERIAL PRIMARY KEY, 
theater_name VARCHAR(255) NOT NULL,
address VARCHAR(255) NOT NULL, 
seats INT NOT NULL CHECK (seats > 0),  
contact_num VARCHAR(20) NOT NULL
);

CREATE TABLE dramas (
drama_id SERIAL PRIMARY KEY, 
drama_name VARCHAR(50) NOT NULL,
description TEXT NOT NULL,
duration INT NOT NULL CHECK (duration > 0)  
);

CREATE TABLE performances (
performance_id SERIAL PRIMARY KEY, 
drama_id INT NOT NULL,
theater_id INT NOT NULL,
FOREIGN KEY (drama_id) REFERENCES dramas(drama_id),
FOREIGN KEY (theater_id) REFERENCES theaters(theater_id)
);

CREATE TABLE performance_actors (
performance_id INT NOT NULL,
role VARCHAR(50) NOT NULL,
actor_id INT NOT NULL,
FOREIGN KEY (performance_id) REFERENCES performances(performance_id),
FOREIGN KEY (actor_id) REFERENCES actors(actor_id)
);

CREATE TABLE schedules (
theater_id INT NOT NULL,
performance_id INT NOT NULL,
start_time TIMESTAMP NOT NULL, 
end_time TIMESTAMP NOT NULL,    
PRIMARY KEY (theater_id, performance_id),
FOREIGN KEY (theater_id) REFERENCES theaters(theater_id),
FOREIGN KEY (performance_id) REFERENCES performances(performance_id),
CHECK (start_time < end_time)  
);

CREATE TABLE tickets (
ticket_id SERIAL PRIMARY KEY,  
performance_id INT NOT NULL,
price DECIMAL(10, 2) NOT NULL CHECK (price > 0),  
left_tickets INT NOT NULL CHECK (left_tickets >= 0), 
class ticket_class NOT NULL, 
FOREIGN KEY (performance_id) REFERENCES performances(performance_id)
);

CREATE TABLE users (
user_id SERIAL PRIMARY KEY,  
user_name VARCHAR(50) NOT NULL,
gender gender_type NOT NULL,  
birthday DATE NOT NULL, 
country VARCHAR(50) NOT NULL,
password VARCHAR(255) NOT NULL  
);

CREATE TABLE orders (
order_id SERIAL PRIMARY KEY, 
user_id INT NOT NULL,
ticket_id INT NOT NULL,
seat_id VARCHAR(3) NOT NULL,
status order_status DEFAULT 'pending',  
FOREIGN KEY (user_id) REFERENCES users(user_id),
FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
);

CREATE TABLE staff (
work_id SERIAL PRIMARY KEY,  
work_name VARCHAR(50) NOT NULL,
password VARCHAR(255) NOT NULL 
);
