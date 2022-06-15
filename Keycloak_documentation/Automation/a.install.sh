ansible-galaxy collection install community.general

# group https://docs.ansible.com/ansible/latest/collections/community/general/keycloak_group_module.html#ansible-collections-community-general-keycloak-group-module
# roles https://docs.ansible.com/ansible/latest/collections/community/general/keycloak_role_module.html#ansible-collections-community-general-keycloak-role-module
# gener https://docs.ansible.com/ansible/latest/collections/community/general/index.html

# ALTERNATIVE:

#   1°:
#     Groups
#       create-one
#     Users
#       connect-to-one-group
#       connect-to-one-role-using-client
#     Clients                            <-- [ Clients ] o [ Client-Scopes for Share ]
#       Name-of-it
#         Roles                          <-- is  visible
#           create-one
#           set-attributes               <-- not visible in access token ( it requires a separate GET )
#         Mappers
#           Group Membership
#             create-one
#           User Attributes
#             create-one

#   2°:
#     Users
#       set-attributes { CAN : Group_Flag1,Flag2,.. }
#
#     Clients                            <-- [ Clients ] o [ Client-Scopes for Share ]
#       Name-of-it
#         Mappers
#           User Attributes
#             create-one                 <-- Listening on CAN
