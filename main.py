from typing import Union
from fastapi.templating import Jinja2Templates

from fastapi import FastAPI, Request

app = FastAPI()

templates = Jinja2Templates(directory="templates")

"""
Displays the dashboard for the homepage
"""

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "somevar": 3
    } )

    """creates a stock and stores it in the database

    Returns:
        string: stock
    """

@app.post("/stock")
def create_stock():
    return {
        "code":"success",
        "message":"Stock Created"
    }

