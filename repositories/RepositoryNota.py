from datetime import date

from sqlalchemy.orm import Session

from models.ModelNota import ModelNota
from schemas.SchemaNota import NotaCreate, NotaUpdate


class NotaRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, nota: NotaCreate) -> ModelNota:
        db_nota = ModelNota(**nota.model_dump(), lancado_em=date.today())
        self.db.add(db_nota)
        self.db.commit()
        self.db.refresh(db_nota)
        return db_nota

    def get_byID(self, nota_id: int) -> ModelNota | None:
        return self.db.query(ModelNota).filter(ModelNota.id == nota_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelNota]:
        return self.db.query(ModelNota).offset(skip).limit(limit).all()

    def update(self, nota_id: int, dados: NotaUpdate) -> ModelNota | None:
        nota = self.get_byID(nota_id)
        if not nota:
            return None

        if dados.valor is not None:
            nota.valor = dados.valor
        if dados.tipo is not None:
            nota.tipo = dados.tipo
        if dados.bimestre is not None:
            nota.bimestre = dados.bimestre

        self.db.commit()
        self.db.refresh(nota)
        return nota

    def delete(self, nota_id: int) -> bool:
        nota = self.get_byID(nota_id)
        if not nota:
            return False
        self.db.delete(nota)
        self.db.commit()
        return True
