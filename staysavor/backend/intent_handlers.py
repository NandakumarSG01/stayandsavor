from fastapi.responses import JSONResponse
import db_helper  # Import database helper functions

async def book_room(parameters):
    room_type = parameters.get('room_type')
    checkin_date = parameters.get('checkin_date')
    checkout_date = parameters.get('checkout_date')

    # Store booking in the database
    order_id = db_helper.insert_booking(room_type, checkin_date, checkout_date)  # Adjusted to return the order ID

    return JSONResponse(content={
        "fulfillmentText": f"You've booked a {room_type} room from {checkin_date} to {checkout_date}. Your booking ID is {order_id}."
    })


def select_room_type(parameters):
    room_type = parameters.get('room_type')
    return JSONResponse(content={
        "fulfillmentText": f"You've selected a {room_type} room. When would you like to check in?"
    })


async def select_checkin_date(parameters):
    checkin_date = parameters.get('check_in_date')
    return JSONResponse(content={
        "fulfillmentText": f"You've selected {checkin_date} as your check-in date. When would you like to check out?"
    })


async def select_checkout_date(parameters):
    checkout_date = parameters.get('check_out_date')
    room_type = parameters.get('room_type')  # Fetch this from parameters

    order_id = db_helper.insert_booking(room_type, parameters['check_in_date'], checkout_date)  # Insert booking logic

    return JSONResponse(content={
        "fulfillmentText": f"Your {room_type} room is booked from {parameters['check_in_date']} to {checkout_date}. Your booking ID is {order_id}. Thank you for choosing Stay & Savor!"
    })


async def track_booking(parameters):
    order_id = parameters.get('order_id')
    status = db_helper.get_order_status(order_id)

    return JSONResponse(content={
        "fulfillmentText": f"The status of your booking with ID {order_id} is {status}."
    })


async def cancel_booking(parameters):
    order_id = parameters.get('order_id')
    if not order_id:
        return JSONResponse(content={
            "fulfillmentText": "Please provide your booking ID to proceed with the cancellation."
        })

    cancellation_success = db_helper.cancel_booking_by_id(order_id)
    if cancellation_success:
        return JSONResponse(content={
            "fulfillmentText": f"Your booking with ID {order_id} has been canceled."
        })
    else:
        return JSONResponse(content={
            "fulfillmentText": f"I'm sorry, but I couldn't find a booking with ID {order_id}."
        })
