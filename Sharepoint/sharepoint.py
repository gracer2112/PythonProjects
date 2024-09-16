from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
#from office365.sharepoint.pages.site_page import SitePage

def authenticate(site_url, username, password):
    ctx_auth = AuthenticationContext(site_url)
    if ctx_auth.acquire_token_for_user(username, password):
        ctx = ClientContext(site_url, ctx_auth)
        print("Autenticação bem-sucedida")
        return ctx
    else:
        print("Erro na autenticação:", ctx_auth.get_last_error())
        return None

def create_page(ctx, page_name, page_title):
    pages_library = ctx.web.lists.get_by_title("Site Pages")
    ctx.load(pages_library)
    ctx.execute_query()

    new_page = SitePage.create(ctx, page_name)
    new_page.page_layout_type = "Article"
    new_page.title = page_title
    new_page.save()
    ctx.execute_query()
    print(f"Página '{page_title}' criada com sucesso.")

def add_content_to_page(ctx, page_name, content):
    pages_library = ctx.web.lists.get_by_title("Site Pages")
    ctx.load(pages_library)
    ctx.execute_query()

    page_item = pages_library.items.filter(f"FileLeafRef eq '{page_name}'").get().execute_query()
    page = SitePage(ctx, page_item[0].properties["FileRef"])
    page.set_text(content)
    page.save()
    ctx.execute_query()
    print(f"Conteúdo adicionado à página '{page_name}'.")

# Configurações
site_url = 'https://fs200dev.sharepoint.com/sites/CooperativaIntegrada-200DEV'
username = 'erica.araujo@200dev.com'
password = 'Afterimage@1'

# Autenticação
ctx = authenticate(site_url, username, password)
if ctx:
    web = ctx.web
    ctx.load(web)
    ctx.execute_query()
    print("Web title: {0}".format(web.properties['Title']))
    # Criar e adicionar conteúdo à página
    # create_page(ctx, "nova_pagina.aspx", "Título da Nova Página")
    # add_content_to_page(ctx, "nova_pagina.aspx", "<h1>Bem-vindo à Nova Página</h1>")