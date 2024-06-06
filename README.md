![DALL·E 2024-06-07 00 32 13 - A minimalist graphic design of a tag with the text 'TagMeIfYouCan' in a simple, hand-drawn style  The tag is plain with a subtle shadow and placed on ](https://github.com/Hambbuk/TagMeIfYouCan/assets/51123268/5e4c7f2d-052c-4436-be61-c0e8baef9bc3)

# TagMeIfYouCan

**TagMeIfYouCan** is an open-source project designed for users to manually tag and classify images, enhancing data accuracy through human input. This project leverages the power of human intuition to build a reliable and precise dataset.

## Key Features
- **Manual Image Tagging:** Users can classify images as 'Flicker' or 'Non-Flicker'.
- **Dynamic Image Loading:** Efficiently loads a batch of images for user classification.
- **Data Aggregation:** Collects user-generated tags to create a comprehensive dataset.

## Tech Stack
- **Backend:** Flask, SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript

## Getting Started

Follow these instructions to set up the project locally.

### Prerequisites

Ensure you have the following installed:
- Python 3.6+
- Virtualenv

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/TagMeIfYouCan.git
    cd TagMeIfYouCan
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    ```bash
    flask db upgrade
    ```

5. **Run the application:**
    ```bash
    flask run
    ```

6. **Access the application:**
    Open your browser and go to `http://127.0.0.1:5000`

## Usage

1. **Start a Session:** Enter your user ID to begin tagging images.
2. **Tag Images:** Navigate through images and tag them as 'Flicker' or 'Non-Flicker'.
3. **Review Status:** Monitor your tagging progress and overall dataset status.

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and push your branch to your fork.
4. Submit a pull request detailing your changes.

Please ensure all changes are covered by tests where applicable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

We appreciate all contributors and maintainers who have dedicated their time to improve this project.

---

By contributing to this project, you agree to abide by the [code of conduct](CODE_OF_CONDUCT.md).
