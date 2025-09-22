

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from entities.mapa_categoria import Mapa
from entities.usuario import Usuario


class MapaCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_mapa(
        self,
        region: str,
        escala: str,
        tipo: str,
        producto_id: UUID,
        id_usuario_crea: UUID = None,
    ) -> Mapa:
        if not region or len(region.strip()) == 0:
            raise ValueError("La región es obligatoria")
        if len(region) > 100:
            raise ValueError("La región no puede exceder 100 caracteres")
        if not escala or len(escala.strip()) == 0:
            raise ValueError("La escala es obligatoria")
        if len(escala) > 50:
            raise ValueError("La escala no puede exceder 50 caracteres")
        if not tipo or len(tipo.strip()) == 0:
            raise ValueError("El tipo es obligatorio")
        if len(tipo) > 50:
            raise ValueError("El tipo no puede exceder 50 caracteres")
        if id_usuario_crea is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para crear el mapa"
                )
            id_usuario_crea = admin.id_usuario
        mapa = Mapa(
            region=region.strip(),
            escala=escala.strip(),
            tipo=tipo.strip(),
            producto_id=producto_id,
            id_usuario_crea=id_usuario_crea,
        )
        self.db.add(mapa)
        self.db.commit()
        self.db.refresh(mapa)
        return mapa

    def obtener_mapa(self, mapa_id: UUID) -> Optional[Mapa]:
        return self.db.query(Mapa).filter(Mapa.id_mapa == mapa_id).first()

    def obtener_mapas(self, skip: int = 0, limit: int = 100) -> List[Mapa]:
        return self.db.query(Mapa).offset(skip).limit(limit).all()

    def actualizar_mapa(
        self, mapa_id: UUID, id_usuario_edita: UUID = None, **kwargs
    ) -> Optional[Mapa]:
        mapa = self.obtener_mapa(mapa_id)
        if not mapa:
            return None
        if "region" in kwargs:
            region = kwargs["region"]
            if not region or len(region.strip()) == 0:
                raise ValueError("La región es obligatoria")
            if len(region) > 100:
                raise ValueError("La región no puede exceder 100 caracteres")
            kwargs["region"] = region.strip()
        if "escala" in kwargs:
            escala = kwargs["escala"]
            if not escala or len(escala.strip()) == 0:
                raise ValueError("La escala es obligatoria")
            if len(escala) > 50:
                raise ValueError("La escala no puede exceder 50 caracteres")
            kwargs["escala"] = escala.strip()
        if "tipo" in kwargs:
            tipo = kwargs["tipo"]
            if not tipo or len(tipo.strip()) == 0:
                raise ValueError("El tipo es obligatorio")
            if len(tipo) > 50:
                raise ValueError("El tipo no puede exceder 50 caracteres")
            kwargs["tipo"] = tipo.strip()
        if id_usuario_edita is None:
            admin = self.db.query(Usuario).filter(Usuario.es_admin == True).first()
            if not admin:
                raise ValueError(
                    "No se encontró un usuario administrador para editar el mapa"
                )
            id_usuario_edita = admin.id_usuario
        mapa.id_usuario_edita = id_usuario_edita
        for key, value in kwargs.items():
            if hasattr(mapa, key):
                setattr(mapa, key, value)
        self.db.commit()
        self.db.refresh(mapa)
        return mapa

    def eliminar_mapa(self, mapa_id: UUID) -> bool:
        mapa = self.obtener_mapa(mapa_id)
        if mapa:
            self.db.delete(mapa)
            self.db.commit()
            return True
        return False
