# Organizations App

Sure, let's break down the models in detail:

### Organisation Model:

- **Fields:**
  - `id`: A UUID field used as the primary key for the Organisation model.
  - `owner`: A foreign key to the User model, indicating the owner of the organisation. It's set to null and blank=True, meaning it's optional.
  - `name`: A CharField representing the name of the organisation.
  - `has_trial`: A boolean field indicating whether the organisation has a trial period. It's set to False by default.
  - `timestamp`: A DateTimeField automatically set to the current date and time when the organisation is created.

- **Meta Class:**
  - `ordering`: Specifies the default ordering for the Organisation model. In this case, it's ordered by the timestamp field in descending order.

### Group Model:

- **Fields:**
  - `id`: A UUID field used as the primary key for the Group model.
  - `organisation`: A foreign key to the Organisation model, indicating the organisation to which the group belongs.
  - `name`: A CharField representing the name of the group.
  - `image`: An ImageField representing an image associated with the group. It's optional, allowing blank and null values.
  - `description`: A TextField for describing the group. It's optional, allowing blank and null values.
  - `timestamp`: A DateTimeField automatically set to the current date and time when the group is created.

- **Manager:**
  - `GroupManager`: This manager provides a method to calculate the percentage change in the number of groups for a given organisation within the last month.

- **Methods:**
  - `members()`: Returns all the members associated with the group.
  - `random_10_members()`: Returns a random selection of 10 members associated with the group.
  - `random_10_admin_members()`: Returns a random selection of 10 admin members associated with the group.
  - `members_count()`: Returns the count of members associated with the group.
  - `imageURL()`: Returns the URL of the group's image, if available.
  - `group_owner()`: Returns the admin member who is the owner of the group, if any.

- **Meta Class:**
  - `ordering`: Specifies the default ordering for the Group model. In this case, it's ordered by the timestamp field in descending order.

These models represent organisations and groups within the application. The Organisation model contains information about organisations, including their owner and trial status. The Group model represents groups within organisations and provides methods for managing group members and retrieving group-related data.