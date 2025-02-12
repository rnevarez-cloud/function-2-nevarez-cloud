import azure.functions as func
import logging
import datetime
import json

date = str(datetime.date.today())

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="get_scores")
@app.route(route="scores")
@app.cosmos_db_input(arg_name="inputDocument", 
                     database_name="game_scores", 
                     container_name="scores_container",
                     sql_query=f"SELECT * FROM c where c.date = '{date}'",
                     connection="CosmosDbConnectionSetting")

def get_scores(inputDocument: func.DocumentList,
                req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info(date)
    scores = []
    for d in inputDocument:
        scores.append(d.to_dict())
   
    if not scores:
        return func.HttpResponse(
            "No scores found for the given date.",
            status_code=200
    )

    return func.HttpResponse(
            json.dumps(scores),
            status_code=200
    )