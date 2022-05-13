# Chest-XRay-Detection

# Kaggle Dataset

 - pip install kaggle

In order to get the pneumonia dataset, you need to authenticate your account with Kaggle's public API.
 - From the website, click on your user profile and select "My account"
 - Scroll to the page labeled API and select "Create New API Token"
 - Find the path to your /.kaggle directory, and put the new kaggle.json file in there
    (for me it was C:/Users/cpshan/.kaggle/)

Once you're authenticated, call:
 - kaggle datasets download -d paultimothymooney/chest-xray-pneumonia
 - unzip this once it's done downloading
 - MAKE SURE THE UNZIPPED FOLDER IS NAMED chest-xray-pneumonia