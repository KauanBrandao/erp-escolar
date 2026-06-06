def criar_usuario(
    dados: UsuarioCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    return ServiceUsuario(db).criar(dados)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuario(
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    return ServiceUsuario(db).listar()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def buscar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    return ServiceUsuario(db).buscar_por_id(usuario_id)


@router.get("/{usuario_id}/permissoes")
def ver_permissoes(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    usuario = ServiceUsuario(db).buscar_por_id(usuario_id)
    perfil = db.query(ModelPerfil).filter(ModelPerfil.id == usuario.perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")

    dominio = criar_usuario_dominio(usuario.nome, usuario.email, perfil.nome)
    return {
        "usuario": str(dominio),
        "perfil": perfil.nome,
        "permissoes": dominio.get_permissoes(),
        "pode_deletar": dominio.pode_deletar(),
    }


@router.get("/{usuario_id}/menu")
def ver_menu(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    usuario = ServiceUsuario(db).buscar_por_id(usuario_id)
    perfil = db.query(ModelPerfil).filter(ModelPerfil.id == usuario.perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil nao encontrado")

    dominio = criar_usuario_dominio(usuario.nome, usuario.email, perfil.nome)
    return {
        "usuario": usuario.nome,
        "perfil": perfil.nome,
        "menu": dominio.exibir_menu(),
    }


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def atualizar_usuario(
    usuario_id: int,
    dados: UsuarioUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    return ServiceUsuario(db).atualizar(usuario_id, dados)


@router.delete("/{usuario_id}")
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_permission("usuarios:manage")),
):
    return ServiceUsuario(db).deletar(usuario_id)
