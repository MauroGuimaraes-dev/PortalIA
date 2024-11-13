from nicegui import ui, app
from pages.partials.navbar import Navbar
from core.models import Categoria, Modelos, get_session, Config


class HomePage:

    def build(self):

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
                        with ui.scroll_area().style("flex: 1;"):
                            self.__categorias()
                    with ui.column().style("flex: 2;"):
                        self.__video_home()
            with ui.element("footer").style(
                "background-color: #8234E9; display: flex; flex-direction: column; flex: 0.1; margin-top: 5px;"
            ):
                ui.label("Portal-IA-PREMIX").style(
                    "flex: 1; align-items: center; justify-content: center; display: flex;"
                )

    @ui.refreshable
    def __video_home(self):
        ui.html(
            """<iframe width="750" height="450" src="{}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>""".format(
                self.video_link_home
            )
        )

    def __select_video_home(self, video_link):
        self.video_link_home = video_link
        self.__video_home.refresh()

    def __categorias(self):
        with get_session() as session:
            video_link_home = (
                session.query(Config)
                .filter_by(key="video_categorias", is_active=1)
                .first()
            )
            self.video_link_home = video_link_home.value if video_link_home else ""
            categorias = session.query(Categoria).all()
            for categoria in categorias:
                with ui.row().style(
                    "width: 100%; flex-direction: row; align-items: center; justify-content: center;"
                ):
                    with ui.row().style(
                        "display: flex; flex-direction: row; width: 50%;"
                    ):
                        self.button_categoria(categoria)

    def button_categoria(self, categoria: Categoria):
        ui.button(
            f"{categoria.nome}",
            on_click=lambda _: ui.navigate.to(f"/categoria/{categoria.id}"),
            color="#8234E9",
        ).style("margin: 10px; padding: 10px; border-radius: 5px; flex: 0.9;")
        if categoria.video_link:
            ui.button(icon="smart_display", color="#8234E9").on(
                "click", lambda: self.__select_video_home(categoria.video_link)
            ).style("margin: 10px; padding: 10px; border-radius: 5px; flex: 0.1;")
        else:
            ui.button(icon="smart_display", color="#8234E9").style(
                "margin: 10px; padding: 10px; border-radius: 5px; flex: 0.1;"
            ).set_enabled(False)
