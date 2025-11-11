# Filtered PhD Courses Calendar

> Automatically generate a filtered `.ics` calendar from the official PhD courses schedule.  
> Only selected courses are included, and the calendar is kept up-to-date automatically via GitHub Actions.

---

## 🎯 Purpose

This repository allows you to subscribe to a **filtered version** of the PhD courses calendar, containing only the courses you care about, such as:

- A walkthrough on Generative AI  
- Data Visualization  
- Elements of Deep Learning  
- Machine Learning for Mobile Communication Systems  

Events containing undesired keywords (e.g., “Pillonetto”) are excluded.

---

## 🛠 Features

- Filters events based on keywords in **title, description, or location**.  
- Excludes unwanted events by specific keywords.  
- Generates a valid **iCalendar `.ics` file** compatible with Google Calendar, Apple Calendar, or Outlook.  
- Fully automated: updated daily via **GitHub Actions**.  
- API key for Google Calendar is kept private — never exposed in the repository.

---

## ⚡ Subscribe to the calendar

Once the workflow runs, the `.ics` file is publicly accessible. You can subscribe using:
https://raw.githubusercontent.com/edos08/phd-filtered-calendar/main/phd_filtered_calendar.ics