import type { DashboardPageScaffoldModel } from "@/components/dashboard/types/dashboard.types";
import type { ProfileAchievementsPageModel } from "@/modules/profile/types/profile.types";

export function createEmptyProfileAchievementsModel(
    scaffold: DashboardPageScaffoldModel,
): ProfileAchievementsPageModel {
    return {
        scaffold,
        hero: {
            topline: "Достижения и награды",
            icon: "fas fa-award",
            title: "Портфолио достижений внутри платформы",
            text:
                "Здесь появятся сертификаты платформы, личные награды и загруженные документы пользователя.",
            badges: [
                {
                    icon: "fas fa-certificate",
                    label: "Сертификаты платформы",
                },
                {
                    icon: "fas fa-medal",
                    label: "Личные награды",
                },
                {
                    icon: "fas fa-cloud-arrow-up",
                    label: "Загрузка документов",
                },
            ],
            statusRows: [
                {
                    label: "Сертификаты платформы",
                    value: 0,
                },
                {
                    label: "Личные документы",
                    value: 0,
                },
                {
                    label: "Награды",
                    value: 0,
                },
                {
                    label: "На проверке",
                    value: 0,
                },
            ],
            summaryTitle: "Портфолио пользователя",
            summarySubtitle: "Текущая сводка",
        },
        stats: [
            {
                key: "platform-certificates",
                icon: "fas fa-certificate",
                value: 0,
                label: "сертификатов платформы",
            },
            {
                key: "personal-documents",
                icon: "fas fa-file-arrow-up",
                value: 0,
                label: "личных документов",
            },
            {
                key: "verified",
                icon: "fas fa-shield-check",
                value: 0,
                label: "подтвержденных материалов",
            },
            {
                key: "pending",
                icon: "fas fa-clock",
                value: 0,
                label: "документов на проверке",
            },
        ],
        filters: {
            icon: "fas fa-sliders",
            topline: "Управление коллекцией",
            title: "Фильтры и представление",
            text: "Документы можно будет фильтровать по источнику и категории после их добавления.",
            uploadLabel: "Добавить документ",
            uploadIcon: "fas fa-paperclip",
            isUploadEnabled: false,
            sourceAriaLabel: "Источник достижений",
            sources: [
                {
                    key: "all",
                    label: "Все материалы",
                },
                {
                    key: "platform",
                    label: "Платформенные",
                },
                {
                    key: "personal",
                    label: "Личные",
                },
            ],
            categories: [
                {
                    key: "all",
                    label: "Все",
                },
                {
                    key: "certificate",
                    label: "Сертификаты",
                },
                {
                    key: "diploma",
                    label: "Дипломы",
                },
                {
                    key: "gratitude",
                    label: "Благодарности",
                },
                {
                    key: "award",
                    label: "Награды",
                },
                {
                    key: "methodic",
                    label: "Методические",
                },
            ],
        },
        featuredContent: {
            icon: "fas fa-star",
            topline: "Избранное",
            title: "Ключевые достижения",
            text: "Избранные материалы пользователя будут отображаться в этом блоке.",
            emptyIcon: "fas fa-star",
            emptyTitle: "Избранных достижений пока нет",
            emptyText: "Добавленные в избранное документы появятся здесь.",
        },
        documentsContent: {
            icon: "fas fa-certificate",
            topline: "Коллекция документов",
            title: "Все сертификаты и награды",
            text: "Основной каталог сертификатов, наград и пользовательских документов.",
            emptyIcon: "fas fa-file-circle-plus",
            emptyTitle: "Данные пока не добавлены",
            emptyText: "Сертификаты и документы появятся после подключения портфолио.",
        },
        featuredDocuments: [],
        documents: [],
    };
}
