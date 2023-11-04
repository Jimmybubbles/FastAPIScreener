import models
import yfinance
from fastapi.templating import Jinja2Templates
from models import Stock
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from database import SessionLocal, engine
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


class StockRequest(BaseModel):
    symbol: str
    
def get_db():
    try:
        # create new db session
        db = SessionLocal()
        yield db
    finally:
        # close db session
        db.close()

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request
    } )

def fetch_stock_data(id: int):
    db = SessionLocal()
    stock = db.query(Stock).filter(Stock.id == id).first()
    
    yahoo_data = yfinance.Ticker(stock.symbol)
    
    stock.ma200 = yahoo_data.info['twoHundredDayAverage']
    stock.ma50 = yahoo_data.info['fiftyDayAverage']
    stock.price = yahoo_data.info['previousClose']
    stock.forward_pe = yahoo_data.info['forwardPE']
    stock.forward_eps = yahoo_data.info['forwardEps']
    stock.dividend_yield = yahoo_data.info['dividendYield'] * 100
    

    db.add(stock)
    db.commit()    

@app.post("/stock")
def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    
    stock = Stock()
    stock.symbol = stock_request.symbol
    
    db.add(stock)
    db.commit()
    
    background_tasks.add_task(fetch_stock_data, stock.id)
    
    return {
        "code":"success",
        "message":"Stock Created"
    }

