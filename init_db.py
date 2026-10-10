from app import app, seed_cardapio_padrao
from models import db, Usuario
from werkzeug.security import generate_password_hash


def run():
    with app.app_context():
        db.drop_all()
        db.create_all()

        admin = Usuario(nome="Administrador",
                        email="admin@pizzaria.com",
                        senha_hash=generate_password_hash("admin123"),
                        role="admin", admin_id=None)
        db.session.add(admin); db.session.commit()
        seed_cardapio_padrao(admin.id)

        garcom = Usuario(nome="Joao (Garcom)",
                         email="garcom@pizzaria.com",
                         senha_hash=generate_password_hash("garcom123"),
                         role="garcom", admin_id=admin.id)
        db.session.add(garcom)

        cozinha = Usuario(nome="Maria (Cozinha)",
                          email="cozinha@pizzaria.com",
                          senha_hash=generate_password_hash("cozinha123"),
                          role="cozinha", admin_id=admin.id)
        db.session.add(cozinha)
        db.session.commit()

        print("[OK] Banco criado!")
        print()
        print("Usuarios demo:")
        print("  ADMIN    admin@pizzaria.com   / admin123")
        print("  GARCOM   garcom@pizzaria.com  / garcom123")
        print("  COZINHA  cozinha@pizzaria.com / cozinha123")
        print()
        print("Rode: python app.py")
        print("Abra: http://127.0.0.1:5000")


if __name__ == "__main__":
    run()
