from abc import ABC, abstractmethod
from datetime import date


class EntidadeBase(ABC):
    """
    Superclasse abstrata para todas as entidades do sistema.
    Define atributos comuns (id, criado_em) e obriga as subclasses
    a implementarem os métodos validar() e resumo() (polimorfismo).
    """

    def __init__(self, id: int):
        self.__id = id                    # Encapsulamento: atributo privado
        self.__criado_em = date.today()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def criado_em(self) -> date:
        return self.__criado_em

    @abstractmethod
    def validar(self) -> bool:
        """Valida os dados obrigatórios da entidade."""
        pass

    @abstractmethod
    def resumo(self) -> str:
        """Retorna um texto resumido da entidade para relatórios."""
        pass

    def __str__(self) -> str:
        return self.resumo()


# ----------------------------------------------------------------

class AlunoEntidade(EntidadeBase):
    """
    Representa um Aluno como entidade de domínio.
    Herda de EntidadeBase e encapsula os dados do aluno.
    """

    def __init__(self, id: int, nome: str, cpf: str, matricula_numero: int, ativo: bool):
        super().__init__(id)              # Herança: chama o __init__ da superclasse
        self.__nome = nome                # Encapsulamento: atributos privados
        self.__cpf = cpf
        self.__matricula_numero = matricula_numero
        self.__ativo = ativo

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def cpf(self) -> str:
        # Exibe CPF mascarado (encapsulamento protege o dado real)
        return f"***{self.__cpf[-4:]}"

    @property
    def matricula_numero(self) -> int:
        return self.__matricula_numero

    @property
    def ativo(self) -> bool:
        return self.__ativo

    def validar(self) -> bool:
        """Valida se os dados mínimos do aluno estão preenchidos."""
        return bool(self.__nome) and len(self.__cpf) >= 11 and self.__matricula_numero > 0

    def resumo(self) -> str:
        """Polimorfismo: resumo específico para Aluno."""
        status = "Ativo" if self.__ativo else "Inativo"
        return f"Aluno #{self.id} | {self.__nome} | Mat: {self.__matricula_numero} | {status}"


# ----------------------------------------------------------------

class TurmaEntidade(EntidadeBase):
    """
    Representa uma Turma como entidade de domínio.
    Herda de EntidadeBase e encapsula os dados da turma.
    """

    def __init__(self, id: int, nome: str, serie: str, turno: str, ano_letivo: int):
        super().__init__(id)              # Herança: chama o __init__ da superclasse
        self.__nome = nome
        self.__serie = serie
        self.__turno = turno
        self.__ano_letivo = ano_letivo

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def turno(self) -> str:
        return self.__turno

    @property
    def ano_letivo(self) -> int:
        return self.__ano_letivo

    def validar(self) -> bool:
        """Valida se os dados mínimos da turma estão preenchidos."""
        return bool(self.__nome) and self.__ano_letivo >= 2000

    def resumo(self) -> str:
        """Polimorfismo: resumo específico para Turma."""
        return f"Turma #{self.id} | {self.__nome} | {self.__serie} | {self.__turno} | {self.__ano_letivo}"
