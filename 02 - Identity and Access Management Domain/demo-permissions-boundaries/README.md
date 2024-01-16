# Walk-through (WIP)

Work in progress...

## High-level Walk-through

1. first create a managed policy to define the boundary for the new users
1. give users the permissions policies they need, but we want those users to be restricted
1. create managed policy `SooperDooperCompanyBoundaries`
1. allows designated user to create all X-Company users, but only with the SooperDooperCompanyBoundaries permissions boundary created in previous step
1. create the following customer managed policy named `SooperDooperIamEngineersBoundaries`. This policy defines the maximum permissions that our user can have.
1. Because the permissions boundary limits the maximum permissions, but does not grant access on its own, we must create a permissions policy for our user.
1. creates the following policy named `SooperDooperIamEngineersPermissions`
1. log in as the new IAM user and have them create a policy and assign to a group.
1. he can create new users with any permissions that they need, but he must assign them the SooperDooperCompanyBoundaries policy as a permissions boundary. Permissions policy would be: `SooperDooperCloudSysAdminPermissions`

### Creation Process steps

1. Create managed policy `SooperDooperCompanyBoundaries`
1. create customer managed policy named `SooperDooperIamEngineersBoundaries`
1. create the policy named `SooperDooperIamEngineersPermissions`
1. log in as the new IAM user
1. as new user create a policy called `SooperDooperCloudSysAdminPermissions`
1. create other new user and assign `SooperDooperCloudSysAdminPermissions` policy that was just created
1. first, do not include a permissions boundary. **You should get an error message**
1. second, go back, add the `SooperDooperCompanyBoundaries` and try to create again. This time it should work

### Demo Testing steps

1. Sign-in as the newly created user
1. attempt to look at IAM policies and remove the boundary. This fails due to the boundaries in place.
1. Attempt to navigate to DynamoDB, and this should fail as well, since the boundary did not allow them to do so.

### CONTINUE HERE

...
