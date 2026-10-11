"""Illustrative IAM policy configuration (not a SailPoint integration)."""
ROLE_ENTITLEMENTS = {
    "Engineer": {"github_read", "jira_read", "deploy_dev"},
    "Finance Analyst": {"erp_read", "invoice_create"},
    "Finance Manager": {"erp_read", "invoice_approve"},
    "HR Specialist": {"hr_read", "hr_edit"},
    "Sales Associate": {"crm_read", "crm_edit"},
    "IT Admin": {"directory_admin", "vpn_access", "github_read"},
}
SOD_CONFLICTS = [("invoice_create", "invoice_approve"), ("hr_edit", "directory_admin")]
PRIVILEGED = {"directory_admin", "invoice_approve", "deploy_prod"}
ALL_ENTITLEMENTS = sorted(set().union(*ROLE_ENTITLEMENTS.values(), {"deploy_prod"}))
