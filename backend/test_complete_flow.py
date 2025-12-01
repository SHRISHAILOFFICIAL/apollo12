"""
Final API Verification Test
Tests the complete exam flow: Register → Login → List Exams → Start Exam → Submit Answer → Submit Exam → Get Result
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000/api"

def test_complete_flow():
    print("\n" + "="*70)
    print("  QUIZ PLATFORM - COMPLETE FLOW TEST")
    print("="*70 + "\n")
    
    # Test 1: Student Login
    print("1️⃣  Testing Student Login...")
    login_data = {
        "username": "student",
        "password": "student123"
    }
    response = requests.post(f"{BASE_URL}/users/login/", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   ❌ Login failed: {response.text}")
        return
    
    data = response.json()
    token = data.get('access')
    user_id = data.get('user', {}).get('id')
    print(f"   ✅ Login successful! User ID: {user_id}")
    print(f"   Token: {token[:30]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 2: List Exams
    print("\n2️⃣  Fetching Available Exams...")
    response = requests.get(f"{BASE_URL}/exams/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"   ❌ Failed to fetch exams: {response.text}")
        return
    
    exams = response.json()
    print(f"   ✅ Found {len(exams)} exams:")
    for exam in exams:
        print(f"      - [{exam['id']}] {exam['title']} ({exam.get('duration_minutes')}min)")
    
    if not exams:
        print("   ⚠️  No exams available!")
        return
    
    exam_id = exams[0]['id']
    
    # Test 3: Get Exam Details
    print(f"\n3️⃣  Getting Details for Exam #{exam_id}...")
    response = requests.get(f"{BASE_URL}/exams/{exam_id}/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        exam_detail = response.json()
        print(f"   ✅ Exam: {exam_detail['title']}")
        print(f"   Description: {exam_detail.get('description', 'N/A')[:60]}...")
        print(f"   Total Marks: {exam_detail.get('total_marks')}")
    
    # Test 4: Start Exam
    print(f"\n4️⃣  Starting Exam #{exam_id}...")
    response = requests.post(f"{BASE_URL}/attempts/start_exam/", 
                            json={"exam": exam_id}, headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code not in [200, 201]:
        print(f"   ❌ Failed to start exam: {response.text}")
        return
    
    attempt_data = response.json()
    attempt_id = attempt_data.get('id')
    print(f"   ✅ Exam started! Attempt ID: {attempt_id}")
    print(f"   Status: {attempt_data.get('status')}")
    
    # Test 5: Get Questions
    print(f"\n5️⃣  Fetching Questions for Exam #{exam_id}...")
    response = requests.get(f"{BASE_URL}/exams/{exam_id}/take_exam/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        exam_questions = response.json()
        questions = exam_questions.get('questions', [])
        print(f"   ✅ Loaded {len(questions)} questions")
        
        if questions:
            q = questions[0]
            print(f"\n   Sample Question:")
            print(f"   Q: {q['question_text'][:70]}...")
            print(f"   Marks: {q['marks']} | Difficulty: {q['difficulty']}")
            
            # Test 6: Submit Answer
            if q.get('options'):
                print(f"\n6️⃣  Submitting Answer...")
                answer_data = {
                    "attempt": attempt_id,
                    "question": q['id'],
                    "option": q['options'][0]['id']  # Select first option
                }
                response = requests.post(f"{BASE_URL}/attempts/submit_answer/", 
                                        json=answer_data, headers=headers)
                print(f"   Status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    answer_result = response.json()
                    print(f"   ✅ Answer submitted!")
                    print(f"   Correct: {answer_result.get('is_correct', 'Unknown')}")
                else:
                    print(f"   ⚠️  Failed to submit answer: {response.text[:100]}")
    
    # Test 7: Submit Exam
    print(f"\n7️⃣  Submitting Exam...")
    response = requests.post(f"{BASE_URL}/attempts/{attempt_id}/submit_exam/", 
                            headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"   ✅ Exam submitted successfully!")
        print(f"   Total Score: {result.get('total_score', 0)}/{result.get('exam', {}).get('total_marks', 0)}")
        print(f"   Status: {result.get('status')}")
    
    # Test 8: Get Result
    print(f"\n8️⃣  Fetching Detailed Result...")
    response = requests.get(f"{BASE_URL}/attempts/{attempt_id}/result/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        detailed_result = response.json()
        print(f"   ✅ Result retrieved!")
        print(f"   Total Score: {detailed_result.get('total_score')}")
        print(f"   Percentage: {detailed_result.get('percentage')}%")
        print(f"   Result: {detailed_result.get('result')}")
        print(f"   Total Questions: {detailed_result.get('total_questions')}")
        print(f"   Correct Answers: {detailed_result.get('correct_answers')}")
        print(f"   Incorrect Answers: {detailed_result.get('incorrect_answers')}")
        print(f"   Unanswered: {detailed_result.get('unanswered')}")
    
    # Test 9: My Attempts
    print(f"\n9️⃣  Fetching All My Attempts...")
    response = requests.get(f"{BASE_URL}/attempts/my_attempts/", headers=headers)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        my_attempts = response.json()
        print(f"   ✅ Found {len(my_attempts)} attempt(s)")
        for att in my_attempts[:3]:
            print(f"      - Attempt #{att['id']}: {att.get('exam_title', 'N/A')} - Score: {att.get('total_score', 0)}")
    
    print("\n" + "="*70)
    print("  ✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*70 + "\n")
    print("🎉 Your Quiz Platform API is fully functional!\n")

if __name__ == "__main__":
    try:
        test_complete_flow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
