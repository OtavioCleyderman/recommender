from models.user import User

def test_create_user():
    user = User(1, 'Juliana', 'juliana@example.com')
    assert user.id == 1
    assert user.name == 'Juliana'
    assert user.email == 'juliana@example.com'
    assert user.interest_profile == {}

def test_interest_update():
    user = User(1, 'Juliana', 'juliana@example.com')
    user.update_interest('viagem', 2)
    assert user.interest_profile["viagem"] == 2
