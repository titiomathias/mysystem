# My System

The aim is control my routing using XP to track my progress.


# Database Model
users
-----
- id (PK)
- username
- email (UNIQUE)
- password_hash
- level
- xp
- created_at


attributes
----------
- user_id (PK, FK -> users.id)
- cha
- wis
- int
- str
- agi
- con


tasks
-----
- id (PK)
- user_id (FK)
- name
- description
- category
- frequency ENUM('once', 'daily', 'weekly', 'habit')
- base_xp
- active BOOLEAN


task_attributes
---------------
- task_id (FK)
- attribute ENUM('cha','wis','int','str','agi','con')
- value INT


task_logs
---------
- id (PK)
- task_id (FK)
- user_id (FK)
- xp_earned
- completed_at
