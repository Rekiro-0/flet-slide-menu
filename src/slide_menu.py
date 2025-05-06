from typing import List

import flet as ft
from flet.core.gradients import Gradient

class _ButtonsBar(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        icon_width: int,
        icon_height: int,
        gradient: Gradient,
        button_highlight: str, 
    ):
        self._icon_width = icon_width
        self._icon_height = icon_height
        self._button_highlight = button_highlight

        self._current_tab = None
        self._tabs_count = 0
        
        self._buttons_row = ft.Row(
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
        super().__init__(
            content=self._buttons_row,
            gradient=gradient,
            bottom=0,
            left=0,
            right=0,
            padding=0,
            expand=True,
        )

    def add_button(self, image_src: str) -> None:
        self._tabs_count += 1
        image = ft.Image(
            src=image_src,
            width=self._icon_width,
            height=self._icon_height,
        )
        tappable_container = ft.Container(
            content=image,
            width=self._icon_width+32,
        )
        gesture = ft.GestureDetector(
            content=tappable_container,
            mouse_cursor=ft.MouseCursor.CLICK,
            on_tap=self._on_tap,
            data=self._tabs_count-1,
        )
        stack = ft.Stack(controls=[gesture], alignment=ft.alignment.center)
        container_ = ft.Container(content=stack, expand=True, padding=8, border_radius=15)
        self._buttons_row.controls.append(container_)

        if self._current_tab is None:
            self._current_tab = 0
            self._buttons_row.controls[self._current_tab].bgcolor = self._button_highlight

    def _on_tap(self, event):
        new_button = event.control.data
        self.choose_button(new_button)
        self.on_frame_changed(new_button)

    def choose_button(self, new_button: int):		
        if self._current_tab == new_button:
            return
        buttons = self._buttons_row.controls
        buttons[self._current_tab].bgcolor = None
        buttons[self._current_tab].update()
        self._current_tab = new_button
        buttons[self._current_tab].bgcolor = self._button_highlight
        buttons[self._current_tab].update()

    @staticmethod
    def on_frame_changed(frame_number: int) -> None:
        pass

class _ContentArea(ft.GridView):
    def __init__(self, page: ft.Page, autoscroll_duration: int):
        self._autoscroll_duration = autoscroll_duration
        super().__init__(
            expand=True,
            runs_count=1,
            horizontal=True,
            child_aspect_ratio=page.height/page.width,
            spacing=0,
            run_spacing=0,
            padding=0, 
            cache_extent=500, #eliminates white  areas when sliding
        )

        self._prev_pixels = 0
        self._page = page
        self._current_frame = 0
        self.on_scroll = self._on_scroll
        self._key_counter = 0

    def add_frame_content(self, frame: ft.Stack):
        frame.key = f"frame_{self._key_counter}"
        self._key_counter += 1
        self.controls.append(frame)

    def scroll_to_frame(self, frame_number):
        self.scroll_to(
            offset=frame_number*self._page.width,
            duration=self._autoscroll_duration,
        )
        self.update()



    def _on_scroll(self, event:  ft.OnScrollEvent):
        if event.event_type == 'end':
            if self._prev_pixels == event.pixels:
                return
            new_frame = (event.pixels + self._page.width/2) // self._page.width
            self.scroll_to(
                offset=new_frame*self._page.width,
                duration=350,
            )
            self._prev_pixels = new_frame*self._page.width
            self.update()
        elif event.event_type == 'update':
            frame = int( (event.pixels + self._page.width/2) // self._page.width )
            if self._current_frame != frame:
                self._current_frame = frame
                self.on_frame_changed(frame)

    @staticmethod
    def on_frame_changed(new_frame: int):
        pass

class SlideNavigation(ft.Stack):
    def __init__(
        self,
        page: ft.Page,
        icon_width: int = 36,
        icon_height: int = 36,
        menu_gradient: Gradient = None,
        button_highlight: str = '#FFFFFF',
        autoscroll_duration: int = 350,
    ):
        self._buttons_bar = _ButtonsBar(
            page=page,
            icon_width=icon_width,
            icon_height=icon_height,
            gradient=menu_gradient,
            button_highlight=button_highlight,
        )
        self._conten_area = _ContentArea(
            page=page,
            autoscroll_duration=autoscroll_duration,
        )
        super().__init__(
            controls=[self._conten_area, self._buttons_bar],
            expand=True
        )
        self._buttons_bar.on_frame_changed = lambda frame: self._conten_area.scroll_to_frame(frame)
        self._conten_area.on_frame_changed = lambda frame: self._buttons_bar.choose_button(frame)

    def add_frame(self, frame: ft.Stack, icon_src: str):
        self._conten_area.add_frame_content(frame)
        self._buttons_bar.add_button(icon_src)

    def scroll_to_frame(self, frame_number: int):
        self._conten_area.scroll_to_frame(frame_number)