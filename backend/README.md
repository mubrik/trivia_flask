# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.


### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```
#### Set up your Enviroment Variables
- create a .env file in the backend root folder `./backend` with your database variables, example:
``` bash
DB_URI='postgresql://username:password@localhost:5432/trivia'
TEST_DB_URI='postgresql://username:password@localhost:5432/trivia_test'
```

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
python run.py
```

### Documentation

`Question object'`
- Instance showing the key value pair of a `Question`
```json
{
  "question": "1 + 1 = ?", 
  "answer": "2", 
  "category": 2, 
  "difficulty": 1
}
```

`Categories object'`
- Instance showing the key value pair of a `Question`
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/api/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with 3 keys, 
  1. `success` boolean value
  2. `categories` that contains an object of `id: category_string` key: value pairs 
  3. `total_categories` that contains total number of categories

```json
{
  "success": True,
  "categories": Categories,
  "total_categories": 6,
}
```

`GET '/api/questions'`

- Fetches a dictionary of categories in which exist questions array, categories and total questions count
- Request Arguments: None
- Returns: An object with 5 keys, 
  1. `success` boolean value
  2. `questions` that contains an array of questions
  3. `categories` that contains an object of `id: category_string` key: value pairs 
  4. `total_questions` that contains total number of questions
  4. `current_category` current category

```json
{
  "success": True,
  "questions": [Question, Question],
  "categories": Categories,
  "total_questions": 2,
  "current_category": 'Science',
}
```

`POST '/api/questions'`

- Creates a Question
- Request Arguments: Question JSON object, Note all fields are required
```json
{
  "question": "1 + 1 = ?", 
  "answer": "2", 
  "category": 2, 
  "difficulty": 1
}
```
- Returns: An object with 1 key, 
  1. `success` boolean value
  
`DELETE '/api/questions/<question_id>'`

- Deletes a Question from DB
- Request Arguments: question_id in url parameter
- Returns: An object with 2 keys, 
  1. `success` boolean value
  2. `id` id of item removed
```json
{
  "success": True,
  "id": question_id
}
```

`POST '/api/questions/search'`

- Fetches a list of questions matching the search term
- Request Arguments: Object with key `searchTerm` and string value
```json
{
  "searchTerm": "title",
}
```
- Returns: An object with 4 keys, 
  1. `success` boolean value
  2. `questions` that contains an array of questions
  3. `total_questions` that contains an object of `id: category_string` key: value pairs 
  4. `current_category` current category

```json
{
  "success": True,
  "questions": [Question, Question, Question],
  "total_questions": 3,
  "current_category": "Science"
}
```

`GET '/api/categories/<category_id>/questions'`

- Fetches a dictionary that contains questions in the specified category
- Request Arguments: category_id in url parameter
- Returns: An object with 3 keys, 
  1. `success` boolean value
  2. `questions` that contains an array of questions
  3. `total_questions` that contains total number of questions

```json
{
  "success": True,
  "questions": [Question],
  "total_questions": 1
}
```

`POST '/api/quizzes'`

- Fetches a list of questions matching the search term
- Request Arguments: Object with key `previous_questions` and value which is an arry of IDs to exclude, key `quiz_category`, category to exclude
- Note: To get from all categories, `quiz_category` object with a key `id` whose value = 0 is required
```json
{
  "previous_questions": [4],
  "quiz_category": {"id": 3, "type": "Geography"}
}
```
- Returns: An object with 4 keys, 
  1. `success` boolean value
  2. `question` the next question in specified category, this will return a False|Nullish value if no other question exists

```json
{
  "success": True,
  "question": Question | Null ,
}
```

`Error'`

- Error object form from bad api calls comes with message to detail error cause, example:
```json
{
  "success": False,
  "message": "Missing Field: Answer",
  "error": 405
}
```

## Testing

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
