# Training Management System

A web-based Training Management System built with Django.

## Overview

This project is a Training Management System designed to manage courses, materials, and user profiles. It utilizes Django for the backend and integrates HTMX and Tailwind CSS to create a dynamic and responsive user interface.

## Features

- **User Authentication**: Custom user model supporting different user types (admin, trainer, trainee).
- **Course Management**: Create, update, and view courses and materials.
- **Enrollment System**: Trainees can enroll in courses.
- **Profile Management**: Users can view and edit their profiles.
- **Responsive UI**: Built with Tailwind CSS for styling and HTMX for dynamic interactions.

## Technologies Used

- **Backend**: Django framework
- **Frontend**: HTMX, Tailwind CSS
- **Database**: SQLite (default Django database)
- **Templating**: Django Templates with reusable components

## Project Structure

- `accounts/`: Handles user authentication and profiles.
- `courses/`: Manages courses and materials.
- `templates/`: Contains base templates and components.
- `static/`: Static files including CSS and JavaScript.


====================== 

# User Stories

## Authentication & User Management
- As a user, I want to register an account so that I can access the system
- As a user, I want to log in with my credentials so that I can access my personalized content
- As a user, I want to view and edit my profile information so that I can keep my details up to date

## Course Management
- As a participant, I want to browse available courses so that I can find training opportunities
- As a participant, I want to enroll in courses so that I can attend training sessions
- As a trainer, I want to create and manage courses so that I can organize training sessions
- As an admin, I want to manage course capacities so that classes don't get overbooked

## Training Sessions
- As a trainer, I want to create training sessions so that I can schedule classes 
- As a participant, I want to view my enrolled sessions so that I can attend them
- As a participant, I want to mark my attendance for sessions so that my participation is recorded
- As a participant, I want to provide evaluation feedback so that I can rate the training quality

## Admin Dashboard 
- As an admin, I want to view system statistics so that I can monitor training activities
- As an admin, I want to manage users so that I can assign appropriate roles
- As an admin, I want to view attendance reports so that I can track participation
- As an admin, I want to see evaluation ratings so that I can assess training effectiveness