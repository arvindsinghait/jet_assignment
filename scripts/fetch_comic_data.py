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

# Function to fetch comics in batches
async def fetch_comics_in_batches(start_id, end_id, batch_size=2):
    comics = []
    async with aiohttp.ClientSession() as session:
        for i in range(start_id, end_id, batch_size):
            tasks = [fetch_comic(session, comic_id) for comic_id in range(i, min(i + batch_size, end_id))]
            results = await asyncio.gather(*tasks)
            comics.extend([comic for comic in results if comic])  # Filter out None values

    return comics

# Function to insert comics into PostgreSQL all at once
async def insert_comics_to_postgres(comics):
    conn = await asyncpg.connect(database=DB_CONFIG["database"], 
                                  user=DB_CONFIG["user"], 
                                  password=DB_CONFIG["password"], 
                                  host=DB_CONFIG["host"], 
                                  port=DB_CONFIG["port"])

    # Drop table if it exists (if you want to clear the table before inserting new data)
    await conn.execute("""
        DROP TABLE IF EXISTS jet_assignment_bronze.xkcd_comic_detail;
    """)

    # Create table again after dropping
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS jet_assignment_bronze.xkcd_comic_detail (
            num SERIAL PRIMARY KEY,
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

    # Prepare the data to insert all at once
    query = """
        INSERT INTO jet_assignment_bronze.xkcd_comic_detail (num, title, safe_title, alt, img, year, month, day, link, news, transcript)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    """

    # Insert all comics data at once
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

    # Insert the data all at once
    await conn.executemany(query, values)
    print(f"Inserted {len(comics)} comics into database...")

    await conn.close()

# Main function to orchestrate fetching & storing comics
async def main():
    start_comic_id = 1
    end_comic_id = 3000  # Fetch 3000 comics

    comics_data = await fetch_comics_in_batches(start_comic_id, end_comic_id, batch_size=2)
    
    if comics_data:
        # Insert the comics into the database if data is fetched
        await insert_comics_to_postgres(comics_data)
        print(f"Total {len(comics_data)} comics pulled and inserted into the database.")
    else:
        print("No comics were fetched, stopping the process.")

    print("Data Ingestion Completed!")

# Run the async pipeline
asyncio.run(main())
