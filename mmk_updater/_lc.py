import locale

BASE_LOCALE = {
    "has_update_title": "New version of {} is available",
    "file_pattern": "File: {} ({})",
    "downloading": "Downloading file {}...",
    "downloading_run_after": "Installation will be started automatically after download",
    "download_btn": "Update now",
    "dl_error": "ERROR: Download failed",
    "close_btn": "Close",
    "ppa_migration": "This application migrated from Ubuntu PPA to self-hosted Debian/Ubuntu repository.\n\n"
                     "To receive this and other updates, you must run repository migration.\n"
                     "This will make less than one minute, click here to get instructions.\n"
                     "Sorry for wasting time...",
    "site_btn": "View in web browser",
    "repo_install": "Install it via system package manager.",
    "manual_install": "Update downloaded, but we can't install it automatically.\nFile "
                      "was saved to {}.\nPlease install it after app close."
}

L18N = {
    "ru_RU": {
        "has_update_title": "Доступна новая версия {}",
        "file_pattern": "Будет загружен: {} ({})",
        "downloading": "Загружаем файл {}...",
        "downloading_run_after": "Установка начнётся сразу после загрузки",
        "download_btn": "Обновить",
        "dl_error": "ОШИБКА: Не удалось скачать файл",
        "site_btn": "Перейти на веб-сайт программы",
        "close_btn": "Закрыть",
        "ppa_migration": "Это приложение было перенесено с Ubuntu PPA на собственный репозиторий.\n\n"
                         "Чтобы получить это и последующие обновления, выполните замену подключенного\n"
                         "репозитория. Это займёт одну минуту, нажмите сюда для получения инструкций..\n"
                         "Извините за потраченное время...",
        "repo_install": "Установите обновление ч-з системный пакетный менеджер",
        "manual_install": "Обновление загружено, но мы не можем установить его автоматически.\nФайл "
                          "сохранён по пути {}. \nУстановите его, когда будет возможность."
    }
}


def t(k):
    lang = locale.getlocale()[0]
    if lang in L18N:
        if k in L18N[lang]:
            return L18N[lang][k]

    if k in BASE_LOCALE:
        return BASE_LOCALE[k]
    return k
