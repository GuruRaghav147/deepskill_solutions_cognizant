import mysql.connector
import time

# Db connection
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root1234!',
    'database': 'college_db'
}


#56.N+1 Problem Simulation

def run_n_plus_one_approach():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query_count = 0
    start_time = time.time()
    
    # 1. The "1" Query: Fetch all enrollments (Assume this returns N rows, Ex.12 rows)
    cursor.execute("SELECT * FROM enrollments;")
    enrollments = cursor.fetchall()
    query_count += 1
    
    results = []
    # 2. The "N" Queries: Loop through each row and fire a separate query
    for enrollment in enrollments:
        cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s;", 
            (enrollment['student_id'],)
        )
        student = cursor.fetchone()
        query_count += 1
        
        results.append({
            'enrollment_id': enrollment['enrollment_id'],
            'student_name': f"{student['first_name']} {student['last_name']}" if student else "Unknown"
        })
        
    end_time = time.time()
    cursor.close()
    conn.close()
    
    print(f"--- N+1 Approach ---")
    print(f"Queries executed: {query_count}")
    print(f"Execution time: {end_time - start_time:.6f} seconds\n")
    return results



# 57.Optimized Single JOIN Query

def run_optimized_approach():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    
    query_count = 0
    start_time = time.time()
    
    
    single_query = """
        SELECT e.enrollment_id, CONCAT(s.first_name, ' ', s.last_name) AS student_name
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id;
    """
    cursor.execute(single_query)
    results = cursor.fetchall()
    query_count += 1
    
    end_time = time.time()
    cursor.close()
    conn.close()
    
    print(f"--- Optimized JOIN Approach ---")
    print(f"Queries executed: {query_count}")
    print(f"Execution time: {end_time - start_time:.6f} seconds\n")
    return results

# 58. Run and Compare

if __name__ == "__main__":
    # Run both and log metrics via Python's time module
    n_plus_one_data = run_n_plus_one_approach()
    optimized_data = run_optimized_approach()
