This project aims to create an app that works as a dictionary for Japanese Words. I am currently studing this language and I wanted to have an app that tracks the words I learn.

The .apk files of the app will be published in the releases page eventually. But if you want to try it now, you can build it yourself using the steps below.

## How to build the app

# Building the Japanese Vocabulary App Manually

This guide will walk you through the process of building the Japanese Vocabulary app manually. This method is useful for development and testing purposes.

## Prerequisites

1. Python 3.7 or higher
2. Kivy framework
3. Git (optional, for cloning the repository)

## Steps

1. **Set up the environment:**
   
   Create a new directory for your project and set up a virtual environment:

   ```
   mkdir japanese_vocabulary_app
   cd japanese_vocabulary_app
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

2. **Install dependencies:**
   
   Install Kivy and other required packages:

   ```
   pip install kivy
   ```

3. **Get the source code:**
   
   Either clone the repository (if using Git):
   ```
   git clone https://github.com/your-repo/japanese-vocabulary-app.git
   cd japanese-vocabulary-app
   ```
   
   Or manually copy all the provided Python (.py) and Kivy (.kv) files into your project directory.

4. **Organize the project structure:**
   
   Ensure your project structure looks like this:
   ```
   japanese_vocabulary_app/
   ├── main.py
   ├── utilities.py
   ├── screens/
   │    └── all python files
   ├── kv/
   │    └── all kv files
   └── fonts/
       └── static/
           └── All needed fonts

   ```

5. **Run the app:**
   
   Execute the main.py file to run the app:

   ```
   python main.py
   ```

   This will launch the app in development mode on your local machine.

## Building for Android

To build the app for Android, you'll need to use Buildozer. Here are the steps:

1. Install Buildozer:
   ```
   pip install buildozer
   ```

2. Initialize Buildozer in your project directory:
   ```
   buildozer init
   ```

3. Edit the `buildozer.spec` file to match the provided configuration.

4. Build the Android APK:
   ```
   buildozer android debug
   ```

   This process may take a while as it downloads and sets up the Android SDK and NDK.

5. Once completed, you'll find the APK file in the `bin/` directory.

## Notes

- Make sure all the required files (Python scripts, Kivy files, fonts, etc.) are in the correct locations as specified in the project structure.
- The `words.json` and `tags.json` files will be created automatically when you first add words or tags in the app.
- For production releases, you may want to sign your APK. Refer to the Buildozer documentation for instructions on creating a signed APK.

By following these steps, you should be able to build and run the Japanese Vocabulary app manually on your local machine and create an Android APK for testing or distribution.

## How to build the app




