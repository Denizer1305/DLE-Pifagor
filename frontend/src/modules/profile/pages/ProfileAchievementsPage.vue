<script setup lang="ts">
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import DashboardPageScaffold from "@/components/dashboard/layout/DashboardPageScaffold.vue";

import ProfileAchievementsFilters from "@/modules/profile/components/ProfileAchievementsFilters.vue";
import ProfileAchievementsHero from "@/modules/profile/components/ProfileAchievementsHero.vue";
import ProfileAchievementsStats from "@/modules/profile/components/ProfileAchievementsStats.vue";
import ProfileDocumentPreviewModal from "@/modules/profile/components/ProfileDocumentPreviewModal.vue";
import ProfileDocumentsGrid from "@/modules/profile/components/ProfileDocumentsGrid.vue";
import ProfileFeaturedAchievements from "@/modules/profile/components/ProfileFeaturedAchievements.vue";

import { useProfilePage } from "@/modules/profile/composables/useProfilePage";
import { redirectAfterLogout } from "@/modules/auth/utils/auth-redirect.utils";
import { useAuthStore } from "@/stores/auth.store";

import type {
    ProfileAchievementDocumentModel,
    ProfileAchievementsPageModel,
} from "@/modules/profile/types/profile.types";

const router = useRouter();
const authStore = useAuthStore();

const {
    pageModel,
    isLoading,
    errorMessage,
    loadProfile,
} = useProfilePage();

const activeSource = ref("all");
const activeCategory = ref("all");
const previewDocument = ref<ProfileAchievementDocumentModel | null>(null);

const achievementsModel = computed<ProfileAchievementsPageModel | null>(() => {
    if (!pageModel.value) {
        return null;
    }

    return createMockAchievementsModel(pageModel.value.scaffold);
});

const filteredDocuments = computed(() => {
    const model = achievementsModel.value;

    if (!model) {
        return [];
    }

    return model.documents.filter((document) => {
        const sourceMatches = activeSource.value === "all" ||
            document.sourceType === activeSource.value;

        const categoryMatches = activeCategory.value === "all" ||
            document.category === activeCategory.value;

        return sourceMatches && categoryMatches;
    });
});

const featuredDocuments = computed(() => {
    const model = achievementsModel.value;

    if (!model) {
        return [];
    }

    return model.featuredDocuments;
});

const isPreviewOpen = computed(() => {
    return Boolean(previewDocument.value);
});

function openPreview(document: ProfileAchievementDocumentModel): void {
    previewDocument.value = document;
}

function closePreview(): void {
    previewDocument.value = null;
}

function handleUpload(): void {
    // Подключим загрузку после реализации portfolio backend.
}

async function logout(): Promise<void> {
    await authStore.logout();
    await redirectAfterLogout(router);
}

function createMockAchievementsModel(
    scaffold: ProfileAchievementsPageModel["scaffold"],
): ProfileAchievementsPageModel {
    return {
        scaffold,
        hero: {
            topline: "Достижения и награды",
            icon: "fas fa-award",
            title: "Портфолио достижений внутри платформы",
            text:
                "Здесь собраны сертификаты платформы, личные награды и загруженные документы. Раздел помогает хранить подтверждения профессионального роста и формировать аккуратное цифровое портфолио.",
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
                    label: "Загрузка своих документов",
                },
            ],
            statusRows: [
                {
                    label: "Сертификаты платформы",
                    value: 6,
                },
                {
                    label: "Личные документы",
                    value: 4,
                },
                {
                    label: "Награды",
                    value: 3,
                },
                {
                    label: "На проверке",
                    value: 1,
                },
            ],
        },
        stats: [
            {
                key: "platform-certificates",
                icon: "fas fa-certificate",
                value: 6,
                label: "сертификатов платформы",
            },
            {
                key: "personal-documents",
                icon: "fas fa-file-arrow-up",
                value: 4,
                label: "личных документа",
            },
            {
                key: "verified",
                icon: "fas fa-shield-check",
                value: 9,
                label: "подтверждённых материалов",
            },
            {
                key: "pending",
                icon: "fas fa-clock",
                value: 1,
                label: "документ на проверке",
            },
        ],
        filters: {
            uploadLabel: "Добавить документ",
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
        featuredDocuments: [
            {
                id: "featured-1",
                title: "Методика цифрового урока",
                subtitle:
                    "Сертификат платформы за успешное завершение программы повышения квалификации.",
                icon: "fas fa-file-pdf",
                sourceLabel: "Платформа",
                categoryLabel: "Сертификат",
                sourceType: "platform",
                category: "certificate",
                isFeatured: true,
                previewLabel: "Предпросмотр",
                downloadLabel: "Скачать",
            },
            {
                id: "featured-2",
                title: "Грамота за педагогическое мастерство",
                subtitle:
                    "Профессиональная награда, подтверждающая личные достижения в образовательной практике.",
                icon: "fas fa-trophy",
                sourceLabel: "Личное",
                categoryLabel: "Награда",
                sourceType: "personal",
                category: "award",
                isFeatured: true,
                previewLabel: "Предпросмотр",
                downloadLabel: "Открыть",
            },
        ],
        documents: [
            {
                id: 1,
                title: "Сертификат о завершении программы",
                subtitle: "Методика цифрового урока · 12.03.2026",
                icon: "fas fa-file-pdf",
                sourceLabel: "Платформа",
                categoryLabel: "Сертификат",
                sourceType: "platform",
                category: "certificate",
                previewLabel: "Предпросмотр",
                downloadLabel: "Скачать",
            },
            {
                id: 2,
                title: "Сертификат платформы Пифагор",
                subtitle: "Инструменты проверки и аналитики · 28.02.2026",
                icon: "fas fa-file-pdf",
                sourceLabel: "Платформа",
                categoryLabel: "Сертификат",
                sourceType: "platform",
                category: "certificate",
                previewLabel: "Предпросмотр",
                downloadLabel: "Скачать",
            },
            {
                id: 3,
                title: "Сертификат повышения квалификации",
                subtitle: "Современные цифровые образовательные практики · 14.01.2026",
                icon: "fas fa-file-pdf",
                sourceLabel: "Платформа",
                categoryLabel: "Методическое",
                sourceType: "platform",
                category: "methodic",
                previewLabel: "Предпросмотр",
                downloadLabel: "Скачать",
            },
            {
                id: 4,
                title: "Грамота за педагогическое мастерство",
                subtitle: "Загружено 18.02.2026 · PDF",
                icon: "fas fa-trophy",
                sourceLabel: "Личное",
                categoryLabel: "Награда",
                sourceType: "personal",
                category: "award",
                previewLabel: "Предпросмотр",
                downloadLabel: "Открыть",
            },
            {
                id: 5,
                title: "Благодарственное письмо",
                subtitle: "Загружено 05.01.2026 · JPG",
                icon: "fas fa-award",
                sourceLabel: "Личное",
                categoryLabel: "Благодарность",
                sourceType: "personal",
                category: "gratitude",
                previewLabel: "Предпросмотр",
                downloadLabel: "Открыть",
            },
        ],
    };
}
</script>

<template>
    <DashboardPageScaffold
        v-if="achievementsModel"
        :model="achievementsModel.scaffold"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем достижения и награды..."
        @reload="loadProfile"
        @logout="logout"
    >
        <ProfileAchievementsHero :hero="achievementsModel.hero" />

        <ProfileAchievementsStats :stats="achievementsModel.stats" />

        <ProfileAchievementsFilters
            v-model:active-source="activeSource"
            v-model:active-category="activeCategory"
            :filters="achievementsModel.filters"
            @upload="handleUpload"
        />

        <ProfileFeaturedAchievements
            :documents="featuredDocuments"
            @preview="openPreview"
        />

        <ProfileDocumentsGrid
            :documents="filteredDocuments"
            @preview="openPreview"
        />

        <ProfileDocumentPreviewModal
            :is-open="isPreviewOpen"
            :document="previewDocument"
            @close="closePreview"
        />
    </DashboardPageScaffold>

    <div
        v-else
        class="dashboard-loading-state"
    >
        <i class="fas fa-spinner"></i>
        <span>Загружаем достижения и награды...</span>
    </div>
</template>