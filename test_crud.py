import unittest
from fastapi.testclient import TestClient
from main import app

class TestUserCRUD(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_01_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        print("✅ Health check passed:", data)

    def test_02_create_user(self):
        payload = {
            "name": "Alice Johnson",
            "email": "alice.johnson@example.com",
            "role": "developer",
            "is_active": True
        }
        response = self.client.post("/api/v1/users/", json=payload)
        self.assertIn(response.status_code, [201, 400])
        if response.status_code == 201:
            data = response.json()
            self.assertEqual(data["name"], "Alice Johnson")
            self.assertEqual(data["email"], "alice.johnson@example.com")
            self.assertEqual(data["role"], "developer")
            print("✅ User creation passed:", data)

    def test_03_duplicate_email_prevention(self):
        payload = {
            "name": "Alice Duplicate",
            "email": "alice.johnson@example.com",
            "role": "user"
        }
        response = self.client.post("/api/v1/users/", json=payload)
        self.assertEqual(response.status_code, 400)
        print("✅ Duplicate email error prevention passed.")

    def test_04_get_users_list(self):
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("total", data)
        self.assertIn("users", data)
        self.assertGreaterEqual(data["total"], 1)
        print(f"✅ List users passed (Total: {data['total']}).")

    def test_05_search_users(self):
        response = self.client.get("/api/v1/users/?search=Alice")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data["users"]), 1)
        print(f"✅ User search passed (Found: {len(data['users'])}).")

    def test_06_update_user(self):
        # First get list of users
        list_res = self.client.get("/api/v1/users/")
        user_id = list_res.json()["users"][0]["id"]

        update_payload = {
            "name": "Alice J. Smith",
            "role": "admin"
        }
        response = self.client.put(f"/api/v1/users/{user_id}", json=update_payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Alice J. Smith")
        self.assertEqual(data["role"], "admin")
        print("✅ User update passed:", data)

    def test_07_get_single_user(self):
        list_res = self.client.get("/api/v1/users/")
        user_id = list_res.json()["users"][0]["id"]

        response = self.client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], user_id)
        print("✅ Get single user passed:", data)

    def test_08_delete_user(self):
        # Create temp user to delete
        temp_payload = {
            "name": "Temp User",
            "email": "temp.user@example.com",
            "role": "user"
        }
        create_res = self.client.post("/api/v1/users/", json=temp_payload)
        self.assertEqual(create_res.status_code, 201)
        temp_id = create_res.json()["id"]

        # Delete temp user
        del_res = self.client.delete(f"/api/v1/users/{temp_id}")
        self.assertEqual(del_res.status_code, 200)

        # Verify 404 on get
        get_res = self.client.get(f"/api/v1/users/{temp_id}")
        self.assertEqual(get_res.status_code, 404)
        print("✅ User deletion & 404 verification passed.")

if __name__ == "__main__":
    unittest.main()
