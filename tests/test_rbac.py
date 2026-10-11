from src.rbac_engine import allowed, excessive

def test_role_permissions():
    assert allowed("Engineer","github_read")
    assert not allowed("Engineer","directory_admin")
    assert excessive("Engineer",["github_read","directory_admin"])==["directory_admin"]
