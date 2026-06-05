export type DashboardPlaceholderRole = "admin" | "teacher" | "student" | "parent";

export interface DashboardPlaceholderContent {
    icon: string;
    defaultTitle: string;
    subtitle: string;
    text: string;
    detailsTitle: string;
    details: string[];
    note: string;
    visualIcon: string;
    orbitIcon: string;
    dashboardRouteName: string;
    settingsRouteName: string;
    dashboardLinkTitle: string;
    dashboardLinkText: string;
    homeLabel: string;
    backLabel: string;
}

export const dashboardPlaceholderContent: Record<
    DashboardPlaceholderRole,
    DashboardPlaceholderContent
> = {
    admin: {
        icon: "fa-solid fa-screwdriver-wrench",
        defaultTitle: "Административный раздел",
        subtitle: "Раздел уже стоит в карте платформы и готовится к подключению.",
        text: "Мы аккуратно собираем интерфейс, права доступа и связь с backend. Пока страница закрыта техническим экраном, чтобы не показывать пустые таблицы и случайные данные.",
        detailsTitle: "Что происходит с разделом?",
        details: [
            "Маршрут уже добавлен в личный кабинет администратора.",
            "Компоненты страницы будут подключены после готовности сценария.",
            "Данные появятся только после проверки прав доступа и API.",
        ],
        note: "Это не ошибка доступа. Раздел временно скрыт до завершения реализации.",
        visualIcon: "fa-solid fa-screwdriver-wrench",
        orbitIcon: "fa-solid fa-code-branch",
        dashboardRouteName: "admin-dashboard",
        settingsRouteName: "admin-settings",
        dashboardLinkTitle: "Панель администратора",
        dashboardLinkText: "Вернитесь к рабочей зоне, пользователям и ключевым показателям.",
        homeLabel: "Вернуться в кабинет",
        backLabel: "Назад",
    },
    teacher: {
        icon: "fa-solid fa-chalkboard-user",
        defaultTitle: "Раздел преподавателя",
        subtitle: "Этот инструмент готовится для учебной работы преподавателя.",
        text: "Страница уже добавлена в маршруты, но полноценный интерфейс появится после подключения нужных данных: курсов, занятий, заданий или аналитики.",
        detailsTitle: "Почему раздел пока закрыт?",
        details: [
            "Сценарий находится в очереди на реализацию.",
            "Маршрут сохранен, поэтому навигация не потеряется.",
            "Мы не показываем заглушечные данные вместо настоящей учебной информации.",
        ],
        note: "Вернитесь в кабинет преподавателя: основные рабочие блоки уже доступны там.",
        visualIcon: "fa-solid fa-person-chalkboard",
        orbitIcon: "fa-solid fa-book-open",
        dashboardRouteName: "teacher-dashboard",
        settingsRouteName: "teacher-settings",
        dashboardLinkTitle: "Кабинет преподавателя",
        dashboardLinkText: "Откройте главную рабочую страницу преподавателя.",
        homeLabel: "Вернуться в кабинет",
        backLabel: "Назад",
    },
    student: {
        icon: "fa-solid fa-user-graduate",
        defaultTitle: "Раздел студента",
        subtitle: "Учебный раздел появится после подключения данных студента.",
        text: "Мы готовим страницу так, чтобы она показывала только реальные курсы, задания, оценки и прогресс. Пока нужный источник данных не подключен, раздел закрыт этим экраном.",
        detailsTitle: "Что будет дальше?",
        details: [
            "Страница получит данные из backend после готовности API.",
            "В интерфейсе появятся учебные карточки, списки и действия.",
            "Навигация уже ведет сюда, чтобы структура кабинета оставалась понятной.",
        ],
        note: "Основная сводка студента доступна на главной странице личного кабинета.",
        visualIcon: "fa-solid fa-user-graduate",
        orbitIcon: "fa-solid fa-chart-line",
        dashboardRouteName: "student-dashboard",
        settingsRouteName: "student-settings",
        dashboardLinkTitle: "Кабинет студента",
        dashboardLinkText: "Вернитесь к расписанию, задачам и учебной сводке.",
        homeLabel: "Вернуться в кабинет",
        backLabel: "Назад",
    },
    parent: {
        icon: "fa-solid fa-people-roof",
        defaultTitle: "Раздел родителя",
        subtitle: "Раздел готовится для спокойного контроля учебного процесса.",
        text: "Здесь появятся данные ребенка, сообщения, расписание или учебные показатели. Пока backend-раздел не вернул полноценные данные, мы показываем аккуратный технический экран.",
        detailsTitle: "Раздел в работе",
        details: [
            "Маршрут уже доступен из родительского кабинета.",
            "Контент появится после подключения связанных данных ребенка.",
            "Пустые или тестовые карточки здесь специально не выводятся.",
        ],
        note: "Проверьте главную страницу родительского кабинета: там отображается доступная сводка.",
        visualIcon: "fa-solid fa-people-roof",
        orbitIcon: "fa-solid fa-child",
        dashboardRouteName: "parent-dashboard",
        settingsRouteName: "parent-settings",
        dashboardLinkTitle: "Кабинет родителя",
        dashboardLinkText: "Вернитесь к общей сводке, расписанию и сообщениям.",
        homeLabel: "Вернуться в кабинет",
        backLabel: "Назад",
    },
};
