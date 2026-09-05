-- Example: add an extra FK-style relationship (requires matching column)
-- Demonstrates ALTER TABLE ... ADD CONSTRAINT pattern used in schema evolution.

ALTER TABLE public.employee
ADD CONSTRAINT employee_email_not_blank
CHECK (email IS NULL OR length(trim(email)) > 0);
