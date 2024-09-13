# Django REST Framework Project with Channels, PostgreSQL, Redis, and Docker

## Project Overview

This project aims to develop an online tutoring platform using Django, Django Rest Framework, Channels for real-time communication, PostgreSQL for database management, Redis for storing chat history, and Docker for containerization. The platform will facilitate interactions between tutors and students, allowing them to manage profiles, schedule sessions, provide reviews, and engage in real-time chat.

## Features

### User Management

- **Registration:** Users can register for an account with the platform.
- **Authentication:** Secure authentication mechanisms for user logins.
- **Profile Management:** Users can create and manage their profiles, including personal information, profile picture, etc.
- **Role-Based Access Control:** Different access levels based on user roles, such as students and tutors.

### Tutoring Features

- **Tutor Search:** Users can search for tutors based on various criteria like subject, location, hourly rate, etc.
- **Session Scheduling:** Users can schedule tutoring sessions with available tutors.
- **Availability Management:** Tutors can set their availability schedules, and users can view and book sessions accordingly.
- **Review System:** Users can rate and review tutors based on their experiences.
- **Real-Time Notifications:** Users receive real-time notifications for session bookings, cancellations, and changes to tutor availability.
- **Reservation System:** Users can reserve tutoring lessons, which are confirmed through a seamless booking process.
- **Announcements for Tutors:** Tutors receive announcements regarding platform updates, important notices, and upcoming features.

### Real-Time Communication

- **Private Chats:** Users and tutors can engage in real-time private chats for discussing session details, asking questions, etc.
- **Chat History:** Integration with Redis to store chat history, ensuring seamless communication even after sessions.
- **Real-Time Notifications:** Users and tutors receive notifications for new messages and important updates in real-time.

### Security

- **Email Confirmation:** Users receive email confirmations for successful registration.
- **Password Reset:** Users can reset their passwords via email if forgotten.
- **OAuth2 Google Support:** Integration with OAuth2 for Google to streamline authentication and support user login issues.

## Frontend Integration

This project's frontend is built using Next.js and React and is available at [https://github.com/ProOnDesk/nauczajka-front](https://github.com/ProOnDesk/nauczajka-front). The backend will provide RESTful APIs and Websockets endpoints, enabling seamless communication and integration with the Next.js frontend.
