from sqlalchemy import select

from cinematch_back.models import User


def test_create_user(session):
    new_user = User(
        username='Jean', password='segredo', email='jean@teste.com'
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'Jean'))

    assert user.username == 'Jean'
