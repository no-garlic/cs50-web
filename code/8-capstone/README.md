![Image](quizly/static/quizly/image/quizly.jpeg)

# Quizly - Interactive Quiz Platform
Quizly is a web application that allows users to create, attempt, and share quizzes. The platform offers a wide range of features including creating and attempting quizzes, semantic search, ratings, personalized profiles, and leaderboards. Built with Django on the backend and HTML / CSS / JavaScript on the frontend, it provides a responsive and intuitive user interface that works seamlessly across devices.

## Distinctiveness and Complexity
Quizly stands apart from other projects in the CS50 Web course in several significant ways:

### Backend Architecture
The project implements a multi-model database schema with 8 interconnected Django models (User, Category, Quiz, Question, QuizAttempt, Answer, QuizRating, and SavedForLater). This  data structure enables numerous relationships between entities, allowing for more features than were present in the other course projects.

### Semantic Search
A standout feature of Quizly is its semantic search functionality, which I implemented using FAISS and sentence transformers. Unlike simple keyword matching, this system allows users to find quizzes based on semantic meaning:

- The application creates vector embeddings for quizzes using sentence transformers
- These embeddings are indexed in a FAISS database for efficient similarity searching
- Background loading and thread synchronization is used to load the model and index file, to ensure the user is never blocked waiting for a few seconds.
- The semantic search index is updated and saved to disk after a new quiz is created, to ensure consistency between the SQL database and the FAISS index.
- Search results are ranked by relevance based on cosine similarity

This implementation goes far beyond simple database queries used in previous projects, and represents a more modern approach to search functionality in web applications.

### Advanced Frontend Architecture
The frontend is a more sophisticated than other projects, and includes a lot more emphasis on JavaScript and CSS:

- A lot of effort was spent on the CSS, to make the application look and feel modern.
- Implementation of custom UI components like a star rating system and custom radio buttons, all controlled through javascript.
- Comprehensive CSS variable system for consistent theming across all pages.
- Incorporated external assets through stylesheets, such as google fonts and bootstrap icons.

As you can see from the page navigation diagram below, there is a lot of interconnectivity between the pages, making the navigation user experience very intuative.

![Image](quizly/static/quizly/image/navigation.jpeg)


### Responsive UI/UX Design
The application features a complete responsive design system, with careful consideration for different screen sizes:

- Mobile-first approach with support for different device sizes on every page.
- Collapsible sidebar that transforms based on screen width and shows icons only on small screen sizes
- Fluid grid layouts for quiz and category listings that automatically adjust to available space
- Column hiding in tables as the screen width is reduced
- Touch-friendly interactive elements


### Asynchronous Data Processing
The application uses several asynchronous processes to improve user experience:

- AJAX-based rating and saving functionalities that don't require page reloads
- Background loading of the sentence transformers model and FAISS search index to prevent blocking the main application
- Synchronization mechanisms to handle concurrent access to shared resources

### Data Generation and Seeding
To provide a realistic user experience, I wrote a data generation system that created a production quantity of test-data content so the application can be fully experienced.

- Quiz and question generation for creating realistic test data
- Multi-step migrations to seed the database with diverse categories, quizzes, users, and quiz attempt history


## Core Functionality
- **Quiz Creation**: Users can create quizzes by first selecting a category and entering a quiz name and theme, and then adding multiple questions and answers to their quiz.
- **Quiz Taking**: Users can attempt quizzes, receive scores, and see hints for their incorrect answers to assist them if they choose to retry the quiz.
- **Leaderboards**: Each quiz has a leaderboard where you can compare your best score against everyone else.
- **Browse**: A browse option is available filter by category, and then browse the quizzes within that category.
- **Search**: Both semantic and keyword search options are available for finding quizzes.
- **User Profiles**: Each user has a profile page showing their quiz history and saved-for-later quizzes. User profiles are public and can be browsed by other users.
- **Ratings**: Users can rate quizzes on a 5-star scale, and see an average rating of each quiz across all users.
- **Save For Later**: Users can bookmark quizzes to attempt later, and see a list of all of their bookmarked quizzes.


## File Structure and Description

### Django Models (models.py)
- I defined 8 interconnected models (User, Category, Quiz, Question, QuizRating, QuizAttempt, Answer, SavedForLater)
- Included a number of methods for calculating quiz statistics, leaderboards, average ratings across all users, and user progress.
- Fully fleshed out and customized admin interface.

Below is the database schema for the application.

![Image](quizly/static/quizly/image/schema.jpeg)

### Views
I split the views into multiple files to reduce complexity:
- **account.py**: Performs user authentication (login, logout, registration)
- **browse.py**: Manages category browsing and quiz listing
- **create.py**: Controls quiz and question creation
- **profile.py**: Manages user profile display with previous attempts and quizzes saved for later
- **quiz.py**: Handles quiz viewing, attempts, leaderboards, ratings, and saving for later
- **search.py**: Implements both keyword and semantic search functionality

### Services
- **faiss_search_service.py**: Implements vector embeddings and similarity search using FAISS and sentence transformers
- Includes background loading and thread synchronization for performance optimization

### Migrations and Data Generation
I consolidated the models to a single schema migration, followed by 6 hand crafted migrations for procedully adding a high volume of test data.
- **generate_quizzes.py**: Quiz generation script for generating the test data json files (one-off process), that are later used during the migrations to seed the database.
- **build_faiss_index.py**: Creates the vector embeddings and FAISS index for semantic search as the last step of the migration, to ensure that once the migration is done all setup steps are complete and the application can be started and used with no further steps.

### Templates
- **layout.html**: Base template with a responsive sidebar
- **index.html**: Landing page with feature highlights for the application
- **list.html**: Displays quizzes or categories in a grid layout, and search capability
- **quiz.html**: Shows quiz details, attempts, and ratings
- **attempt.html**: Interface for taking quizzes and viewing results
- **create.html**: Form for creating quizzes and questions
- **profile.html**: User profile with quiz history
- **register.html** and **login.html**: Authentication forms

### Static Files

- CSS:
  - **global-variables.css**: Defines theme colors, spacing, and fonts used by all other pages and stylesheets
  - **styles.css**: Base styles for the application, used by all pages
  - **bootstrap-overrides.css**: Overrides for bootstrap to set specific theme colors and styles
  - Custom stylesheets for each page of the web app (**account.css, attempt.css, create.css, index.css, list.css, profile.css, and quiz.css**)

- JavaScript:
  - **quiz.js**: Handles quiz interactions, ratings, and saving
  - **attempt.js**: Manages quiz attempts and answer selection
  - **create.js**: Controls quiz creation interface
  - **list.js**: Manages the search interface
  - **index.js**: Handles the landing page interactions

## How to Run the Application

### Prerequisites
- Python 3.12.9 or higher
- Pip package manager
- Virtual environment or Conda

### Installation
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   python manage.py runserver
   ```

4. Access the application at `http://127.0.0.1:8000`

### Default Users
The application comes with several pre-created users for testing. New users can be created through the Register User function of the app. To access the admin interface, login with the admin user:
- Username: `admin`, Password: `admin`


