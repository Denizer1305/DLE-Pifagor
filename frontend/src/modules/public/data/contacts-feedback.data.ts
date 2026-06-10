import type { ContactFeedbackContent } from "@/modules/public/types/contact.types";

export const contactFeedbackContent: ContactFeedbackContent = {
    label: "Обратная связь",
    title: "Остались вопросы или есть предложения?",
    description:
        "Напишите нам — мы ответим в течение одного рабочего дня. Прикрепите файлы, если нужно.",
    topics: [
        {
            value: "question",
            label: "Вопрос",
        },
        {
            value: "partnership",
            label: "Сотрудничество",
        },
        {
            value: "organization_connection",
            label: "Подключение организации",
        },
        {
            value: "technical_support",
            label: "Техническая поддержка",
        },
        {
            value: "bug",
            label: "Ошибка в платформе",
        },
        {
            value: "other",
            label: "Другое",
        },
    ],
    fields: {
        topic: {
            label: "Тема обращения",
        },
        name: {
            label: "Ваше имя",
            placeholder: "Иван Иванов",
        },
        email: {
            label: "Электронная почта",
            placeholder: "example@mail.ru",
        },
        phone: {
            label: "Телефон",
            placeholder: "+7 (900) 000-00-00",
        },
        organization: {
            label: "Организация",
            placeholder: "Название образовательной организации",
        },
        subject: {
            label: "Краткая тема",
            placeholder: "Например: подключение организации",
        },
        message: {
            label: "Сообщение",
            placeholder: "О чём хотите рассказать?",
        },
        files: {
            label: "Прикрепить файлы",
            hint:
                "Можно выбрать до 5 файлов. Поддерживаются изображения, PDF, DOC и DOCX. Размер одного файла — до 5 МБ.",
        },
        consent:
            "Я даю согласие на обработку персональных данных в соответствии с Политикой конфиденциальности.",
    },
    submitLabel: "Отправить сообщение",
    submittingLabel: "Отправляем...",
    successTitle: "Сообщение отправлено",
    successText:
        "Спасибо! Мы получили ваше обращение и свяжемся с вами после обработки заявки.",
    resetLabel: "Отправить ещё одно сообщение",
};
