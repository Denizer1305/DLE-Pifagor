import type { AuthFormCardConfig, AuthIntroConfig } from "@/modules/auth/types/auth-form.types";

interface AuthPageConfig {
    intro: AuthIntroConfig;
    form: AuthFormCardConfig;
}

export const loginPageConfig: AuthPageConfig = {
    intro: {
        badges: [
            {
                icon: "fa-solid fa-lock",
                label: "Защищённый вход",
            },
            {
                icon: "fa-solid fa-circle-check",
                label: "Быстрый доступ",
            },
        ],
        title: "С возвращением в Пифагор",
        subtitle:
            "Войдите в личный кабинет, чтобы продолжить обучение, работу с курсами, заданиями, журналом и всей цифровой образовательной средой.",
        meta: [
            {
                icon: "fa-solid fa-book-open",
                label: "Учёба и курсы",
            },
            {
                icon: "fa-solid fa-list-check",
                label: "Задания",
            },
            {
                icon: "fa-solid fa-chart-line",
                label: "Прогресс",
            },
        ],
    },
    form: {
        icon: "fa-solid fa-right-to-bracket",
        topline: "Вход в аккаунт",
        title: "Авторизация",
        description: "Введите email и пароль, чтобы перейти в личное пространство.",
    },
};

export const registerPageConfig: AuthPageConfig = {
    intro: {
        badges: [
            {
                icon: "fa-solid fa-shield-halved",
                label: "Безопасный вход",
            },
            {
                icon: "fa-solid fa-user-plus",
                label: "Быстрая регистрация",
            },
        ],
        title: "Присоединяйтесь к Пифагору",
        subtitle:
            "Создайте аккаунт и получите доступ к современной цифровой образовательной среде — спокойно, быстро и без лишних шагов.",
        meta: [
            {
                icon: "fa-solid fa-graduation-cap",
                label: "Для учащихся",
            },
            {
                icon: "fa-solid fa-chalkboard-user",
                label: "Для преподавателей",
            },
            {
                icon: "fa-solid fa-people-group",
                label: "Для родителей",
            },
        ],
    },
    form: {
        icon: "fa-solid fa-user-check",
        topline: "Новая учетная запись",
        title: "Регистрация",
        description: "Заполните форму ниже, чтобы создать аккаунт и начать работу с платформой.",
    },
};

export const forgotPasswordPageConfig: AuthPageConfig = {
    intro: {
        badges: [
            {
                icon: "fa-solid fa-key",
                label: "Восстановление доступа",
            },
            {
                icon: "fa-solid fa-shield-halved",
                label: "Безопасность аккаунта",
            },
        ],
        title: "Восстановите доступ к аккаунту",
        subtitle:
            "Укажите email, который использовался при регистрации. Мы отправим инструкцию для восстановления доступа.",
        meta: [
            {
                icon: "fa-solid fa-envelope",
                label: "Письмо на email",
            },
            {
                icon: "fa-solid fa-shield",
                label: "Проверка безопасности",
            },
            {
                icon: "fa-solid fa-clock",
                label: "Быстрое восстановление",
            },
        ],
    },
    form: {
        icon: "fa-solid fa-key",
        topline: "Восстановление доступа",
        title: "Забыли пароль?",
        description: "Введите email, и мы отправим ссылку для восстановления пароля.",
    },
};

export const resetPasswordPageConfig: AuthPageConfig = {
    intro: {
        badges: [
            {
                icon: "fa-solid fa-lock",
                label: "Новый пароль",
            },
            {
                icon: "fa-solid fa-shield-halved",
                label: "Защита аккаунта",
            },
        ],
        title: "Создайте новый пароль",
        subtitle:
            "Придумайте новый пароль для входа в аккаунт. Он должен быть надёжным и отличаться от простых комбинаций.",
        meta: [
            {
                icon: "fa-solid fa-key",
                label: "Надёжный доступ",
            },
            {
                icon: "fa-solid fa-user-shield",
                label: "Безопасность аккаунта",
            },
            {
                icon: "fa-solid fa-check",
                label: "Быстрое восстановление",
            },
        ],
    },
    form: {
        icon: "fa-solid fa-lock",
        topline: "Новый пароль",
        title: "Сброс пароля",
        description: "Введите новый пароль и подтвердите его повторным вводом.",
    },
};

export const verifyEmailPageConfig: AuthPageConfig = {
    intro: {
        badges: [
            {
                icon: "fa-solid fa-envelope-circle-check",
                label: "Подтверждение почты",
            },
            {
                icon: "fa-solid fa-shield",
                label: "Защита аккаунта",
            },
        ],
        title: "Подтвердите электронную почту",
        subtitle:
            "Остался один шаг, чтобы завершить регистрацию и активировать аккаунт в цифровой образовательной среде.",
        meta: [
            {
                icon: "fa-solid fa-check-circle",
                label: "Регистрация почти завершена",
            },
            {
                icon: "fa-solid fa-envelope-open-text",
                label: "Проверка email",
            },
            {
                icon: "fa-solid fa-user-shield",
                label: "Защита аккаунта",
            },
        ],
    },
    form: {
        icon: "fa-solid fa-envelope-circle-check",
        topline: "Подтверждение email",
        title: "Проверка почты",
        description: "Мы проверим ссылку подтверждения и сообщим результат.",
    },
};

export const teacherOrganizationCodePageConfig: AuthPageConfig = {
    intro: {
        badges: [
            {
                icon: "fa-solid fa-building-columns",
                label: "Проверка организации",
            },
            {
                icon: "fa-solid fa-shield-halved",
                label: "Безопасная заявка",
            },
        ],
        title: "Подтвердите связь с организацией",
        subtitle:
            "Введите код, который выдала образовательная организация. После проверки мы отправим заявку администратору.",
        meta: [
            {
                icon: "fa-solid fa-user-check",
                label: "Заявка преподавателя",
            },
            {
                icon: "fa-solid fa-envelope-circle-check",
                label: "Подтверждение email",
            },
            {
                icon: "fa-solid fa-clock",
                label: "Ожидание проверки",
            },
        ],
    },
    form: {
        icon: "fa-solid fa-building-columns",
        topline: "Код организации",
        title: "Проверка кода",
        description: "Введите код образовательной организации, чтобы завершить регистрацию преподавателя.",
    },
};
