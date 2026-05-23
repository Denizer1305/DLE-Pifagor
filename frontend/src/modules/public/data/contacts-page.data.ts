import heroLogo from "@/assets/brand/logo/themes/light/hero-logo.svg";
import maxIcon from "@/assets/image/icons/max.svg";

import type {
    ContactFeedbackContent,
    ContactsPageContent,
} from "@/modules/public/types/contact.types";

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

export const contactsPageContent: ContactsPageContent = {
    hero: {
        badges: [
            {
                icon: "fas fa-location-dot",
                text: "Адрес и карта",
            },
            {
                icon: "fas fa-comments",
                text: "Всегда на связи",
            },
        ],
        title: "Контакты",
        subtitle:
            "Если у вас есть вопрос, предложение или интерес к сотрудничеству — мы всегда открыты к диалогу",
        description:
            "Здесь вы найдёте адрес, электронную почту, телефон и карту с точкой расположения. Всё самое важное собрано в одном месте, чтобы связаться с нами было легко и удобно.",
        highlights: [
            "Быстро найти адрес и построить маршрут.",
            "Написать нам по почте или связаться по телефону.",
            "Обсудить использование платформы или возможное партнёрство.",
        ],
        actions: [
            {
                label: "Смотреть контакты",
                href: "#contact-main",
                variant: "primary",
                icon: "fas fa-arrow-right",
            },
            {
                label: "Открыть карту",
                href: "#contact-map",
                variant: "light",
            },
        ],
        logo: {
            src: heroLogo,
            alt: "ЦОС «Пифагор»",
        },
    },

    main: {
        label: "Контактная информация",
        title: "Как с нами связаться",
        description:
            "Выберите удобный способ связи: написать письмо, позвонить, открыть карту или быстро перейти в социальные сети.",
        info: {
            toplineIcon: "fas fa-address-book",
            topline: "Основные данные",
            title: "Контакты",
            text:
                "Основная информация для связи с платформой, командой проекта и потенциальными партнёрами.",
            items: [
                {
                    icon: "fas fa-location-dot",
                    title: "Адрес",
                    text: "г. Владимир, ул. Дворянская, д. 27",
                },
                {
                    icon: "fas fa-envelope",
                    title: "Электронная почта",
                    text: "Pifagor-Platform33@yandex.ru",
                    href: "mailto:Pifagor-Platform33@yandex.ru",
                },
                {
                    icon: "fas fa-phone",
                    title: "Телефон",
                    text: "+7 (900) 000-00-00",
                    href: "tel:+79000000000",
                },
                {
                    icon: "fas fa-building",
                    title: "По вопросам сотрудничества",
                    text:
                        "Пишите нам на почту или используйте форму обратной связи на платформе.",
                },
            ],
            actions: [
                {
                    icon: "fas fa-paper-plane",
                    label: "Написать письмо",
                    href: "mailto:Pifagor-Platform33@yandex.ru",
                },
                {
                    icon: "fas fa-phone-volume",
                    label: "Позвонить",
                    href: "tel:+79000000000",
                },
            ],
        },
        hours: {
            toplineIcon: "fas fa-clock",
            topline: "График связи",
            title: "Когда лучше обращаться",
            text:
                "Мы стараемся отвечать быстро и по существу. Ниже — удобный ориентир, когда и как лучше с нами связаться.",
            items: [
                {
                    title: "Будние дни",
                    text: "Пн–Пт, с 09:00 до 18:00",
                },
                {
                    title: "Электронная почта",
                    text: "Можно писать в любое время",
                },
                {
                    title: "Телефон",
                    text: "Удобно для быстрого уточнения",
                },
                {
                    title: "Партнёрские запросы",
                    text: "Лучше направлять письмом",
                },
            ],
        },
        socials: {
            toplineIcon: "fas fa-hashtag",
            topline: "Социальные сети",
            title: "Мы онлайн",
            text:
                "Следите за новостями платформы, обновлениями проекта и новыми возможностями в наших каналах.",
            items: [
                {
                    icon: "fab fa-vk",
                    title: "VK",
                    text: "Новости платформы и публикации",
                    href: "#",
                },
                {
                    icon: "fab fa-telegram",
                    title: "Telegram",
                    text: "Быстрая связь и объявления",
                    href: "#",
                },
                {
                    image: maxIcon,
                    title: "MAX",
                    text: "Дополнительный канал связи",
                    href: "#",
                },
            ],
        },
        map: {
            toplineIcon: "fas fa-map",
            topline: "Яндекс Карты",
            title: "Где мы находимся",
            text:
                "На карте показано расположение платформы. Вы можете сразу открыть маршрут и посмотреть точную точку.",
            address: "г. Владимир, ул. Дворянская, д. 27",
            mapTitle: "Карта расположения ЦОС «Пифагор»",
            mapSrc:
                "https://yandex.ru/map-widget/v1/?ll=40.397102%2C56.126674&z=16&text=%D0%92%D0%BB%D0%B0%D0%B4%D0%B8%D0%BC%D0%B8%D1%80%2C%20%D1%83%D0%BB.%20%D0%94%D0%B2%D0%BE%D1%80%D1%8F%D0%BD%D1%81%D0%BA%D0%B0%D1%8F%2C%2027",
            fallbackText:
                "Карта временно недоступна. Ниже остаётся адрес, по которому нас можно найти.",
        },
        find: {
            toplineIcon: "fas fa-route",
            topline: "Как нас найти",
            title: "Маршрут без лишних сложностей",
            text:
                "Всё устроено так, чтобы до нас было легко добраться и быстро сориентироваться на месте.",
            steps: [
                {
                    number: "01",
                    title: "Откройте карту",
                    text:
                        "Перейдите к карте на этой странице и посмотрите точное расположение.",
                },
                {
                    number: "02",
                    title: "Постройте маршрут",
                    text:
                        "Используйте Яндекс Карты, чтобы выбрать самый удобный путь на автомобиле или пешком.",
                },
                {
                    number: "03",
                    title: "Свяжитесь заранее",
                    text:
                        "Если планируется визит, лучше написать или позвонить заранее, чтобы мы могли сориентировать вас точнее.",
                },
            ],
            notes: [
                "Для подробных вопросов лучше использовать электронную почту.",
                "Для быстрых уточнений удобнее позвонить.",
                "Для сотрудничества и партнёрства лучше сразу коротко описать запрос в письме.",
            ],
        },
    },

    feedback: contactFeedbackContent,

    cta: {
        title: "Будем рады вашему сообщению",
        text:
            "Если вы хотите задать вопрос, обсудить внедрение платформы или предложить сотрудничество, напишите нам или свяжитесь по телефону. Мы открыты к общению, идеям и сильным партнёрствам.",
        note:
            "Мы ценим живой диалог, внимательную обратную связь и долгосрочное сотрудничество.",
        actions: [
            {
                label: "Написать нам",
                href: "mailto:Pifagor-Platform33@yandex.ru",
                variant: "primary",
                icon: "fas fa-arrow-right",
            },
            {
                label: "Позвонить",
                href: "tel:+79000000000",
                variant: "secondary",
            },
        ],
    },
};
