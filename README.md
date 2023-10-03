# ai_dating_algorithm

## Description

AI Dating Algorithm is an AI-powered application that matches dating profiles based on user responses to a set of questions. It utilizes machine learning embeddings and PostgreSQL with the pgvector extension for efficient and accurate matchmaking.

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL
- pgvector PostgreSQL extension

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/ai_dating_algorithm.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd ai_dating_algorithm
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` file to store your OpenAI API key:**

    ```bash
    echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
    ```

5. **Setup PostgreSQL Database:**

    - Install PostgreSQL and create a new database.
    - Install the pgvector extension by running `CREATE EXTENSION IF NOT EXISTS pgvector;` in your PostgreSQL database.


## Usage

1. The program will prompt you to answer a series of questions.
2. Your answers will be combined and converted into an embedding using OpenAI's API.
3. The program will then query a PostgreSQL database to find the most similar profile based on the generated embedding.
4. The top match will be displayed.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)


