"""Manage users, groups, roles, and API tokens."""

from proxmox_api import ProxmoxAPI

api = ProxmoxAPI(
    "192.168.1.100",
    user="root@pam",
    token_name="mytoken",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
)

# --- Users ---

# List all users
for user in api.access.list_users():
    print(f"User: {user['userid']}  Enabled: {user.get('enable', 1)}")

# Create a new user
api.access.create_user(
    userid="deploy@pve",
    password="s3cure-p@ss",
    comment="CI/CD deployment account",
    groups="admins",
)

# --- Groups ---

# Create a group
api.access.create_group(groupid="developers", comment="Dev team")

# --- Roles ---

# List existing roles
for role in api.access.list_roles():
    print(f"Role: {role['roleid']}  Privs: {role.get('privs', '')}")

# Create a custom role with limited privileges
api.access.create_role(
    roleid="VMOperator",
    privs="VM.Audit,VM.Console,VM.PowerMgmt",
)

# --- ACLs (assign permissions) ---

# Give the developers group VMOperator access to /vms
api.access.update_acl(
    path="/vms",
    roles="VMOperator",
    groups="developers",
)

# --- API Tokens ---

# Create an API token for the deploy user
token = api.access.create_user_token(
    userid="deploy@pve",
    tokenid="ci-token",
    privsep=True,
    comment="Token for CI pipeline",
)
print(f"Token created: {token}")

# List tokens for a user
for t in api.access.list_user_tokens("deploy@pve"):
    print(f"  Token: {t['tokenid']}  Expire: {t.get('expire', 'never')}")

# --- Cleanup ---
api.access.delete_user_token("deploy@pve", "ci-token")
api.access.delete_user("deploy@pve")
api.access.delete_role("VMOperator")
api.access.delete_group("developers")
print("Cleanup complete.")
