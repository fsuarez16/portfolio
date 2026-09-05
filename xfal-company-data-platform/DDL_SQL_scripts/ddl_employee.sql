-- public.employee definition

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
