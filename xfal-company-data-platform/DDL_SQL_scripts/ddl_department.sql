-- public.department definition

CREATE TABLE IF NOT EXISTS public.department (
    department_id   serial4 PRIMARY KEY,
    department_name varchar(255) NOT NULL
);
