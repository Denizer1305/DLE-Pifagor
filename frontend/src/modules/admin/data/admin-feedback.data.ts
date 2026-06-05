import type {
    AdminFeedbackStatus,
    AdminFeedbackTopic,
} from "@/modules/admin/types/admin-feedback.types";

export const adminFeedbackContent = {
    badge: "Поддержка",
    title: "Обращения пользователей",
    text: "Заявки из публичной формы обратной связи и запросы поддержки платформы.",
    searchPlaceholder: "Поиск по имени, email, теме или тексту",
    emptyTitle: "Обращений не найдено",
    emptyText: "Новые сообщения появятся здесь после отправки формы обратной связи.",
    loadingText: "Загружаем обращения...",
    errorText: "Не удалось загрузить обращения.",
};

export const adminFeedbackStatusOptions = [
    { value: "", label: "Все статусы" },
    { value: "new", label: "Новое" },
    { value: "in_progress", label: "В работе" },
    { value: "answered", label: "Ответ отправлен" },
    { value: "closed", label: "Закрыто" },
    { value: "spam", label: "Спам" },
];

export const adminFeedbackTopicOptions = [
    { value: "", label: "Все темы" },
    { value: "question", label: "Вопрос" },
    { value: "partnership", label: "Сотрудничество" },
    { value: "organization_connection", label: "Подключение организации" },
    { value: "technical_support", label: "Техническая поддержка" },
    { value: "bug", label: "Ошибка в платформе" },
    { value: "other", label: "Другое" },
];

export function getFeedbackStatusLabel(status: AdminFeedbackStatus): string {
    return adminFeedbackStatusOptions.find((option) => option.value === status)?.label || status;
}

export function getFeedbackTopicLabel(topic: AdminFeedbackTopic): string {
    return adminFeedbackTopicOptions.find((option) => option.value === topic)?.label || topic;
}
