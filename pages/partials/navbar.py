from nicegui import ui, app


app.add_static_files("static", "./static")


class Navbar:

    def build(self):
        return (
            ui.image(source="static/logo.png")
            .style("width: 150px; height: 150px;")
            .on("click", lambda: ui.navigate.to("/"))
        )


class Footer:

    def build(self):
        return ui.label("Desenvolvido por: Ciência dos Dados").style(
            "flex: 1; align-items: center; justify-content: center; display: flex;"
        )
