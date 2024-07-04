# Part 2: Queries with GraphQL

**Summary of Part 1**
In the previous part, we created a simple Django project with a books application, set up a model with title and author fields, configured a GraphQL schema to query book data, and populated the database with sample data. We then tested the GraphQL endpoint to make sure it was working correctly.

[Creating a Simple Django Project with GraphQL](https://github.com/nimodb/SimpleDjangoProjectWithGraphQL.git)

## Step 1: Clone the repository
```bash
git clone https://github.com/nimodb/QueriesWithGraphQL_Part2
cd QueriesWithGraphQL_Part2
```

## Step 2: Set Up Virtual Environment and Install Packages
First, create a virtual environment and install the necessary packages.
```bash
# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows
env\Scripts\activate

# On macOS/Linux
source env/bin/activate

# Install the required packages:
pip install -r requirements.txt
```

## Step 3: Create New Django App
Start the second part by creating a new app called `quiz`:
```bash
python manage.py startapp quiz
```