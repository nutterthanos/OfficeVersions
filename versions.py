import aiohttp
import asyncio
import aiofiles

async def fetch_url(session, semaphore, url):
    try:
        async with semaphore:
            async with session.head(url) as response:
                print(f"Checking {url}, HTTP status: {response.status}")
                if response.status == 200:
                    return url
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return None

async def process_versions(session, semaphore, base_url, start_build, end_build, start_revision, end_revision, output_file):
    valid_urls = []
    
    async with aiofiles.open(output_file, mode='w') as file:
        tasks = []

        for build in range(start_build, end_build + 1):
            for revision in range(start_revision, end_revision + 1):
                version = f"16.0.{build}.{revision}"
                url_with_version = base_url.format(version=version)
                
                task = fetch_url(session, semaphore, url_with_version)
                tasks.append(task)

        valid_urls = await asyncio.gather(*tasks)
        valid_urls = [url for url in valid_urls if url is not None]

        for url in valid_urls:
            await file.write(url + '\n')

    return valid_urls

async def main():
    base_url = "http://officecdn.microsoft.com/sg/EA4A4090-DE26-49D7-93C1-91BFF9E53FC3/Office/Data/v64_{version}.cab"
    start_build = 9200
    end_build = 9300
    start_revision = 0
    end_revision = 25000
    output_file = "valid_urls.txt"
    max_concurrent_requests = 100

    semaphore = asyncio.Semaphore(max_concurrent_requests)

    async with aiohttp.ClientSession() as session:
        valid_urls = await process_versions(session, semaphore, base_url, start_build, end_build, start_revision, end_revision, output_file)

    print(f"Valid URLs written to {output_file}:\n{valid_urls}")

if __name__ == "__main__":
    asyncio.run(main())
