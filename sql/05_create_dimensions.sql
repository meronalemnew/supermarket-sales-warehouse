CREATE TABLE warehouse.dim_branch (
    branch_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    branch_code VARCHAR(1) NOT NULL,
    city VARCHAR(50) NOT NULL,
    UNIQUE (branch_code, city)
);

CREATE TABLE warehouse.dim_product_line (
    product_line_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    product_line VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE warehouse.dim_customer_segment (
    customer_segment_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_type VARCHAR(20) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    UNIQUE (customer_type, gender)
);

CREATE TABLE warehouse.dim_payment (
    payment_key INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payment_method VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE warehouse.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(15) NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    day_of_week VARCHAR(15) NOT NULL
);

CREATE TABLE warehouse.dim_time (
    time_key INTEGER PRIMARY KEY,
    full_time TIME NOT NULL UNIQUE,
    hour INTEGER NOT NULL,
    minute INTEGER NOT NULL,
    time_of_day VARCHAR(20) NOT NULL
);