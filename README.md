
# Web Remembrance Agent

This project is a lightweight web archiver which archives every webpage you visit on Mozilla Firefox.

- YouTube videos are archived as their subtitle files
- Generic websites are archived as Markdown

## Documentation
### System Diagram
```
┌────────────┐
│    Clio    │
│  (Firefox  │
│ Extension) │
└──────┬─────┘
       │
  sends URLs
       │
┌──────▼──────┐
│   Archiver  │
│ (Flask App) │
└──────┬──────┘
       │
  archives URL
  as file
       │
  ┌────▼────┐
  │ Archive │
  └─────────┘
```

## Setup
1. Download this repository
2. Create a virtual environment
    - `python -m venv .venv`
3. Activate the virtual environment
    - `.\.venv\Scripts\activate`
4. Install the requirements
    - `pip install -r requirements.txt`

## Deployment
This project consists of two components:
1. **Clio**, the Firefox extension which sends the URLs of the pages you visit to the Archiver web app
2. **Archiver**, the Flask app which archives the URLs that are passed to it.

Deployment requires 

### Deploying Archiver
1. Activate the virtual environment
    - `.\.venv\Scripts\activate`
2. Start the Flask app
    - `python .\app.py`

### Deploying Clio
1. Open Firefox
2. Navigate to `about:debugging#/runtime/this-firefox` (in the address bar)
3. Click "Load Temporary Add-on..."
4. Navigate to the location where you have installed this repository
5. Navigate to the subfolder "clio"
    - e.g. `C:\Documents\web-remembrance-agent\clio`
6. Double-click on the "manifest" file