# Welcome to the Django UserJourney Map Documentation!

[![License](https://img.shields.io/github/license/lazarus-org/dj-userjourney-map)](https://github.com/lazarus-org/dj-userjourney-map/blob/main/LICENSE)
[![PyPI Release](https://img.shields.io/pypi/v/dj-userjourney-map)](https://pypi.org/project/dj-userjourney-map/)
[![Pylint Score](https://img.shields.io/badge/pylint-10/10-brightgreen?logo=python&logoColor=blue)](https://www.pylint.org/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/dj-userjourney-map)](https://pypi.org/project/dj-userjourney-map/)
[![Supported Django Versions](https://img.shields.io/pypi/djversions/dj-userjourney-map)](https://pypi.org/project/dj-userjourney-map/)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=yellow)](https://github.com/pre-commit/pre-commit)
[![Open Issues](https://img.shields.io/github/issues/lazarus-org/dj-userjourney-map)](https://github.com/lazarus-org/dj-userjourney-map/issues)
[![Last Commit](https://img.shields.io/github/last-commit/lazarus-org/dj-userjourney-map)](https://github.com/lazarus-org/dj-userjourney-map/commits/main)
[![Languages](https://img.shields.io/github/languages/top/lazarus-org/dj-userjourney-map)](https://github.com/lazarus-org/dj-userjourney-map)
[![Coverage](https://codecov.io/gh/lazarus-org/dj-userjourney-map/branch/main/graph/badge.svg)](https://codecov.io/gh/lazarus-org/dj-userjourney-map)

`dj-userjourney-map` is a Django package developed by [Lazarus](https://github.com/Lazarus-org) to simplify the creation, management, and visualization of user journey maps in Django applications.
User journey maps are powerful tools for understanding user experiences, capturing stages, actions, feedback, pain points, and opportunities. This package provides a robust, customizable framework for developers to integrate interactive journey maps into their projects, with a user-friendly admin interface, and flexible templates for rendering dynamic visualizations.

Whether you're building a customer experience platform, analyzing user interactions, or designing product workflows, `dj-userjourney-map` offers the tools to model and display user journeys efficiently, making it ideal for modern Django applications.


## Project Detail

- Language: Python >= 3.9
- Framework: Django >= 4.2
- Django REST Framework: >= 3.14

## Documentation Overview

The documentation is organized into the following sections:

- **[Quick Start](#quick-start)**: Get up and running quickly with basic setup instructions.
- **[Usage](#usage)**: How to effectively use the package in your projects.
- **[API Guide](#api-guide)**: Detailed information on available APIs and endpoints.
- **[Settings](#settings)**: Configuration options and settings you can customize.

---

# Quick Start

This section provides a fast and easy guide to getting the `dj-userjourney-map` package up and running in your Django project.
Follow the steps below to quickly set up the package and start using the package.

## 1. Install the Package

**Option 1: Using `pip` (Recommended)**

Install the package via pip:

```bash
$ pip install dj-userjourney-map
```
**Option 2: Using `Poetry`**

If you're using Poetry, add the package with:

```bash
$ poetry add dj-userjourney-map
```

**Option 3: Using `pipenv`**

If you're using pipenv, install the package with:

```bash
$ pipenv install dj-userjourney-map
```

## 2. Install Django REST Framework (Optional for API Support)

If you plan to use the optional DRF API for managing user journey maps, you will need to install Django REST Framework. If it's not already installed in your project, you can install it:

**Using pip:**

```bash
$ pip install djangorestframework
```

## 3. Add to Installed Apps

After installing the necessary packages, ensure that both `rest_framework` (if using the API) and `persona_manager` are added to the `INSTALLED_APPS` in your Django `settings.py` file:

```python
INSTALLED_APPS = [
   # ...
   "rest_framework",  # Only needed if using the API

   "persona_manager",
   "journey_map",
   # ...
]
```

### 4. (Optional) Configure API Filters

To enable filtering through the API, install ``django-filter``, include ``django_filters`` in your ``INSTALLED_APPS`` and configure the filter settings.

Install ``django-filter``:

**Using pip:**

```bash
$ pip install django-filter
```

Add `django_filters` to your `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
   # ...
   "django_filters",
   # ...
]
```

Then, set the filter class configuration in your ``settings.py``:

```python
JOURNEY_MAP_API_USER_JOURNEY_FILTERSET_CLASS = "journey_map.api.filters.UserJourneyFilter"
JOURNEY_MAP_API_JOURNEY_STAGE_FILTERSET_CLASS = "journey_map.api.filters.JourneyStageFilter"
JOURNEY_MAP_API_JOURNEY_ACTION_FILTERSET_CLASS = "journey_map.api.filters.JourneyActionFilter"
JOURNEY_MAP_API_USER_FEEDBACK_FILTERSET_CLASS = "journey_map.api.filters.UserFeedbackFilter"
JOURNEY_MAP_API_PAIN_POINT_FILTERSET_CLASS = "journey_map.api.filters.PainPointFilter"
JOURNEY_MAP_API_OPPORTUNITY_FILTERSET_CLASS = "journey_map.api.filters.OpportunityFilter"
```

You can also define your custom `FilterClass` and reference it in here if needed. This allows you to customize the filtering behavior according to your requirements. for more detailed info, refer to the [Settings](#settings) section.


## 5. Apply Migrations

Run the following command to apply the necessary migrations:
```shell
python manage.py migrate
```

## 6. Add project URLs

If you wish to use the optional API or the Django Template View Include them in your project’s `urls.py` file:
```python
from django.urls import path, include
from persona_manager.views import UserPersonaListView

urlpatterns = [
    # ...
    # User Persona related urls
    path("user_persona/", UserPersonaListView.as_view(), name="user-persona-list"), # Template View
    path("user_persona/api/", include("persona_manager.api.routers.main")),   # Only needed if using the API
    
    # User Journey Map related urls
    path('journey_map/', include("journey_map.urls")), # List & Detail Template View
    path('journey_map/api/', include("journey_map.api.routers")) # Only needed if using the API
    # ...
]
```

---

# API Guide

## Overview

The `dj-userjourney-package` provides APIs for managing user journey maps, enabling the creation and analysis of user experiences within your application. The API exposes six main endpoints:

- **User Journeys**: Manages user journey maps for specific personas.
- **Journey Stages**: Organizes stages within a user journey.
- **Journey Actions**: Details specific actions users take in a stage.
- **User Feedback**: Captures feedback relateda specific action.
- **Pain Points**: Records pain points associated with an action.
- **Opportunities**: Identifies opportunities for improvement linked to an action.

---

## Endpoints

### **User Journeys API**

#### **List User Journeys**
- **Endpoint**: `GET /user-journeys/`
- **Description**: Retrieves a list of all user journeys.
- **Response Example**:
```json
{
    "results": [
        {
            "id": 1,
            "name": "Customer Onboarding",
            "description": "Journey for new customer onboarding",
            "persona": "New User",
            "stages": [
                {
                    "id": 1,
                    "stage_name": "Sign-up",
                    "order": 1,
                    "actions": [
                      {
                            "id": 1,
                            "stage": "Journey (1) - Sign-up",
                            "action_description": "action desc for the sign up stage",
                            "touchpoint": "somewhere",
                            "order": 0,
                            "feedbacks": [
                                {
                                    "id": 1,
                                    "action": "Stage (1) - action desc for the sign up stage",
                                    "feedback_text": "good feedback",
                                    "emotion": "happy",
                                    "intensity": 4,
                                    "is_positive": true
                                }
                            ],
                            "pain_points": [
                                {
                                    "id": 11,
                                    "action": "Stage (1) - action desc for the sign up stage",
                                    "description": "this is a pain point",
                                    "severity": 3
                                }
                            ],
                            "opportunities": [
                                {
                                    "id": 11,
                                    "action": "Stage (1) - action desc for the sign up stage",
                                    "description": "this is an opportunity"
                                }
                            ]
                        }
                    ]
                }
            ],
            "created_at": "2025-04-24T10:00:00Z",
            "updated_at": "2025-04-24T10:00:00Z"
        }
    ]
}
```

#### **Retrieve a User Journey**
- **Endpoint**: `GET /user-journeys/{id}/`
- **Description**: Fetches details of a specific user journey.
- **Response Fields**:
    - `id`: Unique identifier of the journey.
    - `name`: Name of the journey.
    - `description`: Description of the journey.
    - `persona`: The associated user persona.
    - `stages`: List of stages in the journey.
    - `created_at`: Creation timestamp.
    - `updated_at`: Last update timestamp.

#### **Create a User Journey**
- **Endpoint**: `POST /user-journeys/`
- **Payload Example**:
```json
{
    "name": "Customer Onboarding",
    "description": "Journey for new customer onboarding",
    "persona_id": 1
}
```

#### **Update a User Journey**
- **Endpoint**: `PATCH /user-journeys/{id}/`
- **Payload Example**:
```json
{
    "name": "Updated Onboarding",
    "persona_id": 2
}
```

#### **Delete a User Journey**
- **Endpoint**: `DELETE /user-journeys/{id}/`
- **Description**: Deletes a specific user journey.

---

### **Journey Stages API**

#### **List Journey Stages**
- **Endpoint**: `GET /journey-stages/`
- **Description**: Retrieves a list of all journey stages.
- **Response Example**:
```json
{
    "results": [
        {
            "id": 1,
            "journey": "Customer Onboarding",
            "stage_name": "Sign-up",
            "order": 1,
            "actions": [
                {
                    "id": 1,
                    "action_description": "Complete registration form",
                    "touchpoint": "Website",
                    "order": 1
                }
            ]
        }
    ]
}
```

#### **Create a Journey Stage**
- **Endpoint**: `POST /journey-stages/`
- **Payload Example**:
```json
{
    "journey_id": 1,
    "stage_name": "Sign-up",
    "order": 1
}
```

---

### **Journey Actions API**

#### **List Journey Actions**
- **Endpoint**: `GET /journey-actions/`
- **Description**: Retrieves a list of all journey actions.
- **Response Example**:
```json
{
    "results": [
        {
            "id": 1,
            "stage": "Sign-up",
            "action_description": "Complete registration form",
            "touchpoint": "Website",
            "order": 1,
            "feedbacks": [],
            "pain_points": [],
            "opportunities": []
        }
    ]
}
```

#### **Create a Journey Action**
- **Endpoint**: `POST /journey-actions/`
- **Payload Example**:
```json
{
    "stage_id": 1,
    "action_description": "Complete registration form",
    "touchpoint": "Website",
    "order": 1
}
```

---

### **User Feedback API**

#### **List User Feedback**
- **Endpoint**: `GET /user-feedback/`
- **Description**: Retrieves a list of all user feedback entries.
- **Response Example**:
```json
{
    "results": [
        {
            "id": 1,
            "action": "Complete registration form",
            "feedback_text": "Form was easy to use",
            "emotion": "happy",
            "intensity": 4,
            "is_positive": true
        }
    ]
}
```

#### **Create User Feedback**
- **Endpoint**: `POST /user-feedback/`
- **Payload Example**:
```json
{
    "action_id": 1,
    "feedback_text": "Form was easy to use",
    "emotion": "happy",
    "intensity": 4,
    "is_positive": true
}
```

---

### **Pain Points API**

#### **List Pain Points**
- **Endpoint**: `GET /pain-points/`
- **Description**: Retrieves a list of all pain points.
- **Response Example**:
```json
{
    "results": [
        {
            "id": 1,
            "action": "Complete registration form",
            "description": "Form validation errors unclear",
            "severity": "moderate"
        }
    ]
}
```

#### **Create a Pain Point**
- **Endpoint**: `POST /pain-points/`
- **Payload Example**:
```json
{
    "action_id": 1,
    "description": "Form validation errors unclear",
    "severity": "moderate"
}
```

---

### **Opportunities API**

#### **List Opportunities**
- **Endpoint**: `GET /opportunities/`
- **Description**: Retrieves a list of all opportunities.
- **Response Example**:
```json
{
    "results": [
        {
            "id": 1,
            "action": "Complete registration form",
            "description": "Add tooltips for form fields"
        }
    ]
}
```

#### **Create an Opportunity**
- **Endpoint**: `POST /opportunities/`
- **Payload Example**:
```json
{
    "action_id": 1,
    "description": "Add tooltips for form fields"
}
```

---

## Throttling

The API includes configurable throttling to limit request rates. You can customize throttle rates in the Django settings file for each endpoint, such as:

```ini
USER_JOURNEY_API_USER_THROTTLE_RATE = "100/day"
USER_JOURNEY_API_STAFF_THROTTLE_RATE = "60/minute"
```

Custom throttle classes can be defined for each ViewSet and referenced in the settings.

---

## Ordering, Filtering, and Search

The API supports ordering, filtering, and searching across all endpoints:

- **Ordering**: Results can be ordered by fields specific to each ViewSet (e.g., `order`, `created_at`).
- **Filtering**: Requires `django-filter` to be installed. Add `django_filters` to `INSTALLED_APPS` and specify filter classes (e.g., `journey_map.api.filters.UserJourneyFilter`) in settings.
- **Search**: Searchable fields are configurable via `search_fields` in each ViewSet.

These features can be customized in the Django settings.

---

## Pagination

The API uses limit-offset pagination, with configurable minimum, maximum, and default page sizes to control the number of results per page.

---

## Permissions

The default permission is `IsAuthenticated`, allowing access to all users. You can customize permissions by adding classes like `IsAdminUser` or creating custom permission classes in the settings.

---

## Parser Classes

The API supports the following default parsers:

- `JSONParser`
- `MultiPartParser`
- `FormParser`

You can modify parser classes for each ViewSet by updating the API settings to include additional parsers or customize existing ones.

---

## Configuration

All features (throttling, permissions, parsers, etc.) can be configured through the Django settings file. Refer to the [Settings](#settings) section for details.

# Usage

This section provides a comprehensive guide on how to utilize the package's key features, including the functionality of
the Django admin panels for managing user behaviors.

## Admin Site

If you are using a **custom admin site** in your project, you must pass your custom admin site configuration in your
Django settings. Otherwise, Django may raise the following error during checks or the ModelAdmin will not accessible in
the Admin panel.

To resolve this, In your ``settings.py``, add the following setting to specify the path to your custom admin site class
instance

```python
JOURNEY_MAP_ADMIN_SITE_CLASS = "path.to.your.custom.site"
```

example of a custom Admin Site:

```python
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"


# Instantiate the custom admin site as example
example_admin_site = CustomAdminSite(name="custom_admin")
```

and then reference the instance like this:

```python
JOURNEY_MAP_ADMIN_SITE_CLASS = "path.to.example_admin_site"
```

This setup allows `dj-userjourney-map` to use your custom admin site for its Admin interface, preventing any errors and
ensuring a smooth integration with the custom admin interface.

# User Journey Map Admin

The `dj-userjourney-package` provides a robust Django admin interface for managing user journey maps, including `UserJourney`, `JourneyStage`, `JourneyAction`, `UserFeedback`, `PainPoint`, and `Opportunity` models. Built with the `BaseModelAdmin` mixin, these interfaces offer administrators powerful tools to view, filter, search, and manage user journey data efficiently. Below are the features and functionalities of each admin interface.

---

## UserJourney Admin Panel

The `UserJourneyAdmin` class provides an admin interface for managing user journey records.

### Features

#### List Display

The list view for user journey records includes the following fields:

- **Name**: The name of the user journey.
- **Persona**: The associated user persona.
- **Created At**: The timestamp when the journey was created.
- **Updated At**: The timestamp of the last update.

#### Filtering

Admins can filter the list of user journey records based on:

- **Persona**: Filter by the associated user persona.
- **Created At**: Filter by the creation timestamp.

#### Search Functionality

Admins can search for user journey records using:

- **Name**: Search by journey name.
- **Description**: Search by journey description.

#### Autocomplete Fields

- **Persona**: Provides an autocomplete dropdown for selecting the associated `UserPersona`, improving usability when editing.

#### Inlines

- **Journey Stages**: Displays related `JourneyStage` records as an inline table (included if `JOURNEY_MAP_ADMIN_INCLUDE_INLINES` is `True`).

#### Read-Only Fields

The following fields are marked as read-only in the detailed view:

- **Created At**: The creation timestamp.
- **Updated At**: The last update timestamp.

#### Fieldsets

The detailed view organizes fields into collapsible sections:

- **Details**: `name`, `description`, `persona`.
- **Metadata (Collapsed)**: `created_at`, `updated_at`.

---

## JourneyStage Admin Panel

The `JourneyStageAdmin` class provides an admin interface for managing journey stage records.

### Features

#### List Display

The list view for journey stage records includes the following fields:

- **Stage Name**: The name of the stage.
- **Journey**: The associated user journey.
- **Order**: The order of the stage within the journey.

#### Filtering

Admins can filter the list of journey stage records based on:

- **Journey**: Filter by the associated user journey.

#### Search Functionality

Admins can search for journey stage records using:

- **Stage Name**: Search by stage name.
- **Journey Name**: Search by the name of the associated journey (via `journey__name`).

#### Autocomplete Fields

- **Journey**: Provides an autocomplete dropdown for selecting the associated `UserJourney`, enhancing usability when editing.

#### Inlines

- **Journey Actions**: Displays related `JourneyAction` records as an inline table (included if `JOURNEY_MAP_ADMIN_INCLUDE_INLINES` is `True`).

---

## JourneyAction Admin Panel

The `JourneyActionAdmin` class provides an admin interface for managing journey action records.

### Features

#### List Display

The list view for journey action records includes the following fields:

- **Truncated Description**: A shortened version of the action description.
- **Stage Name**: The name of the associated stage.
- **Journey**: The associated user journey (via `stage__journey`).
- **Order**: The order of the action within the stage.

#### Filtering

Admins can filter the list of journey action records based on:

- **Stage**: Filter by the associated stage.
- **Journey**: Filter by the associated journey (via `stage__journey`).

#### Search Functionality

Admins can search for journey action records using:

- **Action Description**: Search by action description.
- **Touchpoint**: Search by touchpoint.
- **Stage Name**: Search by the name of the associated stage (via `stage__stage_name`).

#### Autocomplete Fields

- **Stage**: Provides an autocomplete dropdown for selecting the associated `JourneyStage`.

#### Inlines

- **User Feedback**: Displays related `UserFeedback` records as an inline table.
- **Pain Points**: Displays related `PainPoint` records as an inline table.
- **Opportunities**: Displays related `Opportunity` records as an inline table.
  (Inlines included if `JOURNEY_MAP_ADMIN_INCLUDE_INLINES` is `True`).

---

## UserFeedback Admin Panel

The `UserFeedbackAdmin` class provides an admin interface for managing user feedback records.

### Features

#### List Display

The list view for user feedback records includes the following fields:

- **Truncated Feedback**: A shortened version of the feedback text.
- **Action Description**: A shortened description of the associated action.
- **Emotion**: The emotion associated with the feedback (e.g., happy, frustrated).
- **Intensity**: The intensity level of the feedback.
- **Is Positive**: Indicates if the feedback is positive.

#### Filtering

Admins can filter the list of user feedback records based on:

- **Is Positive**: Filter by positive or negative feedback.
- **Emotion**: Filter by emotion type.
- **Journey**: Filter by the associated journey (via `action__stage__journey`).

#### Search Functionality

Admins can search for user feedback records using:

- **Feedback Text**: Search by feedback content.
- **Action Description**: Search by the description of the associated action (via `action__action_description`).

#### Autocomplete Fields

- **Action**: Provides an autocomplete dropdown for selecting the associated `JourneyAction`.

---

## PainPoint Admin Panel

The `PainPointAdmin` class provides an admin interface for managing pain point records.

### Features

#### List Display

The list view for pain point records includes the following fields:

- **Truncated Description**: A shortened version of the pain point description.
- **Severity**: The severity level of the pain point (e.g., low, moderate, high).
- **Action Description**: A shortened description of the associated action.
- **Journey Name**: The name of the associated journey.

#### Filtering

Admins can filter the list of pain point records based on:

- **Severity**: Filter by severity level.
- **Action Order**: Filter by the order of the associated action.

#### Search Functionality

Admins can search for pain point records using:

- **Description**: Search by pain point description.
- **Action Description**: Search by the description of the associated action (via `action__action_description`).

#### Autocomplete Fields

- **Action**: Provides an autocomplete dropdown for selecting the associated `JourneyAction`.

---

## Opportunity Admin Panel

The `OpportunityAdmin` class provides an admin interface for managing opportunity records.

### Features

#### List Display

The list view for opportunity records includes the following fields:

- **Truncated Description**: A shortened version of the opportunity description.
- **Action Description**: A shortened description of the associated action.
- **Journey Name**: The name of the associated journey

#### Filtering

Admins can filter the list of opportunity records based on:

- **Action Order**: Filter by the order of the associated action.

#### Search Functionality

Admins can search for opportunity records using:

- **Description**: Search by opportunity description.
- **Action Description**: Search by the description of the associated action (via `action__action_description`).

#### Autocomplete Fields

- **Action**: Provides an autocomplete dropdown for selecting the associated `JourneyAction`.

---

Thank you for providing the details about the permission classes for the `dj-userjourney-package`. I’ve noted the following key points:

- **Permission Class Structure**: The package supports Django REST Framework (DRF)-style permission classes that must implement a `has_permission(self, request, view)` method, returning a boolean to indicate whether access is granted. For example, a typical implementation checks for user authentication, as shown in your example.
- **Pre-defined Permission Classes**: When DRF is not used, the package provides built-in permission classes located at:
  - `journey_map.permissions.IsAuthenticated`
  - `journey_map.permissions.IsAdminUser`
  - `journey_map.permissions.IsSuperUser`
  - `journey_map.permissions.AllowAny`
  - `journey_map.permissions.BasePermission` (a base class for implementing custom permissions).
- **DRF Compatibility**: DRF permission classes can also be used if DRF is part of the project.
- **Default Permission**: The default permission class is set to `JOURNEY_MAP_VIEW_PERMISSION_CLASS = "journey_map.permissions.IsAuthenticated"`, requiring users to be authenticated to access the views.

Since you’ve already provided the template views and an example section, and I’ve prepared the template views section, I assume you’d like me to update or confirm the template views section to reflect these permission details explicitly. Below, I’ve revised the **Template Views** section to incorporate the permission class details, ensuring accuracy and alignment with the provided information. If you meant for me to prepare a different section or have additional requirements, please clarify!

---

# User Journey Template Views

The `dj-userjourney-map` provides two class-based template views, `JourneyMapListView` and `JourneyMapDetailView`, for rendering user journey maps in a web interface. These views leverage Django’s generic views (`ListView` and `DetailView`) and include robust permission checks to control access, supporting both Django REST Framework (DRF)-style and package-specific permission classes. Below is a detailed overview of each view’s functionality and features.

---

## JourneyMapListView

The `JourneyMapListView` is a class-based `ListView` that displays a list of all user journeys, allowing users to browse and select a journey to view its detailed map.

### Features

#### Template
- **Template Name**: `journey_map_list.html`
- **Context Object Name**: `journeys`
- **Description**: Renders a list of `UserJourney` instances, typically displayed as a clickable list or table for navigation to detailed views.

#### Queryset
- **Model**: `UserJourney`
- **Optimization**: Uses `select_related("persona")` to fetch the associated `UserPersona` in a single query, reducing database hits.
- **Ordering**: Journeys are ordered by `name` for consistent presentation.

#### Access Control
- **Permission Classes**: Defined by `JOURNEY_MAP_VIEW_PERMISSION_CLASS`, defaulting to `journey_map.permissions.IsAuthenticated`. This requires users to be authenticated (i.e., `request.user.is_authenticated` returns `True`).
- **Supported Permissions**:
  - Package-specific: `IsAuthenticated`, `IsAdminUser`, `IsSuperUser`, `AllowAny` (from `journey_map.permissions`).
  - DRF-style: Any permission class with a `has_permission(self, request, view)` method, such as DRF’s `rest_framework.permissions.IsAuthenticated`.
  - Custom: Inherit from `journey_map.permissions.BasePermission` to create custom permissions.
- **Behavior**: The `BaseView`’s `check_permissions` method evaluates each permission class. If any `has_permission` method is missing or returns `False`, a `PermissionDenied` exception is raised, resulting in a 403 Forbidden response.

#### Usage
1. Navigate to the journey map list URL (e.g., `/journeys/`).
2. Ensure you are authenticated (per the default `IsAuthenticated` permission) or meet the requirements of the configured `JOURNEY_MAP_VIEW_PERMISSION_CLASS`.
3. View the list of user journeys, with each journey’s name and persona details displayed, and click to access the detailed view.

---

## JourneyMapDetailView

The `JourneyMapDetailView` is a class-based `DetailView` that renders a detailed user journey map, including the associated persona, stages, actions, feedback, pain points, and opportunities, presented in a timeline or structured format.

### Features

#### Template
- **Template Name**: `journey_map_detail.html`
- **Context Object Name**: `journey_data`
- **Description**: Renders a comprehensive view of a single `UserJourney`, including a hierarchical structure of stages and actions, with related feedback, pain points, and opportunities.

#### Queryset
- **Model**: `UserJourney`
- **Optimization**:
  - Uses `select_related("persona")` to fetch the associated `UserPersona`.
  - Uses `prefetch_related` with `Prefetch` objects to efficiently retrieve related `JourneyStage`, `JourneyAction`, `UserFeedback`, `PainPoint`, and `Opportunity` instances in a single query.
  - Stages and actions are ordered by their `order` field using `Prefetch` querysets.
- **Retrieval**: Fetches the journey by `id` using `get_object_or_404`, ensuring a 404 response if the journey does not exist.

#### Context Data
- **Structure**: The `journey_data` context is a dictionary containing:
  - `journey`: The `UserJourney` instance.
  - `persona`: The associated `UserPersona`.
  - `stages`: A list of stage dictionaries, each containing:
    - `stage`: The `JourneyStage` instance.
    - `actions`: A list of action dictionaries, each containing:
      - `action`: The `JourneyAction` instance.
      - `feedbacks`: List of related `UserFeedback` instances.
      - `pain_points`: List of related `PainPoint` instances.
      - `opportunities`: List of related `Opportunity` instances.
- **Efficiency**: Accesses prefetched data directly via `_prefetched_objects_cache` to avoid additional database queries.

#### Access Control
- **Permission Classes**: Defined by `JOURNEY_MAP_VIEW_PERMISSION_CLASS`, defaulting to `journey_map.permissions.IsAuthenticated`.
- **Supported Permissions**:
  - Package-specific: `IsAuthenticated`, `IsAdminUser`, `IsSuperUser`, `AllowAny` (from `journey_map.permissions`).
  - DRF-style: Any permission class with a `has_permission(self, request, view)` method.
  - Custom: Inherit from `journey_map.permissions.BasePermission` for tailored permissions.
- **Behavior**: Inherits permission checks from `BaseView`. A `PermissionDenied` exception is raised if access is not granted, resulting in a 403 Forbidden response.

#### Usage
1. Navigate to the journey map detail URL (e.g., `/journeys/1/`).
2. Ensure you are authenticated (per the default `IsAuthenticated` permission) or meet the requirements of the configured `JOURNEY_MAP_VIEW_PERMISSION_CLASS`.
3. View the detailed journey map, featuring:
   - Journey and persona details.
   - A timeline or structured display of stages and actions.
   - Associated feedback, pain points, and opportunities for each action.

---

## Configuration Notes

- **Permission Customization**:
  - The default `JOURNEY_MAP_VIEW_PERMISSION_CLASS = "journey_map.permissions.IsAuthenticated"` ensures only authenticated users can access the views.
  - Override `config.view_permission_class` in your Django settings to use other permissions, such as `IsAdminUser`, `IsSuperUser`, `AllowAny`, or a custom class inheriting from `journey_map.permissions.BasePermission`.
  - DRF permission classes (e.g., `rest_framework.permissions.IsAuthenticated`) are supported if DRF is installed.
- **Template Customization**: The `journey_map_list.html` and `journey_map_detail.html` templates can be overridden in your project to customize the UI, such as integrating with charting libraries (e.g., D3.js) or responsive layouts.
- **Query Optimization**: Both views are optimized for performance using `select_related` and `prefetch_related`, minimizing database queries even for complex, nested data.
- **Error Handling**: The views handle invalid journey IDs with a 404 response and unauthorized access with a 403 response, ensuring robust user feedback.

---

# Settings

This section outlines the available settings for configuring the `dj-userjourney-map` package. You can customize these
settings in your Django project's `settings.py` file to tailor the behavior of the system monitor to your
needs.

## Example Settings

Below is an example configuration with default values:

```python
# Admin Settings
JOURNEY_MAP_ADMIN_SITE_CLASS = None
JOURNEY_MAP_ADMIN_HAS_ADD_PERMISSION = True
JOURNEY_MAP_ADMIN_HAS_CHANGE_PERMISSION = True
JOURNEY_MAP_ADMIN_HAS_DELETE_PERMISSION = True
JOURNEY_MAP_ADMIN_HAS_MODULE_PERMISSION = True
JOURNEY_MAP_ADMIN_INCLUDE_INLINES = True
JOURNEY_MAP_ADMIN_INLINE_HAS_ADD_PERMISSION = True
JOURNEY_MAP_ADMIN_INLINE_HAS_CHANGE_PERMISSION = True
JOURNEY_MAP_ADMIN_INLINE_HAS_DELETE_PERMISSION = True

# Throttle Settings
JOURNEY_MAP_BASE_USER_THROTTLE_RATE = "30/minute"
JOURNEY_MAP_STAFF_USER_THROTTLE_RATE = "100/minute"
JOURNEY_MAP_API_THROTTLE_CLASSES = "journey_map.api.throttlings.RoleBasedUserRateThrottle"

# Global API Settings
JOURNEY_MAP_API_PAGINATION_CLASS = "journey_map.api.paginations.DefaultLimitOffSetPagination"
JOURNEY_MAP_API_EXTRA_PERMISSION_CLASS = None
JOURNEY_MAP_API_PARSER_CLASSES = [
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]

# UserJourney API Settings
JOURNEY_MAP_API_USER_JOURNEY_SERIALIZER_CLASS = None
JOURNEY_MAP_API_USER_JOURNEY_ORDERING_FIELDS = ["created_at", "updated_at"]
JOURNEY_MAP_API_USER_JOURNEY_SEARCH_FIELDS = ["name", "description"]
JOURNEY_MAP_API_USER_JOURNEY_FILTERSET_CLASS = None
JOURNEY_MAP_API_USER_JOURNEY_ALLOW_LIST = True
JOURNEY_MAP_API_USER_JOURNEY_ALLOW_RETRIEVE = True
JOURNEY_MAP_API_USER_JOURNEY_ALLOW_CREATE = True
JOURNEY_MAP_API_USER_JOURNEY_ALLOW_UPDATE = True
JOURNEY_MAP_API_USER_JOURNEY_ALLOW_DELETE = True

# JourneyStage API Settings
JOURNEY_MAP_API_JOURNEY_STAGE_SERIALIZER_CLASS = None
JOURNEY_MAP_API_JOURNEY_STAGE_ORDERING_FIELDS = ["order"]
JOURNEY_MAP_API_JOURNEY_STAGE_SEARCH_FIELDS = ["stage_name", "journey__name"]
JOURNEY_MAP_API_JOURNEY_STAGE_FILTERSET_CLASS = None
JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_LIST = True
JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_RETRIEVE = True
JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_CREATE = True
JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_UPDATE = True
JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_DELETE = True

# JourneyAction API Settings
JOURNEY_MAP_API_JOURNEY_ACTION_SERIALIZER_CLASS = None
JOURNEY_MAP_API_JOURNEY_ACTION_ORDERING_FIELDS = ["order"]
JOURNEY_MAP_API_JOURNEY_ACTION_SEARCH_FIELDS = ["action_description", "touchpoint"]
JOURNEY_MAP_API_JOURNEY_ACTION_FILTERSET_CLASS = None
JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_LIST = True
JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_RETRIEVE = True
JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_CREATE = True
JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_UPDATE = True
JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_DELETE = True

# UserFeedback API Settings
JOURNEY_MAP_API_USER_FEEDBACK_SERIALIZER_CLASS = None
JOURNEY_MAP_API_USER_FEEDBACK_ORDERING_FIELDS = ["created_at", "intensity", "is_positive"]
JOURNEY_MAP_API_USER_FEEDBACK_SEARCH_FIELDS = ["feedback_text"]
JOURNEY_MAP_API_USER_FEEDBACK_FILTERSET_CLASS = None
JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_LIST = True
JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_RETRIEVE = True
JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_CREATE = True
JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_UPDATE = True
JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_DELETE = True

# PainPoint API Settings
JOURNEY_MAP_API_PAIN_POINT_SERIALIZER_CLASS = None
JOURNEY_MAP_API_PAIN_POINT_ORDERING_FIELDS = ["severity"]
JOURNEY_MAP_API_PAIN_POINT_SEARCH_FIELDS = ["description"]
JOURNEY_MAP_API_PAIN_POINT_FILTERSET_CLASS = None
JOURNEY_MAP_API_PAIN_POINT_ALLOW_LIST = True
JOURNEY_MAP_API_PAIN_POINT_ALLOW_RETRIEVE = True
JOURNEY_MAP_API_PAIN_POINT_ALLOW_CREATE = True
JOURNEY_MAP_API_PAIN_POINT_ALLOW_UPDATE = True
JOURNEY_MAP_API_PAIN_POINT_ALLOW_DELETE = True

# Opportunity API Settings
JOURNEY_MAP_API_OPPORTUNITY_SERIALIZER_CLASS = None
JOURNEY_MAP_API_OPPORTUNITY_ORDERING_FIELDS = ["action__order"]
JOURNEY_MAP_API_OPPORTUNITY_SEARCH_FIELDS = ["description"]
JOURNEY_MAP_API_OPPORTUNITY_FILTERSET_CLASS = None
JOURNEY_MAP_API_OPPORTUNITY_ALLOW_LIST = True
JOURNEY_MAP_API_OPPORTUNITY_ALLOW_RETRIEVE = True
JOURNEY_MAP_API_OPPORTUNITY_ALLOW_CREATE = True
JOURNEY_MAP_API_OPPORTUNITY_ALLOW_UPDATE = True
JOURNEY_MAP_API_OPPORTUNITY_ALLOW_DELETE = True

# Template View Settings
JOURNEY_MAP_VIEW_PERMISSION_CLASS = "journey_map.permissions.IsAuthenticated"
```

# Settings Overview

This section provides a detailed explanation of the available settings in the package. You can configure these settings in your Django project's `settings.py` file to tailor the behavior of the system to your needs.

## Admin Settings

### `JOURNEY_MAP_ADMIN_SITE_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies a custom `AdminSite` class for the admin interface, enabling enhanced customization of the admin panel.

---

### `JOURNEY_MAP_ADMIN_HAS_ADD_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Determines whether users have permission to add new records in the admin panel.

---

### `JOURNEY_MAP_ADMIN_HAS_CHANGE_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Controls whether users can modify existing records in the admin panel.

---

### `JOURNEY_MAP_ADMIN_HAS_DELETE_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Specifies whether users have permission to delete records in the admin panel.

---

### `JOURNEY_MAP_ADMIN_HAS_MODULE_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Determines whether users have module-level permissions in the admin panel.

---

### `JOURNEY_MAP_ADMIN_INCLUDE_INLINES`
**Type**: `bool`  

**Default**: `True`  

**Description**: Controls whether inline forms (e.g., `JourneyStageInline`, `JourneyActionInline`) are included in the admin interface.

---

### `JOURNEY_MAP_ADMIN_INLINE_HAS_ADD_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Determines whether users can add new inline records in the admin panel.

---

### `JOURNEY_MAP_ADMIN_INLINE_HAS_CHANGE_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Controls whether users can modify existing inline records in the admin panel.

---

### `JOURNEY_MAP_ADMIN_INLINE_HAS_DELETE_PERMISSION`
**Type**: `bool`  

**Default**: `True`  

**Description**: Specifies whether users can delete inline records in the admin panel.

---

## Throttle Settings

### `JOURNEY_MAP_BASE_USER_THROTTLE_RATE`
**Type**: `str`  

**Default**: `"30/minute"`  

**Description**: Defines the API request throttle rate for regular users (requests per time unit).

---

### `JOURNEY_MAP_STAFF_USER_THROTTLE_RATE`
**Type**: `str`  

**Default**: `"100/minute"`  

**Description**: Defines the API request throttle rate for staff users (requests per time unit).

---

### `JOURNEY_MAP_API_THROTTLE_CLASSES`
**Type**: `str`  

**Default**: `"journey_map.api.throttlings.RoleBasedUserRateThrottle"`  

**Description**: Specifies the throttle class for API requests, enabling role-based rate limiting.

---

## Global API Settings

### `JOURNEY_MAP_API_PAGINATION_CLASS`
**Type**: `str`  

**Default**: `"journey_map.api.paginations.DefaultLimitOffSetPagination"`  

**Description**: Defines the pagination class for API responses, controlling how results are paginated.

---

### `JOURNEY_MAP_API_EXTRA_PERMISSION_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies additional permission classes for API access control, supplementing default permissions.

---

### `JOURNEY_MAP_API_PARSER_CLASSES`
**Type**: `List[str]`  

**Default**:  
```python
[
    "rest_framework.parsers.JSONParser",
    "rest_framework.parsers.MultiPartParser",
    "rest_framework.parsers.FormParser",
]
```  

**Description**: Specifies parsers for handling different request data formats in API endpoints.

---

## UserJourney API Settings

### `JOURNEY_MAP_API_USER_JOURNEY_SERIALIZER_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Defines the serializer class for `UserJourney` API responses, allowing customization of serialization.

---

### `JOURNEY_MAP_API_USER_JOURNEY_ORDERING_FIELDS`
**Type**: `List[str]`  

**Default**: `["created_at", "updated_at"]`  

**Description**: Specifies fields for ordering results in the `UserJourney` API.

---

### `JOURNEY_MAP_API_USER_JOURNEY_SEARCH_FIELDS`
**Type**: `List[str]`  

**Default**: `["name", "description"]`  

**Description**: Defines fields that can be searched within the `UserJourney` API.

---

### `JOURNEY_MAP_API_USER_JOURNEY_FILTERSET_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies the filter class for `UserJourney` API responses, enabling advanced filtering with `django-filter`.

---

### `JOURNEY_MAP_API_USER_JOURNEY_ALLOW_LIST`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables listing of `UserJourney` resources via the API.

---

### `JOURNEY_MAP_API_USER_JOURNEY_ALLOW_RETRIEVE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows retrieving specific `UserJourney` records through the API.

---

### `JOURNEY_MAP_API_USER_JOURNEY_ALLOW_CREATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the creation of new `UserJourney` records via the API.

---

### `JOURNEY_MAP_API_USER_JOURNEY_ALLOW_UPDATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows updating existing `UserJourney` records through the API.

---

### `JOURNEY_MAP_API_USER_JOURNEY_ALLOW_DELETE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the deletion of `UserJourney` records via the API.

---

## JourneyStage API Settings

### `JOURNEY_MAP_API_JOURNEY_STAGE_SERIALIZER_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Defines the serializer class for `JourneyStage` API responses.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_ORDERING_FIELDS`
**Type**: `List[str]`  

**Default**: `["order"]`  

**Description**: Specifies fields for ordering results in the `JourneyStage` API.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_SEARCH_FIELDS`
**Type**: `List[str]`  

**Default**: `["stage_name", "journey__name"]`  

**Description**: Defines fields that can be searched within the `JourneyStage` API.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_FILTERSET_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies the filter class for `JourneyStage` API responses.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_LIST`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables listing of `JourneyStage` resources via the API.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_RETRIEVE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows retrieving specific `JourneyStage` records through the API.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_CREATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the creation of new `JourneyStage` records via the API.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_UPDATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows updating existing `JourneyStage` records through the API.

---

### `JOURNEY_MAP_API_JOURNEY_STAGE_ALLOW_DELETE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the deletion of `JourneyStage` records via the API.

---

## JourneyAction API Settings

### `JOURNEY_MAP_API_JOURNEY_ACTION_SERIALIZER_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Defines the serializer class for `JourneyAction` API responses.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_ORDERING_FIELDS`
**Type**: `List[str]`  

**Default**: `["order"]`  

**Description**: Specifies fields for ordering results in the `JourneyAction` API.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_SEARCH_FIELDS`
**Type**: `List[str]`  

**Default**: `["action_description", "touchpoint"]`  

**Description**: Defines fields that can be searched within the `JourneyAction` API.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_FILTERSET_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies the filter class for `JourneyAction` API responses.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_LIST`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables listing of `JourneyAction` resources via the API.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_RETRIEVE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows retrieving specific `JourneyAction` records through the API.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_CREATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the creation of new `JourneyAction` records via the API.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_UPDATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows updating existing `JourneyAction` records through the API.

---

### `JOURNEY_MAP_API_JOURNEY_ACTION_ALLOW_DELETE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the deletion of `JourneyAction` records via the API.

---

## UserFeedback API Settings

### `JOURNEY_MAP_API_USER_FEEDBACK_SERIALIZER_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Defines the serializer class for `UserFeedback` API responses.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_ORDERING_FIELDS`
**Type**: `List[str]`  

**Default**: `["created_at", "intensity", "is_positive"]`  

**Description**: Specifies fields for ordering results in the `UserFeedback` API.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_SEARCH_FIELDS`
**Type**: `List[str]`  

**Default**: `["feedback_text"]`  

**Description**: Defines fields that can be searched within the `UserFeedback` API.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_FILTERSET_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies the filter class for `UserFeedback` API responses.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_LIST`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables listing of `UserFeedback` resources via the API.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_RETRIEVE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows retrieving specific `UserFeedback` records through the API.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_CREATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the creation of new `UserFeedback` records via the API.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_UPDATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows updating existing `UserFeedback` records through the API.

---

### `JOURNEY_MAP_API_USER_FEEDBACK_ALLOW_DELETE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the deletion of `UserFeedback` records via the API.

---

## PainPoint API Settings

### `JOURNEY_MAP_API_PAIN_POINT_SERIALIZER_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Defines the serializer class for `PainPoint` API responses.

---

### `JOURNEY_MAP_API_PAIN_POINT_ORDERING_FIELDS`
**Type**: `List[str]`  

**Default**: `["severity"]`  

**Description**: Specifies fields for ordering results in the `PainPoint` API.

---

### `JOURNEY_MAP_API_PAIN_POINT_SEARCH_FIELDS`
**Type**: `List[str]`  

**Default**: `["description"]`  

**Description**: Defines fields that can be searched within the `PainPoint` API.

---

### `JOURNEY_MAP_API_PAIN_POINT_FILTERSET_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies the filter class for `PainPoint` API responses.

---

### `JOURNEY_MAP_API_PAIN_POINT_ALLOW_LIST`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables listing of `PainPoint` resources via the API.

---

### `JOURNEY_MAP_API_PAIN_POINT_ALLOW_RETRIEVE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows retrieving specific `PainPoint` records through the API.

---

### `JOURNEY_MAP_API_PAIN_POINT_ALLOW_CREATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the creation of new `PainPoint` records via the API.

---

### `JOURNEY_MAP_API_PAIN_POINT_ALLOW_UPDATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows updating existing `PainPoint` records through the API.

---

### `JOURNEY_MAP_API_PAIN_POINT_ALLOW_DELETE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the deletion of `PainPoint` records via the API.

---

## Opportunity API Settings

### `JOURNEY_MAP_API_OPPORTUNITY_SERIALIZER_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Defines the serializer class for `Opportunity` API responses.

---

### `JOURNEY_MAP_API_OPPORTUNITY_ORDERING_FIELDS`
**Type**: `List[str]`  

**Default**: `["action__order"]`  

**Description**: Specifies fields for ordering results in the `Opportunity` API.

---

### `JOURNEY_MAP_API_OPPORTUNITY_SEARCH_FIELDS`
**Type**: `List[str]`  

**Default**: `["description"]`  

**Description**: Defines fields that can be searched within the `Opportunity` API.

---

### `JOURNEY_MAP_API_OPPORTUNITY_FILTERSET_CLASS`
**Type**: `Optional[str]`  

**Default**: `None`  

**Description**: Specifies the filter class for `Opportunity` API responses.

---

### `JOURNEY_MAP_API_OPPORTUNITY_ALLOW_LIST`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables listing of `Opportunity` resources via the API.

---

### `JOURNEY_MAP_API_OPPORTUNITY_ALLOW_RETRIEVE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows retrieving specific `Opportunity` records through the API.

---

### `JOURNEY_MAP_API_OPPORTUNITY_ALLOW_CREATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the creation of new `Opportunity` records via the API.

---

### `JOURNEY_MAP_API_OPPORTUNITY_ALLOW_UPDATE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Allows updating existing `Opportunity` records through the API.

---

### `JOURNEY_MAP_API_OPPORTUNITY_ALLOW_DELETE`
**Type**: `bool`  

**Default**: `True`  

**Description**: Enables or disables the deletion of `Opportunity` records via the API.

---

## Template View Settings

### `JOURNEY_MAP_VIEW_PERMISSION_CLASS`
**Type**: `Optional[str]`  

**Default**: `"journey_map.permissions.IsAuthenticated"`

**Description**: Specifies the permission class for `JourneyMapListView` and `JourneyMapDetailView`. Supports package-specific permissions (`IsAuthenticated`, `IsAdminUser`, `IsSuperUser`, `AllowAny`) or DRF-style permissions with a `has_permission` method. Customize to control access to template views.

---

This overview should help you understand and customize the settings for the `dj-user-behavior` package as needed.

---

### UserJourney ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `UserJourneyViewSet`:

- **`id`**: Unique identifier of the user journey (orderable, filterable).  
  - **Description**: An integer primary key for the journey record (e.g., `1`).
- **`name`**: The name of the user journey (orderable, searchable, filterable).  
  - **Description**: A string representing the journey’s title (e.g., `"New User Onboarding"`).
- **`description`**: A detailed description of the journey (searchable, filterable).  
  - **Description**: A text field providing context for the journey, nullable (e.g., `"Journey for new customer onboarding"` or `null`).
- **`persona`**: The associated user persona (searchable via `persona__name`, filterable).  
  - **Description**: A foreign key to `UserPersona`, searchable by persona name (e.g., `"Sarah the Project Manager"`), nullable.
- **`created_at`**: The timestamp when the journey was created (orderable, filterable).  
  - **Description**: A datetime marking the creation time (e.g., `"2025-04-24T10:00:00+00:00"`).
- **`updated_at`**: The timestamp when the journey was last updated (orderable, filterable).  
  - **Description**: A datetime marking the last modification time (e.g., `"2025-04-24T12:00:00+00:00"`).

---

### JourneyStage ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `JourneyStageViewSet`:

- **`id`**: Unique identifier of the journey stage (orderable, filterable).  
  - **Description**: An integer primary key for the stage record (e.g., `1`).
- **`journey`**: The associated user journey (searchable via `journey__name`, filterable).  
  - **Description**: A foreign key to `UserJourney`, searchable by journey name (e.g., `"New User Onboarding"`).
- **`stage_name`**: The name of the stage (orderable, searchable, filterable).  
  - **Description**: A string representing the stage’s title (e.g., `"Sign-up"`).
- **`order`**: The position of the stage in the journey sequence (orderable, filterable).  
  - **Description**: A positive integer indicating the stage’s order (e.g., `1`).

---

### JourneyAction ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `JourneyActionViewSet`:

- **`id`**: Unique identifier of the journey action (orderable, filterable).  
  - **Description**: An integer primary key for the action record (e.g., `1`).
- **`stage`**: The associated journey stage (searchable via `stage__stage_name`, filterable).  
  - **Description**: A foreign key to `JourneyStage`, searchable by stage name (e.g., `"Sign-up"`).
- **`action_description`**: A description of the user’s action (searchable, filterable).  
  - **Description**: A text field detailing the action (e.g., `"Complete registration form"`).
- **`touchpoint`**: The point of interaction (searchable, filterable).  
  - **Description**: A string identifying the interaction point, nullable (e.g., `"Website"` or `null`).
- **`order`**: The position of the action in the stage sequence (orderable, filterable).  
  - **Description**: A positive integer indicating the action’s order (e.g., `1`).

---

### UserFeedback ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `UserFeedbackViewSet`:

- **`id`**: Unique identifier of the user feedback (orderable, filterable).  
  - **Description**: An integer primary key for the feedback record (e.g., `1`).
- **`action`**: The associated journey action (searchable via `action__action_description`, filterable).  
  - **Description**: A foreign key to `JourneyAction`, searchable by action description (e.g., `"Complete registration form"`).
- **`feedback_text`**: The user’s feedback or emotional description (searchable, filterable).  
  - **Description**: A text field capturing the feedback (e.g., `"Form was easy to use"`).
- **`emotion`**: The user’s emotional state (orderable, filterable).  
  - **Description**: A string from `EmotionChoices` (e.g., `"Happy"`, `"Frustrated"`).
- **`intensity`**: The strength of the emotion (orderable, filterable).  
  - **Description**: An integer on a 1-5 scale (e.g., `4`).
- **`is_positive`**: Indicates if the feedback is positive or negative (orderable, filterable).  
  - **Description**: A boolean value (e.g., `True` for positive, `False` for negative).
- **`created_at`**: The timestamp when the feedback was created (orderable, filterable).  
  - **Description**: A datetime marking the creation time (e.g., `"2025-04-24T10:30:00+00:00"`).

---

### PainPoint ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `PainPointViewSet`:

- **`id`**: Unique identifier of the pain point (orderable, filterable).  
  - **Description**: An integer primary key for the pain point record (e.g., `1`).
- **`action`**: The associated journey action (searchable via `action__action_description`, filterable).  
  - **Description**: A foreign key to `JourneyAction`, searchable by action description (e.g., `"Complete registration form"`).
- **`description`**: A description of the issue (searchable, filterable).  
  - **Description**: A text field detailing the pain point (e.g., `"Unclear error message"`).
- **`severity`**: The severity of the pain point (orderable, filterable).  
  - **Description**: An integer on a 1-5 scale (e.g., `3`).

---

### Opportunity ViewSet - All Available Fields

These are all fields available for ordering, filtering, and searching in the `OpportunityViewSet`:

- **`id`**: Unique identifier of the opportunity (orderable, filterable).  
  - **Description**: An integer primary key for the opportunity record (e.g., `1`).
- **`action`**: The associated journey action (searchable via `action__action_description`, filterable, orderable via `action__order`).  
  - **Description**: A foreign key to `JourneyAction`, searchable by action description (e.g., `"Complete registration form"`) and orderable by action order.
- **`description`**: A description of the suggested improvement (searchable, filterable).  
  - **Description**: A text field detailing the opportunity (e.g., `"Add tooltips for form fields"`).

----

# Conclusion

We hope this documentation has provided a comprehensive guide to using and understanding the `dj-userjourey-map`.

### Final Notes:

- **Version Compatibility**: Ensure your project meets the compatibility requirements for both Django and Python
  versions.
- **API Integration**: The package is designed for flexibility, allowing you to customize many features based on your
  application's needs.
- **Contributions**: Contributions are welcome! Feel free to check out the [Contributing guide](CONTRIBUTING.md) for
  more details.

If you encounter any issues or have feedback, please reach out via
our [GitHub Issues page](https://github.com/lazarus-org/dj-userjourney-map/issues).
