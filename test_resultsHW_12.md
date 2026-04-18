# API Testing Results

## 1. POST /api/tasks/ - Create Task
**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/tasks/ -H "Content-Type: application/json" -d "{\"title\": \"Test Task 1\", \"description\": \"First test task\", \"status\": \"new\", \"deadline\": \"2026-04-20T12:00:00Z\"}"
```

**Response:**
```json
{"id":7,"title":"Test Task 1","description":"First test task","status":"new","deadline":"2026-04-20T12:00:00Z","created_at":"2026-04-18T13:31:39.211475Z","created_date":"2026-04-18","categories":[]}
```

**Status:** 201 Created - SUCCESS

---

## 2. GET /api/tasks/list/ - Get All Tasks
**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/list/
```

**Response:**
```json
[
  {"id":8,"title":"Test Task 2","description":"Second test task","status":"in_progress","deadline":"2026-04-15T12:00:00Z","created_at":"2026-04-18T13:31:42.112836Z","created_date":"2026-04-18","categories":[]},
  {"id":7,"title":"Test Task 1","description":"First test task","status":"new","deadline":"2026-04-20T12:00:00Z","created_at":"2026-04-18T13:31:39.211475Z","created_date":"2026-04-18","categories":[]},
  {"id":5,"title":"Do It English!","description":"ENGLISH ENGLISH!","status":"blocked","deadline":"2026-03-31T18:00:00Z","created_at":"2026-03-29T21:43:49.466377Z","created_date":"2026-03-29","categories":["European Music","Gachi Music","English Music"]},
  {"id":4,"title":"Do it Gachi!","description":"GACHI GACHI","status":"pending","deadline":"2026-03-11T21:43:19Z","created_at":"2026-03-29T21:43:24.530921Z","created_date":"2026-03-29","categories":["European Music","Gachi Music"]},
  {"id":3,"title":"Create Melody With Violin","description":"Ching Cheng Hanji","status":"new","deadline":"2026-05-07T00:00:00Z","created_at":"2026-03-27T12:21:34.193696Z","created_date":"2026-03-27","categories":["Asian Music"]},
  {"id":2,"title":"Create Melody With Guitar","description":"Moya Oborona!","status":"in_progress","deadline":"2026-03-31T00:00:00Z","created_at":"2026-03-27T12:21:05.387615Z","created_date":"2026-03-27","categories":["European Music"]},
  {"id":1,"title":"Create Melody With Bongo","description":"Bongo Bongo Bom Bom Bom!!!","status":"in_progress","deadline":"2026-03-28T18:00:00Z","created_at":"2026-03-27T12:20:13.537207Z","created_date":"2026-03-27","categories":["European Music"]}
]
```

**Status:** 200 OK - SUCCESS

---

## 3. GET /api/tasks/7/ - Get Task by ID
**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/7/
```

**Response:**
```json
{"id":7,"title":"Test Task 1","description":"First test task","status":"new","deadline":"2026-04-20T12:00:00Z","created_at":"2026-04-18T13:31:39.211475Z","created_date":"2026-04-18","categories":[]}
```

**Status:** 200 OK - SUCCESS

---

## 4. GET /api/tasks/statistics/ - Get Task Statistics
**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/tasks/statistics/
```

**Response:**
```json
{"total_tasks":7,"tasks_by_status":{"new":2,"in_progress":3,"pending":1,"blocked":1,"done":0},"overdue_tasks":5}
```

**Status:** 200 OK - SUCCESS

---

## Testing Summary
All 4 API endpoints are working correctly:
- **Create Task**: Successfully creates new tasks
- **List Tasks**: Returns all tasks with proper ordering
- **Get Task by ID**: Returns specific task details
- **Statistics**: Provides aggregated task data including total count, status breakdown, and overdue tasks

The API is fully functional and ready for use.


