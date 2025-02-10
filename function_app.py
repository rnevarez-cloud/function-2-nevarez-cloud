import azure.functions as func
import logging
import datetime
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="get_scores")
@app.route(route="scores")
@app.cosmos_db_input(arg_name="inputDocument", 
                     database_name="game_scores", 
                     container_name="scores_container",
                     connection="CosmosDbConnectionSetting")

def get_scores(inputDocument: func.DocumentList,
                req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    scores = []
    for d in inputDocument:
        scores.append(d.to_dict())

    date = req.params.get('date')
    if not date:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            date = req_body.get('date')

    if not date:
        date = str(datetime.date.today())

    date_scores = list(filter(lambda x: x['date'] == date, scores))
    
    if not date_scores:
        return func.HttpResponse(
            "No scores found for the given date.",
            status_code=200
    )

    return func.HttpResponse(
            f"{date_scores}",
            status_code=200
    )