from nicegui import ui
from core.models import Config, get_session
from pages.partials.navbar import Navbar


class ConfiguracoesPage:

    def build(self):
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
                                    "Categorias",
                                    on_click=lambda: ui.navigate.to(
                                        "/admin/categorias"
                                    ),
                                    color="#8234E9",
                                    icon="workspaces",
                                ).style("flex: 1;").props("align=left")
                    with ui.column().style("flex: 5; display: flex;"):
                        with ui.row().style(
                            "padding: 5px; width: 100%; flex-direction: row; align-items: center; justify-content: center; display: flex;"
                        ):
                            self.__table_config()
            with ui.element("footer").style(
                "background-color: #8234E9; display: flex; flex-direction: column; flex: 0.1; margin-top: 5px;"
            ):
                ui.label("Portal-IA-PREMIX").style(
                    "flex: 1; align-items: center; justify-content: center; display: flex;"
                )

    @ui.refreshable
    def __table_config(self):
        configs = self.lista_config()
        with ui.column().style("width: 80%; display: flex; flex-direction: column;"):
            for config in configs:
                with ui.row().style(
                    "width: 100%; display: flex; justify-content: center; align-items: center;"
                ):
                    self.button_config(config)

    def lista_config(self):
        with get_session() as session:
            return session.query(Config).all()

    def button_config(self, config: Config):
        ui.label(
            " ".join([x.capitalize() for x in config.key.replace("_", " ").split(" ")])
        ).style("flex: 0.3;")
        value = ui.input(value=config.value).style("flex: 1;")
        ui.button(icon="save", text="").on_click(
            lambda _: self.__update_config(value, config)
        ).style("flex: 0.05;")

    def __update_config(self, value: ui.input, config: Config):
        with get_session() as session:
            config_ = session.query(Config).filter_by(id=config.id).first()
            config_.value = value.value
            session.commit()
            ui.notify("Configuração atualizada com sucesso", type="success")
            self.__table_config.refresh()
