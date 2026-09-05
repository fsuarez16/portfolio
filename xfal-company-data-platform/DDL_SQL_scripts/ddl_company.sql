-- public.company definition

CREATE TABLE IF NOT EXISTS public.company (
    company_id   serial4 PRIMARY KEY,
    company_name varchar(255) NOT NULL,
    address      varchar(255) NOT NULL,
    city         varchar(100) NOT NULL,
    state        bpchar(2)    NOT NULL,
    zip          bpchar(5)    NOT NULL
);
