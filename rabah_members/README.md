# Members App Documentations

## Database Models

### `Family` Model

The `Family` model represents a family entity with the following attributes:

- `name`: CharField representing the name of the family. This field has a maximum length of 250 characters and is optional (blank=True).
- `timestamp`: DateTimeField representing the timestamp when the family object was created. This field is automatically populated with the current date and time when the object is created using `auto_now_add=True`.

#### Methods:

- `__str__()`: This method returns a string representation of the family object, which is the family name.

### `Member` Model

The `Member` model represents a member within an organization with the following attributes:

- `id`: UUIDField serving as the primary key for the member object.
- `user`: ForeignKey linking the member to a `User` object. It establishes a one-to-many relationship with the `User` model.
- `organisation`: ForeignKey linking the member to an `Organisation` object. It establishes a one-to-many relationship with the `Organisation` model.
- `is_owner`: BooleanField indicating whether the member is the owner of the organization.
- `is_admin_member`: BooleanField indicating whether the member has administrative privileges within the organization.
- `is_active`: BooleanField indicating whether the member is active within the organization.
- `groups`: ManyToManyField representing the groups that the member belongs to within the organization. It allows for a many-to-many relationship between members and groups.
- `timestamp`: DateTimeField representing the timestamp when the member object was created. This field is automatically populated with the current date and time when the object is created using `auto_now_add=True`.
- `family`: ForeignKey linking the member to a `Family` object. It establishes a one-to-many relationship with the `Family` model.
- `family_relationship`: CharField representing the relationship of the member within the family. This field has a maximum length of 250 characters and is optional (blank=True).

#### Meta Class:

- `ordering`: Specifies the default ordering of member objects by the timestamp field in descending order ("-timestamp").

#### Methods:

- `__str__()`: This method returns a string representation of the member object, which consists of the user's first and last names.
- `get_family_members`: This property method returns a queryset of all members belonging to the same family as the current member.
- `create_family()`: This method creates a new family associated with the member, if one does not already exist.

### `MemberManager` Model Manager

The `MemberManager` class provides custom queryset methods for querying `Member` objects:

- `is_admin_user(user, organisation_id)`: Checks if the given user is an active admin member within the specified organization.
- `is_member_user(user, organisation_id)`: Checks if the given user is an active member within the specified organization.
- `calculate_member_increment_percentage(organisation_id)`: Calculates the percentage change in the number of members within the organization over the last month.

#### Signals:

- `post_save_create_member`: This signal handler function creates a member object when an organization is created. It assigns the organization owner as an admin member and creates a family associated with the owner if one does not already exist.

This documentation provides a detailed overview of the `Family` and `Member` models, their attributes, methods, and manager functionality.