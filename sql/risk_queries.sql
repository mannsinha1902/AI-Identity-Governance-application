-- Dormant access grants
SELECT e.employee_id, e.role, a.entitlement, a.days_since_used
FROM employees e JOIN access_grants a USING(employee_id)
WHERE a.days_since_used > 90 ORDER BY a.days_since_used DESC;

-- Grants retained for terminated identities (policy violation)
SELECT e.employee_id, a.entitlement
FROM employees e JOIN access_grants a USING(employee_id)
WHERE e.status = 'terminated';

-- Number of grants per department
SELECT e.department, COUNT(*) AS grants
FROM employees e JOIN access_grants a USING(employee_id)
GROUP BY e.department ORDER BY grants DESC;
