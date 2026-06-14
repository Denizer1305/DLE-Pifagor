<!-- DLE-Pifagor Documentation Header -->
<p align="center">
  <a href="../../README.md"><img src="../../design/logos/main/pifagor-logo-primary.svg" alt="DLE-Pifagor" width="96" /></a>
</p>

<p align="center">
  <a href="../../docs/README.md">Документация</a> ·
  <a href="../../docs/README.en.md">English version</a> ·
  <a href="../../README.md">README проекта</a>
</p>

---
<!-- /DLE-Pifagor Documentation Header -->
# Database Schema

## Общий подход

База данных ЦОС «Пифагор» строится вокруг образовательной организации, пользователей, ролей, курсов, уроков, заданий, журнала и расписания.

Основная БД: **PostgreSQL**.

---

## Главные сущности

```text
User
Role
Organization
StudyGroup
Course
Lesson
Assignment
Submission
Grade
ScheduleItem
Material
Notification
AnalyticsSnapshot
```

---

## Пользователи и роли

### User

Базовая учётная запись пользователя.

Поля: `id`, `email`, `phone`, `first_name`, `last_name`, `middle_name`, `avatar`, `is_active`, `created_at`, `updated_at`.

### Role

Роль в системе: `student`, `parent`, `teacher`, `curator`, `methodist`, `organizer`, `mentor`, `director`, `admin`, `superadmin`.

### UserRole

Связь пользователя, роли и организации. Один пользователь может иметь несколько ролей.

---

## Организации

### Organization

Образовательная организация.

Поля: `name`, `short_name`, `type`, `description`, `address`, `logo`, `is_active`.

### AcademicYear

Учебный год: `organization`, `name`, `start_date`, `end_date`, `is_current`.

### AcademicPeriod

Четверть, семестр или модуль: `academic_year`, `name`, `start_date`, `end_date`, `type`.

### StudyGroup

Класс или учебная группа: `organization`, `name`, `education_level`, `grade_level`, `curator`, `academic_year`.

---

## Профили

### StudentProfile

Профиль учащегося: `user`, `organization`, `group`, `grade_level`, `enrollment_date`, `status`.

### ParentProfile

Профиль родителя: `user`, `organization`, `children`.

### TeacherProfile

Профиль преподавателя: `user`, `organization`, `position`, `subjects`, `employment_status`.

---

## Курсы и уроки

### Course

Курс или дисциплина: `organization`, `subject`, `title`, `description`, `education_level`, `grade_level`, `owner`, `status`, `created_at`.

### CourseEnrollment

Зачисление учащегося на курс: `course`, `student`, `status`, `progress_percent`, `enrolled_at`.

### Lesson

Урок: `course`, `title`, `topic`, `description`, `lesson_type`, `date`, `order`, `status`, `created_by`.

### LessonBlock

Блок урока: `lesson`, `type`, `title`, `content`, `order`.

---

## Задания и сдачи

### Assignment

Задание: `course`, `lesson`, `title`, `description`, `assignment_type`, `deadline`, `max_score`, `status`, `created_by`.

### Submission

Сданная работа: `assignment`, `student`, `content`, `status`, `submitted_at`, `reviewed_at`, `score`, `reviewer`.

### SubmissionReview

Проверка работы: `submission`, `reviewer`, `score`, `comment`, `status`, `created_at`.

---

## Журнал

### Grade

Оценка: `student`, `course`, `lesson`, `assignment`, `teacher`, `value`, `score`, `max_score`, `category`, `comment`, `created_at`.

### AttendanceMark

Посещаемость: `student`, `lesson`, `status`, `comment`.

### GradeHistory

История изменения оценки.

---

## Расписание

### Classroom

Кабинет: `organization`, `name`, `capacity`, `location`.

### TimeSlot

Временной слот: `organization`, `start_time`, `end_time`, `order`.

### ScheduleItem

Запись расписания: `organization`, `group`, `course`, `lesson`, `teacher`, `classroom`, `date`, `start_time`, `end_time`, `status`.

---

## Главные связи

```text
Organization → StudyGroup → StudentProfile
Organization → TeacherProfile
TeacherProfile → Course
Course → Lesson
Lesson → Assignment
Assignment → Submission
Submission → Grade
Lesson → AttendanceMark
Group → ScheduleItem
User → Notification
User → AIConversation
StudentProfile → Portfolio
```

---

## Принцип проектирования схемы

База данных должна быть нормализована, но не чрезмерно усложнена. Главный вопрос при добавлении таблицы: эта сущность действительно самостоятельная или это поле уже существующей сущности?

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
