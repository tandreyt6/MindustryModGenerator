class EN:
    type = "en"
    class Settings:
        class General:
            needRestart = "For the changes to take effect, you need to restart the application."

class RU:
    type = "ru"
    class Settings:
        class General:
            needRestart = "Для того, чтобы изменения вступили в силу, необходимо перезапустить приложение."
        class ActionsPanel:
            general = "Основное"
            appearance = "Интерфейс"
            plugins = "Плагины"
            code_editor = "Редактора кода"
            Java = "Java"

    class Launcher:
        class ActionsPanel:
            open = "Открыть"
            open_dir = "Открыть папку"
            delete = "Удалить из списка"
            settings = "Настройки"
            imp_proj = "Импортировать из папки"
            crt_proj = "Создать проект"

        class Dialog:
            confirm_action = "Подтверждение действия"
            delete_project_from_list = "Удалить '{name}' из списка?"
            act_del_from_project_list = "Удалить"
            cancel = "Отмена"

    class Editor:
        class ToolTip:
            gradleMenu_noloaded = "Gradle не был загружен..."
            gradleMenu_loaded = "Gradle загружен."

        class Console:
            input_placeholder = "Введите команду..."
            clear = "Очистить"
            show = "Показать"
            start = "Запустить"
            stop = "Останавить"
            placeholder = "Консоль выполнения..."

        class ActionPanel:
            run_task = "Запустить задачу"
            git_menu = "Git"
            project_settings = "Настройки проекта"
            settings = "Настройки"
            show_project_folder = "Показать папку проекта"
            exit_project = "Выйти из проекта"
            exit = "Выйти"
            file = "Файл"
            open = "Открыть"
            rename = "Переименовать"
            delete = "Удалить"
            create_category = "Создать папку"
            create_item = "Создать элемент"
            view = "Отображение"
            test = "Тест"
            gradle = "Gradle"
            load_gradle = "Загрузка Gradle..."
            build_project = "Собрать проект"
            item_has_been_created_path = "Элемент {name} был создан в {path}"
            item_has_been_saved = "Элемент {name} был сохранен"
            menu_pos_panels = "Позиция панелей"
            menu_pos1_panels = "Лево Право"
            menu_pos2_panels = "Право Лево"
            menu_pos3_panels = "Лево лево"
            menu_pos4_panels = "лево Лево"
            menu_pos5_panels = "Право право"
            menu_pos6_panels = "право Право"

        class Dialog:
            run_task = "Выполнить"
            confirm_action = "Подтверждение действия"
            name_empty_warn = "Название не должно быть пустым!"
            name_is_long_warn = "Название слишком коротко!"
            name_first_word_isDigit_warn = "Название не должно начинаться с цифры"
            name_exist_item = "Это имя уже существует!"
            confirm_delete_item = "Вы уверены, что хотите удалить элемент?\nДанное действие нельзя будет отменить!"
            error = "Ошибка"
            successful = "Успешно"
            build_successful = "Сборка завершена успешно!"
            start_task = "Запущена задача '{name}'..."
            error_load_elements_save = "При загрузке информации об элементах возникла ошибка!\nОшибка: {err}"
            cancel = "Отмена"
            apply = "Применить"
            no_plugin_for_select = "Плагин не установлен"
            save_select = "Запомнить выбор"
            select_plugin = "Выберите плагин, который будет отвечать ща настройку проекта"


Langs = {"ru": ("Русский", RU), "en": ("English", EN)}
Lang: RU = None
