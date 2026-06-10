<script setup lang="ts">
import { computed, ref } from "vue";

import ProfileAchievementsFilters from "@/modules/profile/components/ProfileAchievementsFilters.vue";
import ProfileAchievementsHero from "@/modules/profile/components/ProfileAchievementsHero.vue";
import ProfileAchievementsStats from "@/modules/profile/components/ProfileAchievementsStats.vue";
import ProfileDocumentPreviewModal from "@/modules/profile/components/ProfileDocumentPreviewModal.vue";
import ProfileDocumentsGrid from "@/modules/profile/components/ProfileDocumentsGrid.vue";
import ProfileFeaturedAchievements from "@/modules/profile/components/ProfileFeaturedAchievements.vue";
import ProfilePageShell from "@/modules/profile/components/ProfilePageShell.vue";

import { useProfilePage } from "@/modules/profile/composables/useProfilePage";
import { createEmptyProfileAchievementsModel } from "@/modules/profile/data/profile-achievements.data";

import type {
    ProfileAchievementDocumentModel,
    ProfileAchievementsPageModel,
} from "@/modules/profile/types/profile.types";

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

    return createEmptyProfileAchievementsModel(pageModel.value.scaffold);
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

</script>

<template>
    <ProfilePageShell
        :model="achievementsModel?.scaffold"
        :is-loading="isLoading"
        :error-message="errorMessage"
        loading-text="Загружаем достижения и награды..."
        @reload="loadProfile"
    >
        <template v-if="achievementsModel">
        <ProfileAchievementsHero :hero="achievementsModel.hero" />

        <ProfileAchievementsStats :stats="achievementsModel.stats" />

        <ProfileAchievementsFilters
            v-model:active-source="activeSource"
            v-model:active-category="activeCategory"
            :filters="achievementsModel.filters"
            @upload="handleUpload"
        />

        <ProfileFeaturedAchievements
            :content="achievementsModel.featuredContent"
            :documents="featuredDocuments"
            @preview="openPreview"
        />

        <ProfileDocumentsGrid
            :content="achievementsModel.documentsContent"
            :documents="filteredDocuments"
            @preview="openPreview"
        />

        <ProfileDocumentPreviewModal
            :is-open="isPreviewOpen"
            :document="previewDocument"
            @close="closePreview"
        />
        </template>
    </ProfilePageShell>
</template>
