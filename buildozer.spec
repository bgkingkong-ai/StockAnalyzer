name: Build Android APK

on:
  push:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout Code
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Install Dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y build-essential libffi-dev python3-dev ccache git libssl-dev
        pip install --upgrade pip
        pip install buildozer kivy kivymd

    - name: Build APK
      run: |
        yes | buildozer -v android debug

    - name: Upload APK Artifact
      uses: actions/upload-artifact@v4
      with:
        name: StockAnalyzer-APK
        path: bin/*.apk
