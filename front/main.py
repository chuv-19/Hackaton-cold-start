import os
from time import sleep
import flet as ft
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from inyoyo import settings


# Установка связи с бд
DATABSE_URL = f"postgresql://{settings.db_username}:{settings.db_pass}@{settings.db_hostname}/{settings.db_name}"
engine = create_engine(DATABSE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Создание моделей для работы с бд через SQLalchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

class Tags(Base):
    __tablename__ = 'tags'
    categories = Column(String, nullable=False, primary_key=True)
    user_id = Column(Integer, nullable=False, primary_key=True)
    
class Video(Base):
    __tablename__ = "videos"
    video_id = Column(String, nullable=False, primary_key=True)
    title = Column(String, nullable=False)
    category_id = Column(String, nullable=False)
    
    
# Инициализация сессии
session = Session()

# Основной блок кода фронтэнда
def main(page: ft.Page):
    page.title = "YouTube Clone"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 10
    page.spacing = 0

    pgw = page.width
    pgh = page.height


    # Получение информации о платформе пользователя
    def is_mobile():
        return page.platform in (ft.PagePlatform.ANDROID, ft.PagePlatform.IOS)

    # Создания навигационной панели, если пользователь зашёл на сайт через мобильное устройство
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

    # Создание views и переадресация пользователя
    def route_change(route):
        page.navigation_bar = sidebar
        page.update()
        page.views.clear()
        if page.route == "/":
            content = ft.Container(
                content=video_grid,
                expand=True,
            )

            main_area = ft.Row(
                [sidebar, content],
                expand=True,
            )
            if is_mobile():
                main_area = ft.Row(
                    [content],
                    expand=True,
                )
            page.views.append(
                ft.View(
                    "/",
                    [
                        app_bar,
                        main_area,
                    ],
                    navbar(),
                )
            )

        elif page.route == "/video":
            content = create_video_page()
            main_area = ft.Row(
                [
                    sidebar,
                    content,
                ],
                expand=True,
            )

            if is_mobile():
                main_area = ft.Row(
                    [
                        content,
                    ],
                    expand=True,
                )

            page.views.append(
                ft.View(
                    "/video",
                    [
                        app_bar,
                        main_area,
                    ],
                    navbar(),
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

        elif page.route == "/reg":
            page.views.append(
                ft.View(
                    "/reg",
                    [
                        create_reg_page(),
                    ],
                )
            )
            
        elif page.route == "/catchoose":
            page.views.append(
                ft.View(
                    "/catchoose",
                    [
                        create_category_page(),
                    ],
                )
            )

        page.update()

    # Удаление последнего view, переход на прошлый
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    # Инициализация EVENT HANDLERов для работы с views
    page.on_route_change = route_change
    page.on_view_pop = view_pop


    # Создание компонентов страницы видео ролика
    def create_video_page():
        return ft.Column(
            [
                ft.Container(
                    content=ft.Image(
                        src=(
                            f"https://d1csarkz8obe9u.cloudfront.net/posterpreviews/youtube-thumbnail-interview-podcast-template-design-2a00bc1f530b7ad54f50a59961e39755_screen.jpg?ts=1602531862"
                        ),
                        fit=ft.ImageFit.COVER,
                    ),
                    height=(pgh / 1.7 if not is_mobile() else page.height / 3.5),
                    width=(pgw / 1.5 if not is_mobile() else page.width * 0.95),
                    border_radius=ft.border_radius.all(10),
                ),
                ft.Container(
                    ft.Text("Video Title", size=18, weight=ft.FontWeight.BOLD)
                ),
                ft.Text("Channel Name • 1M views • 2 days ago"),
                
                ft.Row(
                    [
                        ft.ElevatedButton("Like", icon=ft.icons.THUMB_UP),
                        ft.ElevatedButton("Dislike", icon=ft.icons.THUMB_DOWN),
                        ft.ElevatedButton("Share", icon=ft.icons.SHARE),
                        ft.ElevatedButton("Download", icon=ft.icons.DOWNLOAD),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    width=pgw / 1.5 if not is_mobile() else pgw * 0.95,
                ),
                
                ft.Text("Comments", size=18, weight=ft.FontWeight.BOLD),
                ft.ListView(
                    [
                        ft.ListTile(
                            leading=ft.CircleAvatar(
                                foreground_image_src="https://picsum.photos/50"
                            ),
                            title=ft.Text("User Name"),
                            subtitle=ft.Text(
                                "This is a comment on the video.jhfutfyjtdrdtv,hfidwuygfjasdgfiuydgfiuyadgbfiuybgweiuvfwiueyfviuwegbfviuygbvfiuybgqweiuvytcrtysctrescterstersterscertsctersctercterctrscercrcsryyuyuyuyuyuyuyiooooopkkkkkkoytufghcvbnk;j'ouiypouftiydfchjvmnb,bjhu",
                                no_wrap=False,
                            ),
                        )
                        for _ in range(10)
                    ],
                    width=pgw / 1.5 if not is_mobile() else pgw * 0.95,
                    spacing=30,
                ),
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            width=pgw,
        )

    def create_user(e):
        new_usr = User(name = e.data)
        session.add(new_usr)    
        session.commit()
        page.client_storage.set("id",session.query(User).filter(User.name == new_usr.name).first().id)
        page.go("/catchoose")
        print(page.client_storage.get("id"))
        
    # Создание компонентов страницы регистрации пользователя
    def create_reg_page():
        
        return ft.Column(
            [
                ft.Container(
                    content=ft.Text("Missclick"),
                    alignment=ft.alignment.top_left,
                    expand=False,
                ),
                ft.Container(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    """Вас приветствует команда miss Click!
Помоги нам, пожалуйста, ответив на пару вопросов:
Мы хотим сделать наши подборки видео еще лучше!""",
                                    text_align=ft.TextAlign.CENTER,
                                    size=23
                                ),
                                ft.Row(
                                    [
                                        ft.TextField(
                                            hint_text="Введите ваше имя",
                                            width=300,
                                            on_submit=create_user,
                                        ),
                                        ft.ElevatedButton("Отпрвить", width=150, on_click=create_user),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        width=500,
                        height=600,
                        bgcolor="#1C232B",
                        border_radius=40,
                        padding=10,
                        alignment=ft.alignment.top_center,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
        )
        
    # def create_category_page():
        categories = [
            "UNKNOWN", "Авто-мото", "аниме", "бизнес", "видеоигры", "детям", "еда", "животные",
            "здоровье", "интервью", "культура", "лайфхаки", "лайфстайл", "музыка", "мультфильмы",
            "наука", "недвижимость", "обзоры", "охота", "обучение", "психология", "путешествия",
            "развлечения", "разное", "сад, огород", "сериалы", "спорт", "строительство",
            "телепередачи", "юмор", "экзотика", "хобби", "фильмы", "технологии", "техника"
        ]

        def category_clicked(e):
            print(f"Category selected: {e.control.text}")
            # You can add more functionality here, like navigating to a new page or updating user preferences

        # Calculate item size based on screen width
        item_size = min(page.width / 6 - 20, 120)  # Subtract padding and ensure max size

        grid = ft.GridView(
            expand=True,
            runs_count=6,
            max_extent=item_size,
            child_aspect_ratio=1,
            spacing=40,
            run_spacing=40,
            padding=30,
            width=pgw/1.5
            
        )

        for category in categories:
            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.icons.CATEGORY, size=item_size * 0.4, color=ft.colors.BLUE_400),
                            ft.Text(
                                category, 
                                size=item_size * 0.15, 
                                weight=ft.FontWeight.BOLD, 
                                text_align=ft.TextAlign.CENTER,
                                no_wrap=False,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    width=item_size,
                    height=item_size,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=ft.border_radius.all(10),
                    ink=True,
                    on_click=category_clicked,
                )
            )

        return ft.Column(
            [
                ft.Container(
                    content=ft.Text("Выберите интересующие вас категории", size=24, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(top=20, bottom=10),
                ),
                ft.Container(
                    content=grid,
                    expand=True,
                ),
                ft.Container(
                    content=ft.ElevatedButton("Продолжить", width=200, on_click=lambda _: page.go("/")),
                    margin=ft.margin.only(top=20, bottom=20),
                    alignment=ft.alignment.center,
                ),
            ],
            expand=True,
        )

    # Создание компонентов страницы выбора категорий
    def create_category_page():
        categories = [
            "UNKNOWN", "Авто-мото", "аниме", "бизнес", "видеоигры", "детям", "еда", "животные",
            "здоровье", "интервью", "культура", "лайфхаки", "лайфстайл", "музыка", "мультфильмы",
            "наука", "недвижимость", "обзоры", "охота", "обучение", "психология", "путешествия",
            "развлечения", "разное", "сад, огород", "сериалы", "спорт", "строительство",
            "телепередачи", "юмор", "экзотика", "хобби", "фильмы", "технологии", "техника"
        ]

        def add_tag_to_user(e):
            for tag in user_tags:
                new_tag = Tags(categories = tag, user_id = page.client_storage.get("id"))
                session.add(new_tag)
                session.commit()
            page.go("/")

        user_tags = []
        

        def category_clicked(e):
            if e.control.bgcolor != 'green':
                e.control.bgcolor = 'green'
                user_tags.append(e.control.content.controls[1].value)
            else: 
                e.control.bgcolor = ft.colors.SURFACE_VARIANT
                user_tags.pop()
            page.update()

        # Calculate item size based on screen width, aiming for 6x6 grid
        grid_size = min(page.width * 0.8, page.height * 0.8, 900)  # 80% of screen width/height or max 600px
        item_size = (grid_size / 5) - 5  # Subtract spacing

        grid = ft.GridView(
            expand=False,
            runs_count=6,
            max_extent=item_size,
            child_aspect_ratio=1,
            spacing=40,
            run_spacing=40,
            width=grid_size,
            height=grid_size,
        )

        for category in categories:
            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.icons.CATEGORY, size=item_size * 0.4, color=ft.colors.BLUE_400),
                            ft.Text(
                                category, 
                                size=item_size * 0.1, 
                                weight=ft.FontWeight.BOLD, 
                                text_align=ft.TextAlign.RIGHT,
                                no_wrap=False,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=5,
                    ),
                    width=item_size,
                    height=item_size,
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    border_radius=ft.border_radius.all(10),
                    ink=True,
                    on_click=category_clicked,
                )
            )

        return ft.Column(
            [
                ft.Container(
                    content=ft.Text("Выберите интересующие вас категории", size=24, weight=ft.FontWeight.BOLD),
                    margin=ft.margin.only(bottom=20),
                ),
                ft.Row(
                    [grid],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Container(
                    content=ft.ElevatedButton("Продолжить", width=200, on_click=add_tag_to_user),
                    margin=ft.margin.only(top=20),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            expand=True,
            scroll=ft.ScrollMode.HIDDEN
        )

    # Функция по созданию хедера
    def create_app_bar():
        return ft.AppBar(
            toolbar_height=100,
            center_title=True,
            title=ft.Row(
                controls=[
                    (
                        ft.IconButton(ft.icons.MENU, on_click=toggle_sidebar)
                        if not is_mobile()
                        else ft.Container(width=0)
                    ),
                    ft.Text("Missclick"),
                ]
            ),
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
                ft.IconButton(
                    ft.icons.ACCOUNT_CIRCLE, on_click=lambda _: page.go("/reg")
                ),
            ],
        )
        

    # Создание карточек для видео роликов на главной странице
    def create_video_card(title, channel, views, image_url):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Image(src=image_url, fit=ft.ImageFit.COVER),
                        height=180 if not is_mobile() else page.height / 3,
                        width=340 if not is_mobile() else page.width * 0.95,
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
                            spacing=0,
                        ),
                    ),
                ],
                spacing=10,
            ),
            ink=True,
            border_radius=ft.border_radius.all(10),
            on_click=lambda _: [print(f"Clicked on {title}"), page.go("/video")],
        )

    # Создание компонентов страницы поиска
    def create_search_field():
        return ft.TextField(
            hint_text="Search",
            text_vertical_align=ft.VerticalAlignment.CENTER,
            text_size=20,
            expand=True,
            on_submit=search,
            width=pgw * 0.3 if page.width < 600 else min(page.width * 0.3, 700),
            border_radius=25,
            bgcolor="1C232B",
        )


    def search(e):
        print(f"Searching for: {e.data}")

    # Навигационная панель знизу экрана для пользователей, которые зашли с мобильного устройства
    def navbar():
        if is_mobile():
            return ft.NavigationBar(
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
                on_change=lambda e: page.go(
                    ["/", "/explore", "/subscriptions", "/library"][
                        e.control.selected_index
                    ]
                ),
            )

    def sdbr_width():
        min(page.width * 0.2, 100)

    def toggle_sidebar(e):
        sidebar_container.visible = not sidebar_container.visible
        sidebar.width = sdbr_width() if sidebar.width == 0 else 0
        page.update()

    # Вычисление растояния между карточками видео роликов на глваной странице
    def calculate_max_extent(sidebar_visible):
        if is_mobile():
            return 600
        else:
            sidebar_width = 240 if sidebar_visible else 0
            return 390 - (260 - sidebar_width)

    # Сайдбар
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
                on_change=lambda e: page.go(
                    ["/", "/explore", "/subscriptions", "/library"][
                        e.control.selected_index
                    ]
                ),
                expand=True,
            )
        ],
        visible=False,
    )

    sidebar = ft.Container(
        content=sidebar_container,
        # bgcolor=ft.colors.SURFACE_VARIANT,
        width=0,
        height=pgh,
        # animate=ft.animation.Animation(300, ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED),
    )

    # Хедер
    search_field = create_search_field()

    # Инициализация хедера
    app_bar = create_app_bar()

    # Инициализация главной страницы
    video_grid = ft.GridView(
        expand=True,
        runs_count=1 if is_mobile() else None,
        width=pgw / 5 * 0.2,  # This will be updated in update_layout
        max_extent=calculate_max_extent(not is_mobile()),
        child_aspect_ratio=1.2,
        spacing=-3,
        run_spacing=10,
    )

    def vid_grid():
        for i in range(1,21):
            video_grid.controls.append(
                create_video_card(
                    f"Video Title {i+1}",
                    f"Channel {i+1}",
                    f"{1000*i}",
                    f"https://picsum.photos/320/180?random={i+1}"

                    
                    # "https://pic.rutubelist.ru/promoitem/2024-09-27/83/17/83173544c929bcc361d2d5886373d9ea.jpg?width=882",
                    # f"https://picsum.photos/320/180?random={i+1}",
                )
            )

    # Layout
    vid_grid()
    content = ft.Container(
        content=video_grid,
        expand=True,
    )

    # Обновление элементов интерфейса в зависимости от размеров окна веб приложения
    def update_layout(e):

        # Create a new search field with updated width
        new_search_field = create_search_field()

        # Replace the old search field with the new one
        search_container = app_bar.actions[0].content
        search_container.controls[0] = new_search_field

        sidebar_visible = not is_mobile()

        video_grid.width = (pgw / 5 * 0.2,)
        video_grid.max_extent = calculate_max_extent(sidebar_visible)
        video_grid.runs_count = (
            1 if is_mobile() else 5
        )  # Set to None for auto-calculation in desktop mode
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

    page.go("/")

    page.update()


ft.app(main, assets_dir="assets")
