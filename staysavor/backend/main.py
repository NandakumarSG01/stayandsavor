from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Intent handlers
from intent_handlers import (
    book_room,
    select_room_type,
    select_checkin_date,
    select_checkout_date,
    track_booking,
    cancel_booking
)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Stay & Savor API!"}

@app.get("/test")
async def test_endpoint():
    return {"message": "This is a test endpoint."}

@app.post("/book")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = extract_session_id(output_contexts)

    intent_handler_dict = {
        'book.room': book_room,
        'select.room.type': select_room_type,
        'select.checkin_date': select_checkin_date,
        'select.checkout_date': select_checkout_date,
        'track.booking': track_booking,
        'cancel.booking': cancel_booking
    }

    if intent in intent_handler_dict:
        return await intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(content={"error": "Intent not recognized"}, status_code=400)

def extract_session_id(output_contexts):
    # Extract session ID from output contexts
    if output_contexts:
        session_path = output_contexts[0]['name']
        session_id = session_path.split('/')[5]  # Extract the session ID from the context path
        return session_id
    return None

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
