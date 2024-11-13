from nicegui import ui, app
from pages.iamodels import IAModelsPage
from pages.home import HomePage
from pages.categorias import CategoriasPage
from pages.modelos import ModelosPage
from pages.configuracoes import ConfiguracoesPage


@ui.page("/")
def page_home():
    ui.page_title("Home Page")
    ui.dark_mode().enable()
    ui.query(".nicegui-content").classes("p-0")
    HomePage().build()


@ui.page("/categoria/{id}")
def page_iamodels(id: str):
    ui.query(".nicegui-content").classes("p-0")
    ui.dark_mode().enable()
    IAModelsPage().build(id)


@ui.page("/admin")
def page_admin():
    ui.navigate.to("/admin/categorias")
    # ui.page_title("Admin Page")
    # ui.query(".nicegui-content").classes("p-0")
    # ui.dark_mode().enable()
    # AdminPage().build()


@ui.page("/admin/categorias")
def page_admin_categorias():
    ui.page_title("Admin Categoria")
    ui.query(".nicegui-content").classes("p-0")
    ui.dark_mode().enable()
    CategoriasPage().build()


@ui.page("/admin/modelos")
def page_admin_modelos():
    ui.page_title("Admin Modelos")
    ui.query(".nicegui-content").classes("p-0")
    ui.dark_mode().enable()
    ModelosPage().build()


@ui.page("/admin/config")
def page_admin_config():
    ui.page_title("Admin Configurações")
    ui.query(".nicegui-content").classes("p-0")
    ui.dark_mode().enable()
    ConfiguracoesPage().build()


ui.run()
