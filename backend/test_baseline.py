"""
Performance baseline test script
Run this to get current system metrics
"""
import requests
import time
import statistics

BASE_URL = "http://localhost:8000"

def test_exam_load_time():
    """Measure exam loading time"""
    times = []
    
    print("Testing exam load time (10 requests)...")
    for i in range(10):
        start = time.time()
        response = requests.get(f"{BASE_URL}/api/exams/1/")
        end = time.time()
        
        if response.status_code == 200:
            times.append((end - start) * 1000)  # Convert to ms
    
    if times:
        print(f"  Average: {statistics.mean(times):.2f}ms")
        print(f"  Min: {min(times):.2f}ms")
        print(f"  Max: {max(times):.2f}ms")
        print(f"  P95: {statistics.quantiles(times, n=20)[18]:.2f}ms")
    
    return statistics.mean(times) if times else 0

def test_concurrent_requests():
    """Test how many concurrent requests server can handle"""
    import concurrent.futures
    
    def make_request():
        try:
            start = time.time()
            response = requests.get(f"{BASE_URL}/api/exams/", timeout=10)
            return time.time() - start, response.status_code == 200
        except:
            return 0, False
    
    print("\nTesting concurrent capacity...")
    for users in [10, 50, 100, 200, 500]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=users) as executor:
            start = time.time()
            results = list(executor.map(lambda _: make_request(), range(users)))
            total_time = time.time() - start
            
            success_count = sum(1 for _, success in results if success)
            success_rate = (success_count / users) * 100
            
            print(f"  {users} users: {success_rate:.1f}% success, {total_time:.2f}s total")
            
            if success_rate < 90:
                print(f"  ⚠️  Capacity limit reached at ~{users} concurrent users")
                break

if __name__ == "__main__":
    print("=" * 50)
    print("APOLLO11 BASELINE PERFORMANCE TEST")
    print("=" * 50)
    
    avg_time = test_exam_load_time()
    test_concurrent_requests()
    
    print("\n" + "=" * 50)
    print("BASELINE METRICS SUMMARY")
    print("=" * 50)
    print(f"Average exam load time: {avg_time:.2f}ms")
    print("\nNext steps:")
    print("1. Run: locust -f locustfile.py --host=http://localhost:8000")
    print("2. Open: http://localhost:8089")
    print("3. Test with increasing users: 100, 500, 1000")
    print("=" * 50)
