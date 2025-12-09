import unittest
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Game

class TestGameAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['JWT_SECRET_KEY'] = 'test-secret-key'
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            user = User(username='testadmin', email='admin@test.com', is_admin=True)
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
            
            response = self.client.post('/api/auth/login', 
                json={'username': 'testadmin', 'password': 'testpass'})
            self.token = json.loads(response.data)['access_token']
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_register_user(self):
        response = self.client.post('/api/auth/register', 
            json={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpass123'
            })
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_login_user(self):
        response = self.client.post('/api/auth/login', 
            json={'username': 'testadmin', 'password': 'testpass'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('access_token', data)
    
    def test_create_game(self):
        game_data = {
            'name': 'Test Game',
            'description': 'Test Description',
            'year': 2023,
            'image': 'https://example.com/image.jpg',
            'url': 'https://example.com'
        }
        
        response = self.client.post('/api/games/', 
            json=game_data,
            headers={'Authorization': f'Bearer {self.token}'})
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['game']['name'], 'Test Game')
    
    def test_get_games(self):
        game_data = {
            'name': 'Test Game',
            'description': 'Test Description',
            'year': 2023
        }
        
        self.client.post('/api/games/', 
            json=game_data,
            headers={'Authorization': f'Bearer {self.token}'})
        
        response = self.client.get('/api/games/')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('games', data)
    
    def test_update_game(self):
        game_data = {
            'name': 'Old Name',
            'description': 'Old Description',
            'year': 2020
        }
        
        create_response = self.client.post('/api/games/', 
            json=game_data,
            headers={'Authorization': f'Bearer {self.token}'})
        
        game_id = json.loads(create_response.data)['game']['id']
        
        update_data = {
            'name': 'Updated Name',
            'description': 'Updated Description'
        }
        
        response = self.client.put(f'/api/games/{game_id}', 
            json=update_data,
            headers={'Authorization': f'Bearer {self.token}'})
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['game']['name'], 'Updated Name')
    
    def test_delete_game(self):
        game_data = {
            'name': 'Game to Delete',
            'description': 'Will be deleted',
            'year': 2023
        }
        
        create_response = self.client.post('/api/games/', 
            json=game_data,
            headers={'Authorization': f'Bearer {self.token}'})
        
        game_id = json.loads(create_response.data)['game']['id']
        
        response = self.client.delete(f'/api/games/{game_id}',
            headers={'Authorization': f'Bearer {self.token}'})
        
        self.assertEqual(response.status_code, 200)
        
        get_response = self.client.get(f'/api/games/{game_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()