export const messages = {
    ru: {
        auth: {
            login: "Войти",
            register: "Регистрация",
        },
        common: {
            closeMenu: "Закрыть меню",
            closeMobileMenu: "Закрыть мобильное меню",
            closeWindow: "Закрыть окно",
            getStarted: "Начать работу",
            mobileMenu: "Мобильное меню",
            mobileNavigation: "Мобильная навигация",
            navigation: "Основная навигация",
            openMenu: "Открыть меню",
            platformPartners: "Партнёры платформы",
            switchLanguage: "Switch to English",
            switchTheme: "Переключить тему",
        },
        contacts: {
            navigationAddress: "Адрес для навигации:",
            selectedFiles: "Выбрано файлов: {count}",
        },
        footer: {
            brandDescription: "Цифровая образовательная среда для обучения, наставничества, расписания, заданий и роста.",
            brandName: "ЦОС «Пифагор»",
            legal: "Все права защищены.",
            navigation: "Навигация в подвале",
            note: "Спокойное пространство для обучения, наставничества и развития.",
        },
        mobile: {
            fallbackDescription: "Перейти в раздел",
            quote: "Цифровая образовательная среда для спокойного обучения, развития и наставничества.",
        },
        teachers: {
            defaultGuest: "Для гостей показываем преподавателей организации по умолчанию.",
            defaultMember: "Для вас показаны преподаватели вашей образовательной организации.",
            loadingDescription: "Получаем актуальный список преподавателей выбранной образовательной организации.",
            loadingTitle: "Загружаем преподавателей",
            organization: "Образовательная организация",
            reset: "Сбросить",
            search: "Поиск",
            subject: "Предмет",
            teachersCount: "{count} преподавателей",
            awards: "Награды и достижения",
            department: "Отделение",
        },
    },
    en: {
        auth: {
            login: "Sign in",
            register: "Register",
        },
        common: {
            closeMenu: "Close menu",
            closeMobileMenu: "Close mobile menu",
            closeWindow: "Close window",
            getStarted: "Get started",
            mobileMenu: "Mobile menu",
            mobileNavigation: "Mobile navigation",
            navigation: "Main navigation",
            openMenu: "Open menu",
            platformPartners: "Platform partners",
            switchLanguage: "Переключить на русский",
            switchTheme: "Toggle theme",
        },
        contacts: {
            navigationAddress: "Navigation address:",
            selectedFiles: "Selected files: {count}",
        },
        footer: {
            brandDescription: "A digital learning environment for education, mentoring, schedules, assignments, and growth.",
            brandName: "Pifagor DLE",
            legal: "All rights reserved.",
            navigation: "Footer navigation",
            note: "A calm space for learning, mentoring, and development.",
        },
        mobile: {
            fallbackDescription: "Open section",
            quote: "A digital learning environment for calm learning, growth, and mentoring.",
        },
        teachers: {
            defaultGuest: "Guests see teachers from the default organization.",
            defaultMember: "You are seeing teachers from your educational organization.",
            loadingDescription: "Loading the latest teacher list for the selected educational organization.",
            loadingTitle: "Loading teachers",
            organization: "Educational organization",
            reset: "Reset",
            search: "Search",
            subject: "Subject",
            teachersCount: "{count} teachers",
            awards: "Awards and achievements",
            department: "Department",
        },
    },
} as const;

export type MessageLocale = keyof typeof messages;
export type MessagePath = string;
