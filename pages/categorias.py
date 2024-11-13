from nicegui import ui
from core.models import Categoria, get_session
from pages.partials.navbar import Navbar


class CategoriasPage:

    def build(self):
        self.modal_excluir_categoria()
        self.modal_nova_categoria()
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
                                    "Modelos",
                                    on_click=lambda: ui.navigate.to("/admin/modelos"),
                                    color="#8234E9",
                                    icon="insights",
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
                                    "Nova Categoria",
                                    on_click=self.dialog_nova_categoria.open,
                                )
                                ui.button(
                                    "Excluir Categoria",
                                    icon="delete",
                                    on_click=self.dialog_excluir_categoria.open,
                                    color="#F44336",
                                )
                        with ui.row().style(
                            "padding: 5px; width: 100%; align-items: center; justify-content: center;"
                        ):
                            self.__table_categoria()
            with ui.element("footer").style(
                "background-color: #8234E9; display: flex; flex-direction: column; flex: 0.1; margin-top: 5px;"
            ):
                ui.label("Portal-IA-PREMIX").style(
                    "flex: 1; align-items: center; justify-content: center; display: flex;"
                )

    @ui.refreshable
    def __table_categoria(self):
        categorias = self.lista_categorias()
        columns = [
            {
                "name": x.lower(),
                "label": x.capitalize().replace("_", " "),
                "field": x.lower(),
                "sortable": True,
            }
            for x in Categoria.__table__.columns.keys()
            if not x.lower() == "id"
        ]
        rows = [
            {
                column["name"]: getattr(categoria, column["name"])
                for column in columns
                if not column["name"] == "Id"
            }
            for categoria in categorias
        ]
        ui.table(
            columns=columns,
            rows=rows,
            row_key="nome",
            title="Categorias",
            pagination={"rowsPerPage": 10, "sortBy": "nome"},
        ).style("width:75%").add_slot(
            "body-cell-video_link",
            """
<q-td :props="props">
    <a :href="props.value">{{ props.value }}</a>
</q-td>
""",
        )

    def lista_categorias(self):
        with get_session() as session:
            return session.query(Categoria).all()

    @ui.refreshable
    def __categoria_select(self):
        categorias = self.lista_categorias()
        categorias = {categoria.id: categoria.nome for categoria in categorias}
        self.categoria_id = list(categorias.keys())[0] if categorias else None
        ui.select(
            categorias,
            label="Categoria",
            on_change=self.select_categoria,
            value=self.categoria_id,
        )

    def select_categoria(self, event):
        with get_session() as session:
            categoria = session.query(Categoria).filter_by(id=event.value).first()
            self.categoria_id = categoria.id

    def modal_excluir_categoria(self):
        with ui.dialog() as self.dialog_excluir_categoria, ui.card():
            with ui.column():
                self.__categoria_select()
                ui.label("Deseja realmente excluir a categoria?").style(
                    "font-size: 20px; margin-bottom: 20px;"
                )
                with ui.row():
                    ui.button("Sim", color="negative").on_click(
                        lambda: self.__excluir_categoria()
                    )
                    ui.button("Não", color="positive").on_click(
                        lambda: self.dialog_excluir_categoria.close()
                    )

    def modal_nova_categoria(self):
        with ui.dialog() as self.dialog_nova_categoria, ui.card():
            with ui.column():
                ui.label("Nova Categoria").style(
                    "font-size: 20px; margin-bottom: 20px;"
                )
                categoria_nome = ui.input("Nome")
                categoria_video = ui.input("Link do vídeo")
                with ui.row():
                    ui.button("Salvar", color="positive").on_click(
                        lambda: self.__salvar_categoria(
                            categoria_nome.value, categoria_video.value
                        )
                    )
                    ui.button("Cancelar", color="negative").on_click(
                        self.dialog_nova_categoria.close
                    )

    def __excluir_categoria(self):
        with get_session() as session:
            if not self.categoria_id is None:
                categoria = (
                    session.query(Categoria).filter_by(id=self.categoria_id).first()
                )
                session.delete(categoria)
                session.commit()
                self.categoria_id = None
                ui.notify("Categoria excluída com sucesso", type="positive")
                self.__table_categoria.refresh()
                self.__categoria_select.refresh()
                self.dialog_excluir_categoria.close()
            else:
                ui.notify("Selecione uma categoria", type="warning")

    def __salvar_categoria(self, categoria_nome, categoria_video):
        with get_session() as session:
            categoria_video = self.add_ember_link(categoria_video)
            categoria = Categoria(nome=categoria_nome, video_link=categoria_video)
            session.add(categoria)
            session.commit()
            ui.notify("Categoria salva com sucesso", type="positive")
            self.__table_categoria.refresh()
            self.__categoria_select.refresh()
            self.dialog_nova_categoria.close()

    def add_ember_link(self, link: str):
        if not "embed" in link.lower():
            return link.replace("watch?v=", "embed/").lower()
        return link
