import oracledb

# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_connection():
    return oracledb.connect(
        user="YOUR_ORACLE_USERNAME",
        password="YOUR_ORACLE_PASSWORD",
        dsn="YOUR_ORACLE_DSN"
    )

# -------------------------
# HELPER: PRINT RESULTS
# -------------------------
def print_results(cursor):
    rows = cursor.fetchall()
    if not rows:
        print("\nNo results found.\n")
        return

    col_names = [desc[0] for desc in cursor.description]
    print()
    print(" | ".join(col_names))
    print("-" * 100)

    for row in rows:
        print(" | ".join(str(value) if value is not None else "NULL" for value in row))
    print()

# -------------------------
# FEATURE 1
# Flights in a date range
# -------------------------
def feature_1(cursor):
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    query = """
    SELECT
        f.FLIGHT_ID,
        a.AIR_NAME,
        dep.AIRP_NAME AS DEPARTURE_AIRPORT,
        arr.AIRP_NAME AS ARRIVAL_AIRPORT,
        f.FLIGHT_DATE,
        f.FLIGHT_SCH_DEPART,
        f.FLIGHT_ACT_DEPART,
        f.FLIGHT_SCH_ARRIVAL,
        f.FLIGHT_ACT_ARRIVAL
    FROM FLIGHTS f
    JOIN AIRLINE a
        ON f.AIR_ID = a.AIR_ID
    JOIN AIRPORT dep
        ON f.DEPART_AIRP_ID = dep.AIRP_ID
    JOIN AIRPORT arr
        ON f.ARRIVAL_AIRP_ID = arr.AIRP_ID
    WHERE f.FLIGHT_DATE BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD')
                            AND TO_DATE(:end_date, 'YYYY-MM-DD')
    ORDER BY f.FLIGHT_DATE, f.FLIGHT_ID
    """

    cursor.execute(query, start_date=start_date, end_date=end_date)
    print_results(cursor)

# -------------------------
# FEATURE 2
# Delayed flights by reason and minimum delay
# -------------------------
def feature_2(cursor):
    delay_reason = input("Enter delay reason (Weather, Technical, Crew, Security, None): ").strip()
    min_delay = input("Enter minimum delay minutes: ").strip()

    query = """
    SELECT
        f.FLIGHT_ID,
        a.AIR_NAME,
        dep.AIRP_CODE AS DEPARTURE_CODE,
        arr.AIRP_CODE AS ARRIVAL_CODE,
        d.DELAY_REASON,
        d.DELAY_MINUTES,
        f.FLIGHT_DATE
    FROM DELAYS d
    JOIN FLIGHTS f
        ON d.FLIGHT_ID = f.FLIGHT_ID
    JOIN AIRLINE a
        ON f.AIR_ID = a.AIR_ID
    JOIN AIRPORT dep
        ON f.DEPART_AIRP_ID = dep.AIRP_ID
    JOIN AIRPORT arr
        ON f.ARRIVAL_AIRP_ID = arr.AIRP_ID
    WHERE UPPER(d.DELAY_REASON) = UPPER(:delay_reason)
      AND d.DELAY_MINUTES >= :min_delay
    ORDER BY d.DELAY_MINUTES DESC, f.FLIGHT_ID
    """

    cursor.execute(query, delay_reason=delay_reason, min_delay=int(min_delay))
    print_results(cursor)

# -------------------------
# FEATURE 3
# Flights for a selected airline within a date range
# -------------------------
def feature_3(cursor):
    airline_name = input("Enter airline name: ").strip()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    query = """
    SELECT
        f.FLIGHT_ID,
        a.AIR_NAME,
        dep.AIRP_CODE AS DEPARTURE_CODE,
        arr.AIRP_CODE AS ARRIVAL_CODE,
        f.FLIGHT_DATE,
        f.FLIGHT_SCH_DEPART,
        f.FLIGHT_ACT_DEPART,
        f.FLIGHT_SCH_ARRIVAL,
        f.FLIGHT_ACT_ARRIVAL
    FROM FLIGHTS f
    JOIN AIRLINE a
        ON f.AIR_ID = a.AIR_ID
    JOIN AIRPORT dep
        ON f.DEPART_AIRP_ID = dep.AIRP_ID
    JOIN AIRPORT arr
        ON f.ARRIVAL_AIRP_ID = arr.AIRP_ID
    WHERE UPPER(a.AIR_NAME) = UPPER(:airline_name)
      AND f.FLIGHT_DATE BETWEEN TO_DATE(:start_date, 'YYYY-MM-DD')
                            AND TO_DATE(:end_date, 'YYYY-MM-DD')
    ORDER BY f.FLIGHT_DATE, f.FLIGHT_ID
    """

    cursor.execute(
        query,
        airline_name=airline_name,
        start_date=start_date,
        end_date=end_date
    )
    print_results(cursor)

# -------------------------
# FEATURE 4
# Airlines operating at a selected airport
# -------------------------
def feature_4(cursor):
    airport_code = input("Enter airport code (ex: ABE): ").strip()

    query = """
    SELECT DISTINCT
        ap.AIRP_NAME,
        ap.AIRP_CODE,
        al.AIR_NAME,
        al.AIR_CODE
    FROM AIRLINE_AIRPORT aa
    JOIN AIRLINE al
        ON aa.AIR_ID = al.AIR_ID
    JOIN AIRPORT ap
        ON aa.AIRP_ID = ap.AIRP_ID
    WHERE UPPER(ap.AIRP_CODE) = UPPER(:airport_code)
    ORDER BY al.AIR_NAME
    """

    cursor.execute(query, airport_code=airport_code)
    print_results(cursor)

# -------------------------
# FEATURE 5
# Airline performance summary
# -------------------------
def feature_5(cursor):
    query = """
    SELECT
        a.AIR_NAME,
        COUNT(DISTINCT f.FLIGHT_ID) AS TOTAL_FLIGHTS,
        COUNT(DISTINCT CASE
            WHEN d.DELAY_MINUTES > 0 THEN f.FLIGHT_ID
        END) AS DELAYED_FLIGHTS,
        ROUND(AVG(CASE
            WHEN d.DELAY_MINUTES > 0 THEN d.DELAY_MINUTES
        END), 2) AS AVG_DELAY_MINUTES
    FROM AIRLINE a
    LEFT JOIN FLIGHTS f
        ON a.AIR_ID = f.AIR_ID
    LEFT JOIN DELAYS d
        ON f.FLIGHT_ID = d.FLIGHT_ID
    GROUP BY a.AIR_NAME
    ORDER BY TOTAL_FLIGHTS DESC, a.AIR_NAME
    """

    cursor.execute(query)
    print_results(cursor)

# -------------------------
# MENU
# -------------------------
def main():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        while True:
            print("Airline Flight Delay & Operations Database")
            print("1. View flights in a date range")
            print("2. Show delayed flights by reason and minimum delay")
            print("3. Show flights for a selected airline in a date range")
            print("4. Show all airlines operating at a selected airport")
            print("5. Show airline performance summary")
            print("6. Exit")

            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                feature_1(cursor)
            elif choice == "2":
                feature_2(cursor)
            elif choice == "3":
                feature_3(cursor)
            elif choice == "4":
                feature_4(cursor)
            elif choice == "5":
                feature_5(cursor)
            elif choice == "6":
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.\n")

        cursor.close()
        connection.close()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
