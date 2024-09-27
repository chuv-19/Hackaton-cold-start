import os
from time import sleep
import flet as ft


def main(page: ft.Page):
    page.title = "YouTube Clone"
    page.theme_mode = ft.ThemeMode.DARK
    # page.bgcolor = ft.colors.GREY_900
    page.padding = 10
    page.spacing = 0
    
    pgw = page.width
    pgh = page.height
    
    thumbnail_dir = "assets"
    thumbnail_files = [f for f in os.listdir(thumbnail_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]

    def is_mobile():
        return page.platform in (ft.PagePlatform.IOS, ft.PagePlatform.ANDROID)

    if is_mobile():
        page.navigation_bar = ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
                    ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                    ft.NavigationBarDestination(
                        icon=ft.icons.SUBSCRIPTIONS, label="Subscriptions"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.icons.VIDEO_LIBRARY, label="Library"
                    ),
                ],
            )
        page.adaptive = True
        
    def create_layout():
        return ft.Column([
            create_app_bar(),
            ft.Row([
                sidebar if not is_mobile() else ft.Container(width=0),
                ft.VerticalDivider(width=1),
                ft.Column([page.route_view], expand=True, scroll=ft.ScrollMode.AUTO),
            ], expand=True),
            ft.NavigationBar(
                destinations=[
                    ft.NavigationDestination(icon=ft.icons.HOME, label="Home"),
                    ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
                    ft.NavigationDestination(icon=ft.icons.SUBSCRIPTIONS, label="Subscriptions"),
                    ft.NavigationDestination(icon=ft.icons.VIDEO_LIBRARY, label="Library"),
                ],
            ) if is_mobile() else None,
        ])

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        create_app_bar(),
                        create_main_content(),
                    ],
                )
            )
        elif page.route == "/video":
            page.views.append(
                ft.View(
                    "/video",
                    [
                        create_app_bar(),
                        create_video_page(),
                    ],
                )
            )
        elif page.route == "/history":
            page.views.append(
                ft.View(
                    "/history",
                    [
                        create_app_bar(),
                        create_history_page(),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    def create_main_content():
        return ft.Row([
            sidebar,
            video_grid,
        ])

    def create_video_page():
        return ft.Row([
            sidebar,
            ft.Container(
                content=ft.Column([
                    ft.AspectRatio(
                        ratio=16/9,
                        content=ft.Image(
                            src="https://picsum.photos/1280/720",
                            fit=ft.ImageFit.COVER,
                        ),
                    ),
                    ft.ListTile(
                        title=ft.Text("Video Title", size=18, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text("Channel Name • 1M views • 2 days ago"),
                    ),
                    ft.Row([
                        ft.ElevatedButton("Like", icon=ft.icons.THUMB_UP),
                        ft.ElevatedButton("Dislike", icon=ft.icons.THUMB_DOWN),
                        ft.ElevatedButton("Share", icon=ft.icons.SHARE),
                        ft.ElevatedButton("Download", icon=ft.icons.DOWNLOAD),
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                    ft.Divider(),
                    ft.Text("Comments", size=18, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.ListView([
                        ft.ListTile(
                            leading=ft.CircleAvatar(foreground_image_src="https://picsum.photos/50"),
                            title=ft.Text("User Name"),
                            subtitle=ft.Text("This is a comment on the video."),
                        ) for _ in range(10)
                    ], height=300),
                ], spacing=10),
                padding=20,
            ),
        ])

    def create_history_page():
        return ft.Column([
            ft.Text("History Page"),
            ft.ElevatedButton("Go back", on_click=lambda _: page.go("/")),
        ])
        
    def create_app_bar():
        return ft.AppBar(title=ft.Row(
            [
                ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar)
                if not is_mobile() else ft.Container(width=0),
                ft.Icon(ft.icons.PLAY_CIRCLE_FILLED, color=ft.colors.RED_500),
                ft.Text("YouTube" if not is_mobile() else "YT"),
            ]
        ),
        
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.Row(
                    [
                        search_field,
                        ft.IconButton(ft.icons.SEARCH, on_click=search),
                    ]
                ),
                # width=400 if page.platform != ft.PagePlatform.ANDROID or page.platform != ft.PagePlatform.IOS else 10,
                # width=page.width * 0.2 if is_mobile() else min(page.width*0.5, 400),
                
                padding=10,
            ),
            ft.IconButton(ft.icons.NOTIFICATIONS),
            ft.IconButton(ft.icons.ACCOUNT_CIRCLE),
        ],
    )
            

    def create_video_card(title, channel, views, image_url):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(src=(f"https://fastly.picsum.photos/id/536/536/354.jpg?hmac=Vg6xur8DUhCMZUuiomMuIllitzm08L_Ay511YycV4k0"), fit=ft.ImageFit.COVER),
                        height=180 if not is_mobile() else page.height/3,
                        width=340 if not is_mobile() else page.width*0.95,
                        border_radius=ft.border_radius.all(10),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    title,
                                    style=ft.TextThemeStyle.BODY_MEDIUM,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    f"{channel} • {views} views",
                                    style=ft.TextThemeStyle.BODY_SMALL,
                                ),
                                
                            ],
                            spacing=0
                        ),
                        
                    ),
                ],
                spacing=10,
                
            ),
            ink=True,
            border_radius=ft.border_radius.all(10),
            on_click=lambda _: [print(f"Clicked on {title}"), page.go("/video")]
        )
        
    def create_search_field():
        return ft.TextField(
            hint_text="Search",
            expand=True,
            on_submit=search,
            width=pgw*0.3 if page.width < 600 else min(page.width * 0.3, 400)
        )


    def search(e):
        print(f"Searching for: {e.data}")

    # def toggle_sidebar(e):
    #     sidebar_container.visible = not sidebar_container.visible
    #     if sidebar_container.visible:
    #         sidebar.width = lambda: page.width * 0.2
    #     else:
    #         sidebar.width = 0
    #     page.update()
    
    def sdbr_width():
        min(page.width * 0.2, 100)

    def toggle_sidebar(e):
        sidebar_container.visible = not sidebar_container.visible
        sidebar.width = sdbr_width() if sidebar.width == 0 else 0
        page.update()
        
    def calculate_max_extent(sidebar_visible):
        if is_mobile():
            return 600
        else:
            sidebar_width = 240 if sidebar_visible else 0
            return 390 - (260 - sidebar_width)
    

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
                        label="Home",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.EXPLORE_OUTLINED,
                        selected_icon=ft.icons.EXPLORE,
                        label="Explore",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.SUBSCRIPTIONS_OUTLINED,
                        selected_icon=ft.icons.SUBSCRIPTIONS,
                        label="Subscriptions",
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.VIDEO_LIBRARY_OUTLINED,
                        selected_icon=ft.icons.VIDEO_LIBRARY,
                        label="Library",
                    ),
                ],
                on_change=lambda e: page.go(["/", "/explore", "/subscriptions", "/library"][e.control.selected_index]),
                expand=True,
            )
        ],
        visible=False,
    )

    sidebar = ft.Container(
        content=sidebar_container,
        # bgcolor=ft.colors.SURFACE_VARIANT,
        width=0,
        height=pgh
        # animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
    )

    

    # App Bar
    # search_field = ft.TextField(hint_text="Search", expand=True, on_submit=search, width=1 if is_mobile() or pgw < 600 else page.width*0.3)
    search_field = create_search_field()
    

    app_bar = ft.AppBar(
        # leading=ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar),
        # leading_width=40,
        # title=ft.Text("YouTube"),
        title=ft.Row(
            [
                ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar)
                if not is_mobile() else ft.Container(width=0),
                ft.Icon(ft.icons.PLAY_CIRCLE_FILLED, color=ft.colors.RED_500),
                ft.Text("YouTube" if not is_mobile() else "YT"),
            ]
        ),
        
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(
                content=ft.Row(
                    [
                        search_field,
                        ft.IconButton(ft.icons.SEARCH, on_click=search),
                    ]
                ),
                # width=400 if page.platform != ft.PagePlatform.ANDROID or page.platform != ft.PagePlatform.IOS else 10,
                # width=page.width * 0.2 if is_mobile() else min(page.width*0.5, 400),
                
                padding=10,
            ),
            ft.IconButton(ft.icons.NOTIFICATIONS),
            ft.IconButton(ft.icons.ACCOUNT_CIRCLE),
        ],
    )
    
    # Main Content
    video_grid = ft.GridView(
        expand=True,
        runs_count=1 if is_mobile() else None,
        width=pgw/5*0.2,  # This will be updated in update_layout
        max_extent=calculate_max_extent(not is_mobile()),
        child_aspect_ratio=1.2,
        spacing=-3,
        run_spacing=10,
    )

    for i in range(20):
        video_grid.controls.append(
            create_video_card(
                f"Video Title {i+1}",
                f"Channel {i+1}",
                f"{(i+1)*1000}",
                f"./assets/{thumbnail_files[0]}",
            )
        )

    # Layout
    content = ft.Container(
        content=video_grid,
        expand=True,
    )
        
    def update_layout(e):
        
        # Create a new search field with updated width
        new_search_field = create_search_field()
        
        # Replace the old search field with the new one
        search_container = app_bar.actions[0].content
        search_container.controls[0] = new_search_field
        
        sidebar_visible = not is_mobile()
        
        video_grid.width = pgw/5*0.2,
        video_grid.max_extent = calculate_max_extent(sidebar_visible)
        video_grid.runs_count = 1 if is_mobile() else 5  # Set to None for auto-calculation in desktop mode
        video_grid.child_aspect_ratio = 1.2
        
        # Update other layout elements based on page width
        if is_mobile():
            page.navigation_bar = ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.icons.HOME, label="Home"),
                    ft.NavigationBarDestination(icon=ft.icons.EXPLORE, label="Explore"),
                    ft.NavigationBarDestination(
                        icon=ft.icons.SUBSCRIPTIONS, label="Subscriptions"
                    ),
                    ft.NavigationBarDestination(
                        icon=ft.icons.VIDEO_LIBRARY, label="Library"
                    ),
                ],
            )
            main_area = ft.Row(
                [
                    content,
                ],
                expand=True,
            )

        else:
            main_area = ft.Row(
                [
                    sidebar,
                    content,
                ],
                expand=True,
            )
            
        page.controls = [app_bar, main_area]
        page.update()

    page.on_resized = update_layout

    update_layout(None)

    page.update()


ft.app(main, assets_dir="assets")
