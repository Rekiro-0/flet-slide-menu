import flet as ft

def main(page: ft.Page):
    page.padding = 0
    if page.platform == ft.PagePlatform.WINDOWS:
        page.window.width = 400
        page.window.height = 750
    page.update()

    grid = ft.GridView(
        expand=1,
        runs_count=1,
        horizontal=True,
        child_aspect_ratio=page.height/page.width,
        spacing=0,
        run_spacing=0,
        padding=0,
    )

    page.add(grid)

    for i in range(0, 3):
        grid.controls.append(
            ft.Image(
                #src=f'assets/backgrounds/{i}.jpg',
                src=f'https://picsum.photos/300/600?random={i}',
                fit=ft.ImageFit.COVER,
                #border_radius=ft.border_radius.all(10),
                key=f'{i}'
            )
        )
    
    prev_pixels = 0
    frame_count = 3
    def on_scroll(event:  ft.OnScrollEvent):
        if event.event_type == 'end':
            nonlocal prev_pixels
            if prev_pixels == event.pixels:
                return
            new_frame = (event.pixels + page.width//2) // page.width
            grid.scroll_to(
                offset=new_frame*page.width,
                duration=350,
            )
            prev_pixels = new_frame*page.width
            grid.update()
    grid.on_scroll = on_scroll

    page.update()

ft.app(main)