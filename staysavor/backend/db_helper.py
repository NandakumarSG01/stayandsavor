import pymysql

# Establish a connection to your MySQL database
def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='N@ndakumar@010213',  # Replace with your actual database password
        database='hotel_test'
    )

def get_order_status(order_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT status FROM bookings WHERE order_id = %s", (order_id,))
                result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        print(f"Error fetching order status: {e}")
        return None

def cancel_booking_by_id(order_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM bookings WHERE order_id = %s", (order_id,))
                connection.commit()
                return cursor.rowcount > 0  # Returns True if a row was deleted
    except Exception as e:
        print(f"Error canceling booking: {e}")
        return False

def insert_booking(room_type, check_in_date, check_out_date):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO bookings (room_type, check_in_date, check_out_date) VALUES (%s, %s, %s)",
                               (room_type, check_in_date, check_out_date))
                connection.commit()
                return cursor.lastrowid  # Return the ID of the newly inserted booking
    except Exception as e:
        print(f"Error inserting booking: {e}")
        return None

# Example usage
if __name__ == "__main__":
    # Test inserting a booking
    booking_id = insert_booking('Deluxe', '2024-10-20', '2024-10-25')
    print(f"Inserted booking ID: {booking_id}")

    # Test getting order status
    status = get_order_status(booking_id)
    print(f"Booking status: {status}")

    # Test canceling a booking
    if cancel_booking_by_id(booking_id):
        print(f"Booking ID {booking_id} canceled successfully.")
    else:
        print(f"Failed to cancel booking ID {booking_id}.")
