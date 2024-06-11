import webbrowser

import aiohttp
import flet as ft
import requests


class State:
    x: float
    y: float


state = State()
lista_videos = []


def extract_redirect_url(html_content):
    start_index = html_content.find("URL") + len("URL=")
    end_index = html_content.find("'", start_index)
    redirect_url = html_content[start_index:end_index]
    return redirect_url


def main(page: ft.Page):
    global lista_videos
    page.title = "Routes Example"
    # link = ft.TextField(label="link do video: ", value='', on_change=textbox_changed)
    pt = ft.Text('Download em Andamento...')
    cg = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value='/download_and_redirect', label='Video'),
            ft.Radio(value='/download_and_redirectmp3', label='Audio')
        ]))
    lv = ft.ListView(expand=1, spacing=10, item_extent=50,
                     controls=[ft.Row(controls=[ft.Text('Apos escolher uma opção acima clique no icone '),
                                                ft.Icon(ft.icons.SAVE)]),
                               ])
    url = ft.Text()

    def textbox_changed(e):
        url.value = e.control.value
        page.update()

    def clear_lista(e):
        lv.clean()
        page.update()

    def limpar_field(e):
        link.value = ''
        url.value = ''
        page.update()

    def limpar_arquivos(e):
        url = 'http://127.0.0.1:8000/excluir_arquivos'
        response = requests.delete(url)
        if response.status_code == 200:
            messagem = response.json()
            print(messagem)

    link = ft.TextField(label="link da playlist: ", value='', on_change=textbox_changed, on_focus=limpar_field)

    async def button_clicked(e):
        global url
        try:
            ytlink = e.control.content.value
            # ytlink = url_video
            api = f'http://127.0.0.1:8000{cg.value}?'
            req = f'{api}video_url={ytlink}'
            print(req)

            async with aiohttp.ClientSession() as session:
                async  with session.post(f'{api}video_url={ytlink}') as response:
                    if response.status == 200:
                        html_content = await response.text()
                        redirect_url = extract_redirect_url(html_content)
                        webbrowser.open(redirect_url)
                        pt.value = 'Baixe seu arquivo'
                        page.update()
                    else:
                        print('A solicitação nao foi bem sucedida')
        except Exception as ex:
            print(f"Erro durante a solicitação: {ex}")
            pass

    async def download_direct(url: str):
        try:
            ytlink = url
            api = f'http://127.0.0.1:8000{cg.value}?'
            req = f'{api}video_url={ytlink}'
            print(req)

            async with aiohttp.ClientSession() as session:
                async  with session.post(f'{api}video_url={ytlink}') as response:
                    if response.status == 200:
                        html_content = await response.text()
                        redirect_url = extract_redirect_url(html_content)
                        webbrowser.open(redirect_url)
                        pt.value = 'Baixe seu arquivo'
                        page.update()
                    else:
                        print('A solicitação nao foi bem sucedida')
        except Exception as ex:
            print(f"Erro durante a solicitação: {ex}")
            pass

    async def button_list(e):
        global options
        try:
            playlist_url = link.value
            playlist_url = playlist_url.replace(':', '%3A')
            playlist_url = playlist_url.replace('/', '%2F')
            playlist_url = playlist_url.replace('=', '%3D')
            playlist_url = playlist_url.replace('?', '%3F')
            playlist_url = playlist_url.replace('&', '%26')

            url1 = f'http://127.0.0.1:8000/playlist3?playlist_url={playlist_url}'
            print(url1)
            response = requests.post(url1)
            if response.status_code == 200:
                videos = response.json()
                for video in videos:
                    lista_videos.append(video)

                for video in lista_videos:
                    url2 = str(video['url'])
                    lv.controls.append(
                        ft.Row(
                            controls=[
                                ft.Text(video['title']),
                                ft.IconButton(ft.icons.SAVE,
                                              on_click=button_clicked,
                                              content=ft.Text(value=url2),
                                              tooltip='Clique no botao para baixar')
                            ]
                        )
                    )
                page.update()
            else:
                print(f'A solicitação nao foi bem sucedida: erro {response.status_code}')
        except Exception as ex:
            print(f"Erro durante a solicitação: {ex}")
            pass

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"),
                              bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Visit Store",
                                      on_click=lambda _: page.go("/store")),
                    ft.ElevatedButton("Visit About",
                                      on_click=lambda _: page.go("/about")),
                    ft.ElevatedButton("Visit Counter",
                                      on_click=lambda _: page.go("/counter")),
                ],
            ))
        if page.route == "/store":
            page.views.append(
                ft.View("/store", [
                    ft.AppBar(title=ft.Text("Store"),
                              bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Go Home",
                                      on_click=lambda _: page.go("/")),
                    ft.ElevatedButton('Limpar arquivos', on_click=limpar_arquivos)

                ]))
        elif page.route == "/about":
            page.views.append(
                ft.View(
                    "/about",
                    [
                        ft.AppBar(title=ft.Text("About"),
                                  bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home",
                                          on_click=lambda _: page.go("/")),
                        ft.TextField(label="link do video: ", value='', on_change=textbox_changed,on_focus=limpar_field),
                        ft.Row(controls=[
                            ft.Text('Escolha uma opção:'),
                            cg
                        ]),
                        pt,
                        ft.IconButton(ft.icons.SAVE, on_click=button_clicked, content=ft.Text(value=url))
                    ],
                ))

        elif page.route == "/counter":

            page.views.append(
                ft.View(
                    "/counter",
                    [
                        ft.AppBar(title=ft.Text("Counter"),
                                  bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home",
                                          on_click=lambda _: page.go("/")),
                        link,
                        ft.Row(
                            controls=[
                                ft.ElevatedButton('Carregar lista', on_click=button_list),
                                ft.ElevatedButton('Limpar lista', on_click=clear_lista),
                            ]
                        ),
                        ft.Row(controls=[
                            ft.Text('Escolha uma opção:'),
                            cg
                        ]),
                        lv
                    ]
                ),
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
