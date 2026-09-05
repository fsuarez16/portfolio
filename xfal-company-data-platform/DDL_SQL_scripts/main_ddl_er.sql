-- XFAL portfolio schema
-- Order: company → department → employee (FK dependencies)

CREATE TABLE IF NOT EXISTS public.company (
    company_id   serial4 PRIMARY KEY,
    company_name varchar(255) NOT NULL,
    address      varchar(255) NOT NULL,
    city         varchar(100) NOT NULL,
    state        bpchar(2)    NOT NULL,
    zip          bpchar(5)    NOT NULL
);

CREATE TABLE IF NOT EXISTS public.department (
    department_id   serial4 PRIMARY KEY,
    department_name varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS public.employee (
    employee_id   serial4 PRIMARY KEY,
    first_name    varchar(100) NOT NULL,
    last_name     varchar(100) NOT NULL,
    phone1        varchar(15)  NULL,
    phone2        varchar(15)  NULL,
    email         varchar(255) NULL,
    company_id    int4         NULL,
    department_id int4         NULL,
    CONSTRAINT employee_company_id_fkey
        FOREIGN KEY (company_id) REFERENCES public.company (company_id),
    CONSTRAINT employee_department_id_fkey
        FOREIGN KEY (department_id) REFERENCES public.department (department_id)
);
