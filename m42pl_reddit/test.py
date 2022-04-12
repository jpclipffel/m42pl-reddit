import asyncio
import asyncpraw

async def main():
    reddit = asyncpraw.Reddit(
        client_id='vFCsESPmNbbwbg7rK-uf9A',
        client_secret='vnTLANmy_Inv6b3V3aDmfcKeWTbLJg',
        user_agent='darwin:m42pl-test:0.0.1 (by /u/Pl4nkRDT)'
    )
    subreddit = await reddit.subreddit('learnpython')
    async for submission in subreddit.hot(limit=10):
        print(submission)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
