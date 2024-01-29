# Timeline

## Table of Contents
- [Description](#description)
- [Design and Structure](#design-and-structure)
  - [Home Page ('index.html')](#home-page-indexhtml)
  - [Layout ('layout.html')](#layout-layouthtml)
  - [Archived ('archived.html')](#archived-archivedhtml)
  - [Login ('login.html')](#login-loginhtml)
  - [Manage Project ('manage_project.html')](#manage-project-manage_projecthtml)
  - [Projects ('project.html')](#projects-projecthtml)
  - [Register ('register.html')](#register-registerhtml)
- [Functionality](#functionality)
  - [Framework](#framework)
  - [Static Files](#static-files)
    - [Script.js](#scriptjs)
    - [styles.css](#stylescss)
  - [CDN Scripts & Styles](#cdn-scripts--styles)
  - [Other Interest Archives](#other-interest-archives)
    - [forms.py](#formspy)
    - [models.py](#modelspy)
- [How to run](#how-to-run)
- [Security](#security)
- [License](#license)

## Description
Timeline is an application designed to create calendars for individual projects. Projects can be of any type, as they all specify a title, description, start date, and end date. The calendar is rendered based on the date range of the created project. Within the calendar, events or tasks can be created for both date ranges and specific times on particular dates. All events are editable and can be moved using the mouse. The project uses Bootstrap to incorporate all the design elements, making it adaptable to mobile screens. Additionally, the menus have been adjusted for smaller screens using the collapsible hamburger menu.

## Design and Structure
### Home Page ('index.html'):
- It's the landing page of the application, the first one users see when visiting the website. 
- It has a submenu that displays links with JavaScript scroll functionality to the lower texts within the page's body. 
- On smaller screens, it features a hamburger menu.

### Layout ('layout.html'):
- It's the page that serves as the foundation to extend the rendering of the other HTML pages.
- It integrates the main menu and the footer.
- It loads the static files and the CDNs.
- It includes a hamburger menu for small screens.

### Archived ('archived.html'):
- It's the page that integrates archived projects.
- It uses pagination.
- It has a search bar and a dropdown menu to sort projects by date or name.
- It is used to view archived projects, allowing them to be unarchived or deleted.

### Login ('login.html'):
- Login page.
- It's use a form login.

### Manage Project ('manage_project.html'):
- It's the page that integrates the calendar.
- Here, events are created, edited, and deleted.
- On this page, the project's timeline can be managed.
- This page integrates the styles and JavaScript to manage the calendar.

### Projects ('project.html'):
- It's the home page after signing up or logging in.
- Displays active projects.
- Allows the creation of projects through a Django form.
- Enables archiving or deleting projects.
- Includes a search bar and a dropdown menu for filtering by name or dates.
- Integrates pagination.

### Register ('register.html'):
- Register page.
- Includes a register form.

## Functionality
### Framework
- [Django 5.0](https://docs.djangoproject.com/en/5.0/).

### Static Files
#### Script.js:
- Includes the JavaScript functions for the application apart from the calendar.
- Integrates functions to create, edit, delete, and archive projects.
- Incorporates a function to capture the CSRF token.

#### styles.css:
- Contains the styles of the application apart from the calendar styles.

### CDN Scripts & Styles
- The files loaded via CDN are located on the layout.html page.
- It loads [Bootstrap](https://getbootstrap.com/), [Fullcalendar](https://fullcalendar.io/), and JavaScript files.

### Other Interest Archives
#### forms.py:
- Contains the form to create and edit a project.

#### models.py:
- Contains three models. One for user, one for project and one for event.

## How to run
1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Create a virtual environment and activate it.
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   .\venv\Scripts\activate   # For Windows
4. Install the project dependencies.
    pip install -r requirements.txt
5. Apply database migrations.
    python manage.py migrate
6. Run the development server.
    python manage.py runserver

## Security
- Integrating all the security measures of the Django 5.0 framework, including session security keys and CSRF tokens. 
- Change DB keys for use.

## License
This project is licensed under the terms of the Django License and the FullCalendar License. Use of this project for commercial purposes is subject to the terms of these licenses.

## Additional Links
- [Django Framework](https://www.djangoproject.com/) - Django web framework.
- [Django Rest Framework](https://www.django-rest-framework.org/) - Django toolkit for building Web APIs.
- [FullCalendar](https://fullcalendar.io/) - Full-sized drag & drop event calendar.
- [Bootstrap](https://getbootstrap.com/) - Front-end component library.
- [GitHub Repository](https://github.com/Merkuryo/timeline) - Explore the source code on GitHub.
