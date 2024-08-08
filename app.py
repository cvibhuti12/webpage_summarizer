import traceback
from time import strftime
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from config.cfg_handler import CfgHandler
from config.cfg_utils import fetch_base_url
from framework.justext.core import justextHTML
from framework.parser.parser import Parser
from implementation import word_frequency_summarize_parser

#initialize fastapi
app = FastAPI()

#RESTservice

#handle undefined routes
@app.exception_handler(404)
def not_found(request: Request,error):
    return JSONResponse(status_code=404, content={"error": str(error)})

@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        print(f'{ts} {request.client.host} {request.method} {request.url.scheme} {request.url.path} {response.status_code}')
    return response

@app.exception_handler(Exception)
async def handle_exception(request: Request, exc: Exception):
    """ Handle and return a JSON response for exceptions. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    print(f'{ts} {request.client.host} {request.method} {request.url.scheme} {request.url.path} ERROR:{exc} \n{tb}')
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)}
    )
    
@app.get("/", response_class=HTMLResponse)
async def index():
    base_url = fetch_base_url(CfgHandler())
    with open("templates/index.html") as f:
        content = f.read()
    content = content.replace("{{ base_url }}", base_url)
    return HTMLResponse(content=content)

# Summarize endpoint
@app.get("/v1/summarize")
async def summarize(url: str = Query(..., description="URL to summarize")):
    if not url:
        raise HTTPException(status_code=400, detail="Bad Request: `url` is empty")

    summary = ""

    try:
        # Fetch web content
        web_text = justextHTML(html_text=None, web_url=url)

        # Parse it via parser
        parser = Parser()
        parser.feed(web_text)

        # summary = facebook_parser_word_frequency_summarize.run_summarization(parser.paragraphs)
        summary = word_frequency_summarize_parser.run_summarization(parser.paragraphs)

    except Exception as ex:
        print(f'summarize(): error while summarizing: {ex}\n{traceback.format_exc()}')
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return JSONResponse(content={'summary': summary})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000, reload=True)