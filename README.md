# Career Guidance Project

This project provides career guidance by suggesting suitable jobs based on the user's area of interest and current stage, along with personalized roadmaps to achieve those career goals.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/Jannudhanusha/Carrier-Guidance-with-AI.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Carrier-Guidance-with-AI
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up your OpenAI API key by creating a `.env` file in the project root directory and adding your key:

    ```bash
    OPENAI_API_KEY=your-api-key
    ```

5. Run the Streamlit app:

    ```bash
    streamlit run app.py
    ```

## Usage

Upon running the Streamlit app, you will be presented with a user interface where you can navigate through different pages:

- **Select Area of Interest**: Choose your area of interest from the provided options.
- **Select Job**: Once you've selected an area of interest, choose a specific job from the suggested list.
- **Current Stage Details**: Enter your current stage (e.g., High School, College) and generate a personalized roadmap to achieve the selected job.

## Contributing

Contributions are welcome! If you have any suggestions, enhancements, or bug fixes, feel free to open an issue or create a pull request.
