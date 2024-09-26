from time import sleep
import flet as ft


def main(page: ft.Page):
    page.title = "YouTube Clone"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.spacing = 0   
    
    
    def create_video_card(title, channel, views, image_url):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Image(src=image_url, fit=ft.ImageFit.COVER),
                    height=180,
                    width=320,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Text(title, style=ft.TextThemeStyle.BODY_MEDIUM, weight=ft.FontWeight.BOLD),
                        ft.Text(f"{channel} • {views} views", style=ft.TextThemeStyle.BODY_SMALL),
                    ]),
                    padding=ft.padding.all(10),
                ),
            ]),
            width=320,
            height=280,
            border_radius=ft.border_radius.all(10),
            ink=True,
            on_click=lambda _: print(f"Clicked on {title}"),
        )

    def search(e):
        print(f"Searching for: {search_field.value}")
        
    # def toggle_sidebar(e):
    #     sidebar_container.visible = not sidebar_container.visible
    #     if sidebar_container.visible:
    #         sidebar.width = lambda: page.width * 0.2
    #     else:
    #         sidebar.width = 0
    #     page.update()
    
    def sidebar_width():
        return min(page.width * 0.2, 100)

    def toggle_sidebar(e):
        sidebar_container.visible = not sidebar_container.visible
        sidebar.width = sidebar_width() if sidebar.width == 0 else 0
        page.update()
        
        
    # Main Content
    video_grid = ft.GridView(
        expand=True,
        runs_count=5,
        max_extent=320,
        child_aspect_ratio=1, 
        spacing=10,
        run_spacing=10,
    )

    for i in range(20):
        video_grid.controls.append(
            create_video_card(
                f"Video Title {i+1}",
                f"Channel {i+1}",
                f"{(i+1)*1000}",
                f"https://picsum.photos/320/180?random={i+1}"
            )
        )

    # App Bar
    search_field = ft.TextField(hint_text="Search", expand=True, on_submit=search)
    
    app_bar = ft.AppBar(
        leading=ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar),
        leading_width=40,
        title=ft.Text("YouTube"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.Row([
                    search_field,
                    ft.IconButton(ft.icons.SEARCH, on_click=search),
                ]),
                width=400,
                padding=10,
            ),
            ft.IconButton(ft.icons.NOTIFICATIONS),
            ft.IconButton(ft.icons.ACCOUNT_CIRCLE),
        ],
    )
    
    page.add(app_bar)
    
    
    # Sidebar
    sidebar_container = ft.Column(
        controls=[
            ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                min_width=70,
                min_extended_width=200,   
                group_alignment=-0.9,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.icons.HOME_OUTLINED, 
                        selected_icon=ft.icons.HOME, 
                        label="Home"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.EXPLORE_OUTLINED, 
                        selected_icon=ft.icons.EXPLORE, 
                        label="Explore"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.SUBSCRIPTIONS_OUTLINED, 
                        selected_icon=ft.icons.SUBSCRIPTIONS, 
                        label="Subscriptions"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.VIDEO_LIBRARY_OUTLINED, 
                        selected_icon=ft.icons.VIDEO_LIBRARY, 
                        label="Library"
                    ),
                ],
                expand=True,
            )
        ], visible=False
    )
    
    
    page.update()
    
    sidebar = ft.Container(
        content=sidebar_container,
        # bgcolor=ft.colors.SURFACE_VARIANT,
        width=0,
        animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
    )

    # Layout
    content = ft.Container(
        content=video_grid,
        expand=True,
    )

    main_area = ft.Row([
        sidebar,
        ft.VerticalDivider(width=1),
        content,
    ], expand=True)

    page.add(
        app_bar,
        main_area
    )

    page.update()


ft.app(main)
