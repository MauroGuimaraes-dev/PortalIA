from nicegui import ui, app
from pages.partials.navbar import Navbar
from core.models import Modelos, get_session, Categoria, Config


class IAModelsPage:

    def build(self, id: str):
        self.id_categoria = id
        with ui.element("div_container").style(
            "width: 100%; height: 100vh; margin: 0; padding: 0; display: flex; flex-direction: column;"
        ):
            with ui.element("div").style(
                "display: flex; flex-direction: column; flex: 0.7; align-items: center; justify-content: center;border-bottom: 2px solid #8234E9; margin-bottom: 5px;"
            ):
                Navbar().build()
            with ui.element("content").style(
                " display: flex; flex-direction: column; flex: 2;"
            ):
                with ui.row().style("width: 100%; display: flex; height: 100%;"):
                    with ui.column().style(
                        "flex: 1; height: 100%; display: flex; flex-direction: column"
                    ):
                        ui.label("Categorias").style(
                            "font-size: 20px; margin-top: 20px;"
                        )
                        with ui.scroll_area().style("flex: 1;"):
                            self.__modelos()
                    with ui.column().style("flex: 2;"):
                        ui.label("Video").style("font-size: 20px; margin-top: 20px;")
                        self.__video_modelo()
            with ui.element("footer").style(
                "background-color: orange; display: flex; flex-direction: column; flex: 0.1; margin-top: 5px;"
            ):
                ui.label("Portal-IA-PREMIX").style(
                    "flex: 1; align-items: center; justify-content: center; display: flex;"
                )

    @ui.refreshable
    def __video_modelo(self):
        ui.html(
            """<iframe width="750" height="450" src="{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>""".format(
                self.video_link_modelo
            )
        )

    def __select_video_modelo(self, video_link):
        self.video_link_modelo = video_link
        self.__video_modelo.refresh()

    def __modelos(self):
        with get_session() as session:
            video_link_modelo = (
                session.query(Config)
                .filter_by(key="video_modelos", is_active=1)
                .first()
            )
            self.video_link_modelo = (
                video_link_modelo.value if video_link_modelo else ""
            )
            modelos = (
                session.query(Modelos).filter_by(categoria_id=self.id_categoria).all()
            )
            if modelos:
                for modelo in modelos:
                    with ui.row().style(
                        "width: 100%; flex-direction: row; align-items: center; justify-content: center;"
                    ):
                        with ui.row().style(
                            "display: flex; flex-direction: row; width: 50%;"
                        ):
                            self.button_modelo(modelo)
            else:
                ui.label("Nenhum modelo encontrado").style(
                    "margin: 10px; padding: 10px; border-radius: 5px; flex: 0.9;"
                )

    def button_modelo(self, modelo: Modelos):
        ui.button(
            f"{modelo.nome}",
            color="#8234E9",
            on_click=lambda _: ui.navigate.to(modelo.ipaddress, new_tab=True),
        ).style("margin: 10px; padding: 10px; border-radius: 5px; flex: 0.9;")
        if modelo.video_link:
            ui.button(
                icon="smart_display",
                color="#8234E9",
                on_click=lambda _: self.__select_video_modelo(modelo.video_link),
            ).style("margin: 10px; padding: 10px; border-radius: 5px; flex: 0.1;")
        else:
            ui.button(icon="smart_display", color="#8234E9").style(
                "margin: 10px; padding: 10px; border-radius: 5px; flex: 0.1;",
            ).set_enabled(False)
