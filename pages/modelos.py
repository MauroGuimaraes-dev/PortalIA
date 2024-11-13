from nicegui import ui
from core.models import Modelos, Categoria, get_session
from pages.partials.navbar import Navbar


class ModelosPage:

    def build(self):
        self.modal_excluir_modelo()
        self.modal_nova_modelo()
        with ui.element("div_container").style(
            "width: 100%; height: 100vh; margin: 0; padding: 0; display: flex; flex-direction: column;"
        ):
            with ui.element("div").style(
                "display: flex; flex-direction: column; flex: 0.7; align-items: center; justify-content: center;border-bottom: 2px solid #8234E9; margin-bottom: 5px;"
            ):
                Navbar().build()
            with ui.element("content").style(
                " display: flex; flex-direction: column; flex: 2; align-items: center; justify-content: center;"
            ):
                with ui.row().style("width: 100%; display: flex; height: 100%;"):
                    with ui.column().style(
                        "flex: 1; height: 100%; display: flex; flex-direction: column ; padding: 10px; align-items: center"
                    ):
                        ui.label("Menu").style("font-size: 20px; margin-top: 20px;")
                        with ui.column():
                            with ui.row().style("width: 100%; display: flex;"):
                                ui.button(
                                    "Home",
                                    on_click=lambda: ui.navigate.to("/"),
                                    color="#8234E9",
                                    icon="home",
                                ).style("flex: 1;").props("align=left")
                            with ui.row().style("width: 100%; display: flex;"):
                                ui.button(
                                    "Categorias",
                                    on_click=lambda: ui.navigate.to(
                                        "/admin/categorias"
                                    ),
                                    color="#8234E9",
                                    icon="workspaces",
                                ).style("flex: 1;").props("align=left")
                            with ui.row().style("width: 100%; display: flex;"):

                                ui.button(
                                    "Configurações",
                                    on_click=lambda: ui.navigate.to("/admin/config"),
                                    color="#8234E9",
                                    icon="settings",
                                ).style("flex: 1;").props("align=left")
                    with ui.column().style("flex: 5;"):
                        with ui.row().style(
                            "width: 100%; display: flex; height: 100%; background-color: #8234E9; padding: 10px; align-items: center; justify-content: end;"
                        ):
                            with ui.button_group():
                                ui.button(
                                    "Nova modelo",
                                    on_click=self.dialog_nova_modelo.open,
                                )
                                ui.button(
                                    "Excluir modelo",
                                    icon="delete",
                                    on_click=self.dialog_excluir_modelo.open,
                                    color="#F44336",
                                )
                        with ui.row().style(
                            "padding: 5px; width: 100%; align-items: center; justify-content: center;"
                        ):
                            self.__table_modelo()
            with ui.element("footer").style(
                "background-color: #8234E9; display: flex; flex-direction: column; flex: 0.1; margin-top: 5px;"
            ):
                ui.label("Portal-IA-PREMIX").style(
                    "flex: 1; align-items: center; justify-content: center; display: flex;"
                )

    def get_categoria(self) -> dict:
        with get_session() as session:
            categoria = session.query(Categoria).all()
        return {categoria.id: categoria.nome for categoria in categoria}

    @ui.refreshable
    def __table_modelo(self):
        modelos = self.lista_modelos()
        categorias = self.get_categoria()
        columns = [
            {
                "name": x.lower(),
                "label": x.capitalize().replace("_", " ").replace(" id", ""),
                "field": x.lower(),
                "sortable": True,
            }
            for x in Modelos.__table__.columns.keys()
            if not x.lower() == "id"
        ]
        rows = [
            {
                column["name"]: (
                    getattr(modelo, column["name"])
                    if not column["name"] == "categoria_id"
                    else categorias.get(getattr(modelo, column["name"]))
                )
                for column in columns
                if not column["name"] == "Id"
            }
            for modelo in modelos
        ]
        ui.table(
            columns=columns,
            rows=rows,
            row_key="nome",
            title="modelos",
            pagination={"rowsPerPage": 10, "sortBy": "nome"},
        ).style("width:75%").add_slot(
            "body-cell-video_link",
            """
<q-td :props="props">
    <a :href="props.value">{{ props.value }}</a>
</q-td>
""",
        )

    def lista_modelos(self):
        with get_session() as session:
            return session.query(Modelos).all()

    @ui.refreshable
    def __modelo_select(self):
        modelos = self.lista_modelos()
        modelos = {modelo.id: modelo.nome for modelo in modelos}
        self.modelo_id = list(modelos.keys())[0] if modelos else None
        ui.select(
            modelos,
            label="modelo",
            on_change=self.select_modelo,
            value=self.modelo_id,
        )

    def __categoria_select(self):
        with get_session() as session:
            categorias = session.query(Categoria).all()
            self.categorias = {categoria.id: categoria.nome for categoria in categorias}
        self.categoria_id = list(self.categorias.keys())[0]
        ui.select(
            self.categorias,
            label="Categoria",
            on_change=self.select_categoria,
            value=self.categoria_id,
        )

    def select_categoria(self, event: ui.select):
        self.categoria_id = event.value

    def select_modelo(self, event: ui.select):
        with get_session() as session:
            modelo = session.query(Modelos).filter_by(id=event.value).first()
            self.modelo_id = modelo.id

    def modal_excluir_modelo(self):
        with ui.dialog() as self.dialog_excluir_modelo, ui.card():
            with ui.column():
                self.__modelo_select()
                ui.label("Deseja realmente excluir a modelo?").style(
                    "font-size: 20px; margin-bottom: 20px;"
                )
                with ui.row():
                    ui.button("Sim", color="negative").on_click(
                        lambda: self.__excluir_modelo()
                    )
                    ui.button("Não", color="positive").on_click(
                        lambda: self.dialog_excluir_modelo.close()
                    )

    def modal_nova_modelo(self):
        with ui.dialog() as self.dialog_nova_modelo, ui.card():
            with ui.column():
                ui.label("Novo modelo").style("font-size: 20px; margin-bottom: 20px;")
                modelo_nome = ui.input("Nome")
                modelo_ipaddress = ui.input("IP Address")
                modelo_video = ui.input("Link do vídeo")
                self.__categoria_select()
                with ui.row():
                    ui.button("Salvar", color="positive").on_click(
                        lambda: self.__salvar_modelo(
                            modelo_nome.value,
                            modelo_video.value,
                            modelo_ipaddress.value,
                        )
                    )
                    ui.button("Cancelar", color="negative").on_click(
                        self.dialog_nova_modelo.close
                    )

    def __excluir_modelo(self):
        with get_session() as session:
            if not self.modelo_id is None:
                modelo = session.query(Modelos).filter_by(id=self.modelo_id).first()
                session.delete(modelo)
                session.commit()
                self.modelo_id = None
                ui.notify("modelo excluída com sucesso", type="positive")
                self.__table_modelo.refresh()
                self.__modelo_select.refresh()
                self.dialog_excluir_modelo.close()
            else:
                ui.notify("Selecione uma modelo", type="warning")

    def __salvar_modelo(self, modelo_nome, modelo_video, modelo_ipaddress):
        with get_session() as session:
            modelo_video = self.add_ember_link(modelo_video)
            modelo = Modelos(
                nome=modelo_nome,
                video_link=modelo_video,
                ipaddress=modelo_ipaddress,
                categoria_id=self.categoria_id,
            )
            session.add(modelo)
            session.commit()
            ui.notify("modelo salva com sucesso", type="positive")
            self.__table_modelo.refresh()
            self.__modelo_select.refresh()
            self.dialog_nova_modelo.close()

    def add_ember_link(self, link: str):
        if not "embed" in link.lower():
            return link.replace("watch?v=", "embed/").lower()
        return link
