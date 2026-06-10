import type { SettingsPasswordFormContent } from "@/modules/settings/types/settings.types";

export const securityPasswordFormContent: SettingsPasswordFormContent = {
    fields: [
        {
            key: "currentPassword",
            label: "Текущий пароль",
            text: "Введите пароль, который используется сейчас.",
            autocomplete: "current-password",
        },
        {
            key: "newPassword",
            label: "Новый пароль",
            text: "Используйте сложный пароль из букв, цифр и символов.",
            autocomplete: "new-password",
        },
        {
            key: "newPasswordConfirm",
            label: "Повторите новый пароль",
            text: "Повтор нужен, чтобы избежать ошибки при вводе.",
            autocomplete: "new-password",
        },
    ],
    errorIcon: "fas fa-triangle-exclamation",
    submitIcon: "fas fa-floppy-disk",
    submitLabel: "Изменить пароль",
    submittingLabel: "Сохраняем...",
};
