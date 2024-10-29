#regex patterns for user validation
username_pattern = r"^[a-zA-Z][a-zA-Z0-9_-]{2,14}$"
name_pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s.'-]+$"
email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
phone_pattern = r"^\+\d{7,15}$"
date_pattern = r"^\d{4}-\d{2}-\d{2}$"
password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"

#regex patterns for book addition/modification
title_pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s'-]+$"
author_pattern = r"^[A-Za-zÀ-ÖØ-öø-ÿ\s.'-]+$"
ISBN_pattern = r"^\d{1,20}$"
available_pattern = r"^\d+$"