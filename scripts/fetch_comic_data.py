import aiohttp
import asyncio
import asyncpg

# Database connection details
DB_CONFIG = {
    "database": "jet_assignment",
    "user": "postgres",
    "password": "{{ env_var('DBT_POSTGRES_PASSWORD') }}",
    "host": "localhost",
    "port": 5432
}

# Function to fetch the latest available XKCD comic number (called only once)
async def get_latest_comic_number():
    url = "https://xkcd.com/info.0.json"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    latest_comic = await response.json()
                    return latest_comic["num"]  # Get the latest comic ID
                else:
                    print(f"Failed to fetch latest comic number. Status: {response.status}")
                    return None
    except Exception as e:
        print(f"Error fetching latest comic number: {e}")
        return None

# Function to fetch a single comic
async def fetch_comic(session, comic_id):
    url = f"https://xkcd.com/{comic_id}/info.0.json"
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                print(f"Failed to fetch comic {comic_id}, Status: {response.status}")
                return None
    except Exception as e:
        print(f"Error fetching comic {comic_id}: {e}")
        return None

# Function to fetch comics in batches (improves performance)
async def fetch_comics_in_batches(start_id, end_id, batch_size=2):
    comics = []
    async with aiohttp.ClientSession() as session:
        for i in range(start_id, end_id + 1, batch_size):  # Ensure it reaches end_id
            tasks = [fetch_comic(session, comic_id) for comic_id in range(i, min(i + batch_size, end_id + 1))]
            results = await asyncio.gather(*tasks)
            comics.extend([comic for comic in results if comic])  # Remove None values
    return comics

# Function to insert comics into PostgreSQL using UPSERT (to avoid duplicate inserts)
async def insert_comics_to_postgres(comics):
    conn = await asyncpg.connect(
        database=DB_CONFIG["database"], 
        user=DB_CONFIG["user"], 
        password=DB_CONFIG["password"], 
        host=DB_CONFIG["host"], 
        port=DB_CONFIG["port"]
    )

    # Create table if it doesn't exist
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS jet_assignment_bronze.xkcd_comic_detail (
            num INTEGER PRIMARY KEY,
            title TEXT,
            safe_title TEXT,
            alt TEXT,
            img TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            link TEXT,
            news TEXT,
            transcript TEXT
        )
    """)

    # UPSERT query to insert or update existing records
    query = """
        INSERT INTO jet_assignment_bronze.xkcd_comic_detail (num, title, safe_title, alt, img, year, month, day, link, news, transcript)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        ON CONFLICT (num) 
        DO UPDATE SET 
            title = EXCLUDED.title,
            safe_title = EXCLUDED.safe_title,
            alt = EXCLUDED.alt,
            img = EXCLUDED.img,
            year = EXCLUDED.year,
            month = EXCLUDED.month,
            day = EXCLUDED.day,
            link = EXCLUDED.link,
            news = EXCLUDED.news,
            transcript = EXCLUDED.transcript;
    """

    # Prepare values for batch insertion
    values = [
        (
            comic["num"], 
            comic["title"], 
            comic["safe_title"], 
            comic["alt"], 
            comic["img"], 
            int(comic["year"]),  
            int(comic["month"]),  
            int(comic["day"]), 
            comic["link"], 
            comic["news"], 
            comic["transcript"]
        ) 
        for comic in comics
    ]

    try:
        # Bulk insert using executemany for better performance
        await conn.executemany(query, values)
        print(f"Inserted/Updated {len(comics)} comics into database...")
    except Exception as e:
        print(f"Database insertion error: {e}")
    
    await conn.close()

# Main function to orchestrate fetching & storing comics
async def main():
    start_comic_id = 1  # Start fetching from comic ID 1
    
    # Fetch the latest available XKCD comic number (only once)
    latest_comic_num = await get_latest_comic_number()
    if not latest_comic_num:
        print("Failed to retrieve latest comic number. Exiting...")
        return
    
    end_comic_id = latest_comic_num  # Use the latest comic ID dynamically

    print(f"Fetching comics from {start_comic_id} to {end_comic_id}")

    # Fetch comics in batches for efficiency
    comics_data = await fetch_comics_in_batches(start_comic_id, end_comic_id, batch_size=2)
    
    if comics_data:
        # Insert the comics into the database if data is fetched
        await insert_comics_to_postgres(comics_data)
        print(f" Total {len(comics_data)} comics pulled and inserted into the database.")
    else:
        print("No comics were fetched, stopping the process.")

    print("Data Ingestion Completed!")

# Run the async pipeline
asyncio.run(main())
