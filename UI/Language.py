class EN:
    type = "en"

    class Settings:
        class General:
            needRestart = "For the changes to take effect, you need to restart the application."

        class ActionsPanel:
            general = "General"
            appearance = "Appearance"
            plugins = "Plugins"
            code_editor = "Code Editor"
            Java = "Java"

    class Launcher:
        class ActionsPanel:
            open = "Open"
            open_dir = "Open Folder"
            delete = "Remove from List"
            settings = "Settings"
            imp_proj = "Import from Folder"
            crt_proj = "Create Project"

        class Dialog:
            confirm_action = "Confirm Action"
            delete_project_from_list = "Remove '{name}' from the list?"
            act_del_from_project_list = "Remove"
            cancel = "Cancel"

    class Editor:
        class ToolTip:
            gradleMenu_noloaded = "Gradle has not been loaded..."
            gradleMenu_loaded = "Gradle loaded."

        class Console:
            input_placeholder = "Enter a command..."
            clear = "Clear"
            show = "Show"
            start = "Start"
            stop = "Stop"
            placeholder = "Execution Console..."

        class ActionPanel:
            run_task = "Run Task"
            git_menu = "Git"
            treeMenu = "Research"
            openTreeMenu = "Open Research Tree"
            project_settings = "Project Settings"
            settings = "Settings"
            show_project_folder = "Show Project Folder"
            exit_project = "Exit Project"
            exit = "Exit"
            file = "File"
            open = "Open"
            rename = "Rename"
            delete = "Delete"
            create_category = "Create Folder"
            create_item = "Create Item"
            view = "View"
            test = "Test"
            gradle = "Gradle"
            load_gradle = "Loading Gradle..."
            build_project = "Build Project"
            item_has_been_created_path = "Item {name} has been created at {path}"
            item_has_been_saved = "Item {name} has been saved"
            menu_pos_panels = "Panel Position"
            menu_pos1_panels = "Left Right"
            menu_pos2_panels = "Right Left"
            menu_pos3_panels = "Left left"
            menu_pos4_panels = "left Left"
            menu_pos5_panels = "Right right"
            menu_pos6_panels = "right Right"

        class Dialog:
            run_task = "Run"
            confirm_action = "Confirm Action"
            name_empty_warn = "Name must not be empty!"
            name_is_long_warn = "Name is too short!"
            name_first_word_isDigit_warn = "Name must not start with a digit"
            name_exist_item = "This name already exists!"
            confirm_delete_item = "Are you sure you want to delete the item?\nThis action cannot be undone!"
            error = "Error"
            successful = "Success"
            build_successful = "Build completed successfully!"
            start_task = "Task '{name}' started..."
            error_load_elements_save = "An error occurred while loading element data!\nError: {err}"
            cancel = "Cancel"
            apply = "Apply"
            no_plugin_for_select = "Plugin not installed"
            save_select = "Remember selection"
            plugin_created_mod_not_found = (
                "Mod configuration can only be done by the plugin that generated the mod!\n"
                "Please enable the plugin '{name}'!"
            )
            select_plugin = "Select the plugin responsible for project configuration"
            gradlew_task = "Gradlew Task"
            task_placeholder = "<task>"
            failed_build_item_no_constructor = "Failed to create item '{name}': constructor not available."
            unknown_item_no_loader = "Failed to load item: no loader found\nInstall plugin: {name}"
            preview = "Preview"
            save = "Save"
            variables = "Variables"
            search = "Search"

    class TechTreeWindow:
        class Dialog:
            select = "Select"
            remove = "Remove"
            remove_selected_item = "Are you sure you want to remove '{name}' and all of its children?"
            error_join_parent_to_parent = "Cannot link a node to its child!"
            rejoin_item_to_child = "Reattach '{child}' to '{parent}' as a child node?"
            join_item_to_parent = "Attach '{child}' to '{parent}' as a child node?"
            search_ = "Search..."
            select_existing_root_item = "Select an item for the root node:"
            item_list_empty_error = "No available items!"
            tech_tree_name_exist_error = "A tree with this name already exists."
            rejoin_item_error = "Invalid reattachment operation!"
            save_error = "Failed to save changes!"
            research_type = "Requirement Type"
            resources = "Resources"
            value = "Value"
            remove_tree_question = "Are you sure you want to delete the tree?\nThis action cannot be undone!"
            create_tree = "Create Tree"
            remove_tree = "Delete Tree"
            add_root_node = "Add Root Node"
            remove_node = "Remove Node"
            enter_tree_name = "Enter tree name"

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
            treeMenu = "Исследования"
            openTreeMenu = "Открыть дерево исследования"
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
            plugin_created_mod_not_found = "Настройка мода может проводится только тем плагином, которым был сгенерирован мод!\nПожалуйста включите плагин '{name}'!"
            select_plugin = "Выберите плагин, который будет отвечать ща настройку проекта"
            gradlew_task = "Задача gradlew"
            task_placeholder = "<задача>"
            failed_build_item_no_constructor = "Не удалось создать элемент {name}': конструктор недоступен."
            unknown_item_no_loader = "Не удалось загрузить элемент: Отсутствует загрузчик\nУстановите плагин: {name}"
            preview = "Предпросмотр"
            save = "Сохранить"
            variables = "Переменные"
            search = "Поиск"

    class TechTreeWindow:
        class Dialog:
            select = "Выбрать"
            remove = "remove"
            remove_selected_item = "Вы уверены, что хотите удалить '{name}' и всю ветку после него?"
            error_join_parent_to_parent = "Нельзя привязать узел к его дочернему элементу!"
            rejoin_item_to_child = "Перепривязать '{child}' к '{parent}' как дочерний узел?"
            join_item_to_parent = "Добавить '{child}' к '{parent}' как дочерний узел?"
            search_ = "Поиск..."
            select_existing_root_item = "Выберите предмет для корневого узла:"
            item_list_empty_error = "Нет доступных элементов!"
            tech_tree_name_exist_error = "Дерево с таким именем уже существует."
            rejoin_item_error = "Неверная операция перепривязки!"
            save_error = "Не удалось сохранить изменения!"
            research_type  = "Тип требования"
            resources = "Ресурсы"
            value = "Значение"
            remove_tree_question = "Вы действительно хотите удалить дерево?\nЭто действие нельзя будет отменить!"
            create_tree = "Создать дерево"
            remove_tree = "Удалить дерево"
            add_root_node = "Добавить корневой узел"
            remove_node = "Удалить узел"
            enter_tree_name = "Введите название дерева"
            add_tree_requirements = "+ Добавить зависимость"
            requirements = "Зависимости"
            type_ = "Тип:"


Langs = {"ru": ("Русский", RU), "en": ("English", EN)}
Lang: RU = None
