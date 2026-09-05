-- Example: re-add company FK after a drop (schema evolution demo)

ALTER TABLE public.employee
ADD CONSTRAINT employee_company_id_fkey
FOREIGN KEY (company_id) REFERENCES public.company (company_id);
