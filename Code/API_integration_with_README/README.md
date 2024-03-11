
First, create a virtual environment in the root of the folder and install the requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Place the random_forest_model.pkl file in the root of the folder.

To run the app, use the below command:
```bash
uvicorn main:app --reload
```

Then the project page would be hosted on http://localhost:8000
Copy this URL and paste it on a browser to view the site.