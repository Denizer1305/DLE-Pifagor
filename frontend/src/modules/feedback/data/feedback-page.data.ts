import type { FeedbackPageContent } from "@/modules/feedback/types/feedback.types";

export const feedbackPageContent: FeedbackPageContent = {
    loadingText: "Готовим форму обращения...",
    errorTitle: "Не удалось подготовить страницу",
    retryLabel: "Повторить",
    retryIcon: "fas fa-rotate-right",
    hero: {
        badge: "Поддержка",
        title: "Обращения",
        text:
            "Опишите вопрос, ошибку или предложение. Обращение попадет в службу поддержки платформы и будет обработано администратором.",
    },
    info: {
        title: "Как мы работаем с обращениями",
        text: "Чем точнее описана ситуация, тем быстрее команда сможет помочь.",
        items: [
            {
                icon: "fas fa-clock",
                title: "Срок ответа",
                text: "Обычно отвечаем в течение одного рабочего дня.",
            },
            {
                icon: "fas fa-shield-halved",
                title: "Безопасность",
                text: "Не передавайте пароль и коды подтверждения в тексте обращения.",
            },
            {
                icon: "fas fa-paperclip",
                title: "Детали",
                text: "Укажите страницу, действие и ожидаемый результат, если сообщаете об ошибке.",
            },
        ],
    },
    form: {
        title: "Новое обращение",
        text: "Заполните форму, и мы передадим сообщение ответственному специалисту.",
        topicLabel: "Тема обращения",
        subjectLabel: "Краткая тема",
        subjectPlaceholder: "Например: не открывается календарь",
        messageLabel: "Сообщение",
        messagePlaceholder: "Опишите ситуацию, вопрос или предложение.",
        filesLabel: "Прикрепить файлы",
        filesHint: "До 5 файлов: JPG, PNG, WEBP, PDF, DOC и DOCX. Каждый файл до 5 МБ.",
        filesButtonLabel: "Выбрать файлы",
        removeFileLabel: "Убрать файл",
        nameLabel: "Имя",
        emailLabel: "Email",
        phoneLabel: "Телефон",
        organizationLabel: "Организация",
        consentLabel: "Я даю согласие на обработку персональных данных.",
        submitLabel: "Отправить обращение",
        submittingLabel: "Отправляем...",
        successTitle: "Обращение отправлено",
        successText: "Спасибо. Мы получили ваше сообщение и передали его в обработку.",
        resetLabel: "Создать еще одно обращение",
    },
    topics: [
        { value: "question", label: "Вопрос" },
        { value: "technical_support", label: "Техническая поддержка" },
        { value: "bug", label: "Ошибка в платформе" },
        { value: "organization_connection", label: "Подключение организации" },
        { value: "partnership", label: "Сотрудничество" },
        { value: "other", label: "Другое" },
    ],
};
