import subprocess
import asyncio
import time

async def run_async_scripts():
    print("Starting asynchronous scripts...")
    # Run ZK_Assync.py and SQL_write.py asynchronously
    process1 = await asyncio.create_subprocess_exec('python', 'SQL_write.py')
    process2 = await asyncio.create_subprocess_exec('python', 'ZK_Assync.py')
    
    print(f"Started ZK_Assync.py with PID: {process1.pid}")
    print(f"Started SQL_write.py with PID: {process2.pid}")
    
    # Add a delay before starting POST.py
    await asyncio.sleep(10)
    process3 = await asyncio.create_subprocess_exec('python', 'POST.py')
    print(f"Started POST.py with PID: {process3.pid}")
    
    await process1.wait()
    await process2.wait()
    await process3.wait()
    print("Asynchronous scripts completed.")

def main():
    print("Running sync.py...")
    # Run sync.py synchronously
    subprocess.run(['python', 'Sync.py'])
    print("sync.py completed.")
    
    # Run the async scripts
    asyncio.run(run_async_scripts())

if __name__ == "__main__":
    main()
