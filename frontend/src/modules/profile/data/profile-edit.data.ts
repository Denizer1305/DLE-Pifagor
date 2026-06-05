import type {
    ProfileEditFormContent,
    ProfileEditPageContent,
} from "@/modules/profile/types/profile-edit.types";

export const profileEditPageContent: ProfileEditPageContent = {
    hero: {
        icon: "fas fa-pen",
        topline: "Редактирование профиля",
        title: "Обновление личных и ролевых данных",
        text:
            "Здесь можно изменить основную информацию аккаунта, способы связи, настройки отображения и профессиональные данные, связанные с ролью пользователя.",
        badges: [
            {
                icon: "fas fa-user",
                label: "Общие данные",
            },
            {
                icon: "fas fa-id-badge",
                label: "Ролевая информация",
            },
            {
                icon: "fas fa-shield-check",
                label: "Безопасное обновление",
            },
        ],
        primaryAction: {
            icon: "fas fa-floppy-disk",
            label: "Сохранить изменения",
            pendingLabel: "Сохраняем...",
        },
        secondaryAction: {
            icon: "fas fa-arrow-left",
            label: "Вернуться в профиль",
            to: {
                name: "profile",
            },
        },
    },
    submit: {
        title: "Готово к сохранению?",
        text: "Проверьте данные перед отправкой. Часть изменений может пройти модерацию.",
        cancelAction: {
            label: "Отмена",
            to: {
                name: "profile",
            },
        },
        submitAction: {
            icon: "fas fa-floppy-disk",
            label: "Сохранить профиль",
            pendingLabel: "Сохраняем...",
        },
    },
    successTitle: "Изменения сохранены",
    successIcon: "fas fa-circle-check",
};

export const profileEditFormContent: ProfileEditFormContent = {
    identity: {
        heading: {
            icon: "fas fa-id-card",
            topline: "Общие данные",
            title: "Личная информация",
            text: "Основные сведения о пользователе, которые используются в профиле и системе.",
        },
        labels: {
            lastName: "Фамилия",
            firstName: "Имя",
            middleName: "Отчество",
            birthDate: "Дата рождения",
            gender: "Пол",
            city: "Город",
            about: "О себе",
        },
        aboutPlaceholder: "Краткая информация о пользователе...",
        genderAriaLabel: "Выбрать пол",
        genderOptions: [
            { value: "female", label: "Женский" },
            { value: "male", label: "Мужской" },
            { value: "not_specified", label: "Не указывать" },
        ],
    },
    contacts: {
        heading: {
            icon: "fas fa-paper-plane",
            topline: "Связь и аккаунт",
            title: "Контакты и способы связи",
            text: "Данные, по которым с пользователем можно связаться внутри и вне платформы.",
        },
        labels: {
            email: "Электронная почта",
            phone: "Телефон",
            backupEmail: "Резервный email",
            vkUrl: "VK",
            maxUrl: "MAX",
            preferredContactMethod: "Предпочтительный способ связи",
        },
        emailStatus: "Email меняется отдельным подтверждением",
        phonePlaceholder: "+7 999 123-45-67",
        backupEmailPlaceholder: "backup@example.ru",
        contactMethodAriaLabel: "Выбрать способ связи",
        contactMethodOptions: [
            { value: "email", label: "Электронная почта" },
            { value: "phone", label: "Телефон" },
            { value: "vk", label: "VK" },
            { value: "max", label: "MAX" },
        ],
    },
    display: {
        heading: {
            icon: "fas fa-eye",
            topline: "Отображение и уведомления",
            title: "Параметры отображения профиля",
            text: "Настройки того, как профиль показывается в системе и какие уведомления получает пользователь.",
        },
        toggles: [
            {
                key: "showEmail",
                label: "Показывать email в профиле",
                text: "Электронная почта будет доступна в публичной карточке профиля.",
            },
            {
                key: "showPhone",
                label: "Показывать телефон",
                text: "Телефон будет отображаться в карточке профиля и контактах.",
            },
            {
                key: "emailNotifications",
                label: "Email-уведомления",
                text: "Получение системных и учебных уведомлений на почту.",
            },
            {
                key: "pushNotifications",
                label: "Внутрисистемные уведомления",
                text: "Показывать уведомления о событиях внутри платформы.",
            },
        ],
    },
};
