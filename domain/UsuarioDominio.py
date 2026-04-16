# ============================================================
# domain/UsuarioDominio.py
# Demonstra: Herança, Polimorfismo e Encapsulamento (POO)
# ============================================================

from abc import ABC, abstractmethod


class Usuario(ABC):
    """
    Superclasse abstrata para todos os tipos de usuário.
    Aplica encapsulamento (atributos privados) e define a
    interface comum que as subclasses devem implementar (herança + polimorfismo).
    """

    def __init__(self, nome: str, email: str):
        # Encapsulamento: atributos privados, acessíveis só via @property
        self.__nome = nome
        self.__email = email

    # --- Métodos públicos de acesso (encapsulamento) ---

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def email(self) -> str:
        return self.__email

    # --- Métodos abstratos (devem ser implementados pelas subclasses) ---

    @abstractmethod
    def get_permissoes(self) -> list[str]:
        """Retorna as permissões do perfil. Cada subclasse define as suas (polimorfismo)."""
        pass

    @abstractmethod
    def pode_deletar(self) -> bool:
        """Indica se o perfil tem permissão para deletar registros."""
        pass

    @abstractmethod
    def exibir_menu(self) -> list[str]:
        """
        Retorna os itens de menu disponíveis para o perfil.
        Polimorfismo: mesmo método, resultado diferente para cada tipo de usuário.
        """
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.__nome} ({self.__email})"


# ----------------------------------------------------------------

class Administrador(Usuario):
    """
    Subclasse de Usuario com acesso total ao sistema.
    Herda os atributos e comportamentos base de Usuario.
    """

    def get_permissoes(self) -> list[str]:
        # Polimorfismo: Administrador tem permissões completas
        return ["criar", "ler", "atualizar", "deletar", "gerenciar_usuarios"]

    def pode_deletar(self) -> bool:
        return True

    def exibir_menu(self) -> list[str]:
        # Polimorfismo: menu completo para o administrador
        return [
            "1 - Gerenciar Alunos",
            "2 - Gerenciar Turmas",
            "3 - Gerenciar Usuarios",
            "4 - Gerenciar Financeiro",
            "5 - Ver Relatorios",
            "6 - Configuracoes do Sistema",
            "0 - Sair",
        ]


# ----------------------------------------------------------------

class Operador(Usuario):
    """
    Subclasse de Usuario com acesso restrito.
    Não pode deletar registros nem acessar configurações do sistema.
    """

    def get_permissoes(self) -> list[str]:
        # Polimorfismo: Operador tem permissões limitadas
        return ["criar", "ler", "atualizar"]

    def pode_deletar(self) -> bool:
        return False

    def exibir_menu(self) -> list[str]:
        # Polimorfismo: menu reduzido para o operador
        return [
            "1 - Consultar Alunos",
            "2 - Consultar Turmas",
            "3 - Lancamento de Notas",
            "4 - Registro de Frequencia",
            "0 - Sair",
        ]


# ----------------------------------------------------------------

def criar_usuario_dominio(nome: str, email: str, perfil_nome: str) -> Usuario:
    
    if perfil_nome.lower() in ("administrador", "admin"):
        return Administrador(nome, email)
    return Operador(nome, email)
