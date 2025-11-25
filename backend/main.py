from services.user_service import UserService

def run_app():
    """
    Função principal que simula a execução da aplicação.
    """
    print("Iniciando a Aplicação Web...")
    
    user_service = UserService()
    
    try:
        # Tenta registrar alguns usuários
        print("\nTentando inserir dados...")
        user1_id = user_service.register_new_user("Alice", "alice@example.com")
        print(f"Usuário 1 registrado com ID: {user1_id}")
        
        user2_id = user_service.register_new_user("Bob", "bob@example.com")
        print(f"Usuário 2 registrado com ID: {user2_id}")
        
        # Simula a execução da aplicação (seu loop principal de servidor web, etc.)
        # O código fica "rodando" aqui
        import time
        print("\nAplicação rodando... Pressione Ctrl+C para simular o fechamento.")
        # time.sleep(10) # Manteria a aplicação ativa por 10 segundos
        
        # Em uma aplicação real, você teria aqui o loop do seu servidor web (Flask/Django)
        # Ex: app.run()

        # Para este exemplo, usaremos um input para simular a espera
        input("Pressione ENTER para fechar a aplicação...")

    except KeyboardInterrupt:
        print("\nDetectado Ctrl+C. Fechando a aplicação.")
    except Exception as e:
        print(f"\nOcorreu um erro durante a execução: {e}")
    finally:
        # A função cleanup_database será chamada automaticamente pelo atexit
        print("\n--- Processo de Finalização Inciado ---")


if __name__ == "__main__":
    run_app()

# Ao terminar o script, o atexit garante a chamada da função de limpeza