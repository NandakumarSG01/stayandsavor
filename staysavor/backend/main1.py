import logging
import pymysql
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Database connection
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='N@ndakumar@010213',  # Replace with your actual database password
        database='hotel_test'
    )


def get_order_status(order_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT status FROM bookings WHERE order_id = %s", (order_id,))
                result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        logger.error(f"Error fetching order status: {e}")
        return None


def cancel_booking_by_id(order_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM bookings WHERE order_id = %s", (order_id,))
                conn.commit()
                return cursor.rowcount > 0  # Returns True if a row was deleted
    except Exception as e:
        logger.error(f"Error canceling booking: {e}")
        return False


def insert_booking(room_type, check_in_date, check_out_date):
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO bookings (room_type, check_in_date, check_out_date) VALUES (%s, %s, %s)",
                               (room_type, check_in_date, check_out_date))
                conn.commit()
                return cursor.lastrowid  # Return the ID of the newly inserted booking
    except Exception as e:
        logger.error(f"Error inserting booking: {e}")
        return None


# FastAPI app
app = FastAPI()


def extract_session_id(output_contexts):
    return output_contexts[0]['name'].split('/')[-1]  # Extract session ID from context


# Intent handler functions
async def book_room(parameters, session_id):
    room_type = parameters.get('room_type')
    checkin_date = parameters.get('check_in_date')
    checkout_date = parameters.get('check_out_date')

    order_id = insert_booking(room_type, checkin_date, checkout_date)  # Insert booking and get ID

    if order_id:
        return JSONResponse(content={
            "fulfillmentText": f"You've booked a {room_type} room from {checkin_date} to {checkout_date}. Your booking ID is {order_id}."
        })
    else:
        return JSONResponse(content={"fulfillmentText": "There was an error booking your room."}, status_code=500)


async def select_room_type(parameters, session_id):
    room_type = parameters.get('room_type')

    if room_type:
        return JSONResponse(content={
            "fulfillmentText": f"You've selected a {room_type} room. When would you like to check in?"
        })
    else:
        return JSONResponse(content={
            "fulfillmentText": "I didn't catch that. Can you please tell me what type of room you want to book?"
        })


async def select_checkin_date(parameters, session_id):
    checkin_date = parameters.get('check_in_date')
    return JSONResponse(content={
        "fulfillmentText": f"You've selected {checkin_date} as your check-in date. When would you like to check out?"
    })


async def select_checkout_date(parameters, session_id):
    checkout_date = parameters.get('check_out_date')
    room_type = parameters.get('room_type')

    order_id = insert_booking(room_type, parameters['check_in_date'], checkout_date)  # Insert booking logic
    if order_id:
        return JSONResponse(content={
            "fulfillmentText": f"Your {room_type} room is booked from {parameters['check_in_date']} to {checkout_date}. Your booking ID is {order_id}. Thank you for choosing Stay & Savor!"
        })
    else:
        return JSONResponse(content={"fulfillmentText": "There was an error booking your room."}, status_code=500)


async def track_booking(parameters, session_id):
    order_id = parameters.get('order_id')
    status = get_order_status(order_id)

    if status is not None:
        return JSONResponse(content={
            "fulfillmentText": f"The status of your booking with ID {order_id} is {status}."
        })
    else:
        return JSONResponse(content={"fulfillmentText": "No booking found with that ID."}, status_code=404)


async def cancel_booking(parameters, session_id):
    order_id = parameters.get('order_id')
    if not order_id:
        return JSONResponse(content={
            "fulfillmentText": "Please provide your booking ID to proceed with the cancellation."
        })

    cancellation_success = cancel_booking_by_id(order_id)
    if cancellation_success:
        return JSONResponse(content={
            "fulfillmentText": f"Your booking with ID {order_id} has been canceled."
        })
    else:
        return JSONResponse(content={
            "fulfillmentText": f"I'm sorry, but I couldn't find a booking with ID {order_id}."
        })


@app.post("/book")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']
    session_id = extract_session_id(output_contexts)

    # Log the intent and parameters
    logger.info(f"Received Intent: {intent}, Parameters: {parameters}")

    # Mapping intents to handler functions
    intent_handler_dict = {
        'book.room': book_room,
        'select.room.type': select_room_type,
        'select.checkin_date': select_checkin_date,
        'select.checkout_date': select_checkout_date,
        'track.booking': track_booking,
        'cancel.booking': cancel_booking,
    }

    if intent in intent_handler_dict:
        return await intent_handler_dict[intent](parameters, session_id)
    else:
        return JSONResponse(content={"error": "Intent not recognized"}, status_code=400)


# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
