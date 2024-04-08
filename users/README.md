# User App Documentation

## User Models:

Sure, let's break down the user models:

1. **UserManager:** This class is a custom manager for the `User` model. It provides methods for creating regular users and superusers.

    - `create_user(email, password, **extra_fields)`: Method for creating a regular user with the given email and password.
    - `create_superuser(email, password, **extra_fields)`: Method for creating a superuser with the given email and password. It sets `is_staff`, `is_superuser`, and `is_active` to `True` by default.

2. **User:** This class represents the user model.

    - It inherits from `AbstractBaseUser` and `PermissionsMixin`.
    - `id`: UUIDField for the primary key.
    - `USERNAME_FIELD`: The field to use as the username, in this case, it's set to `email`.
    - `REQUIRED_FIELDS`: Additional fields required when creating a user.
    - `first_name`, `last_name`, `email`, `mobile`, `is_active`, `is_staff`, `verified`, `is_billing_verified`, `date_joined`, `timestamp`: Various fields for user data.
    - `generate_token()`: Method to generate a token for the user.
    - `verify_token(token, max_age)`: Static method to verify a token.
    - `objects`: The custom `UserManager` manager.

3. **UserProfile:** This class represents the user profile model.

    - `id`: UUIDField for the primary key.
    - `user`: OneToOneField to the `User` model, creating a one-to-one relationship between `User` and `UserProfile`.
    - `profile_image`, `career`, `about`, `gender`, `marital_status`, `address`, `date_of_birth`, `timestamp`: Various fields for additional user profile data.
    - `profileImageURL`: Property to get the URL of the profile image.
    
4. **post_save_create_user_profile:** Signal handler function that automatically creates a `UserProfile` instance whenever a `User` instance is created. This function is connected to the `post_save` signal of the `User` model.

These models provide a comprehensive representation of user data, including authentication, profile information, and signal handling for related operations.