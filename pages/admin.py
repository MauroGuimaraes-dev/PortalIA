from nicegui import ui, app
from pages.partials.navbar import Navbar
from core.models import User, Modelos, get_session


class AdminPage:

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
                ...

            with ui.element("footer").style(
                "background-color: #8234E9; display: flex; flex-direction: column; flex: 0.1; margin-top: 5px;"
            ):
                ui.label("Portal-IA-PREMIX").style(
                    "flex: 1; align-items: center; justify-content: center; display: flex;"
                )

    def __form_modelo(self):
        # Formulário de cadastro de modelos
        with ui.column().style(
            "align-items: center; justify-content: center; display: flex; flex-direction: column; width: 100%;"
        ):
            self.nome_modelo = ui.input(label="Nome do Modelo").style("width: 20%")
            self.ipaddress = ui.input(label="IP Address").style("width: 20%")
            self.video_link = ui.input(label="Video Link").style("width: 20%")
            with ui.row().style("width: 20%; align-items: end;"):
                self.__categorias()
                ui.button(icon="add_circle_outline").props(
                    "outline color=purple"
                ).style("flex: 1; margin-left: 5px;")
            ui.button("Salvar", icon="save").on("click", self.__salvar_modelo).props(
                "outline color=purple"
            ).style("margin-top: 20px;")

    def __salvar_modelo(self):
        with get_session() as session:
            modelo = Modelos(
                nome=self.nome_modelo.value,
                ipaddress=self.ipaddress.value,
                video_link=self.video_link.value,
                categoria_id=self.categorias.value,
            )
            session.add(modelo)
            session.commit()
            ui.notification("Modelo salvo com sucesso!", type="positive")
            self.nome_modelo.value = ""
            self.ipaddress.value = ""
            self.video_link.value = ""
            self.categorias.value = ""
