<script setup lang="ts">
import { computed } from "vue";

import { useI18n } from "@/composables/useI18n";
import PublicLayout from "@/layouts/PublicLayout.vue";
import TeacherModal from "@/modules/public/components/teachers/TeacherModal.vue";
import TeachersCatalogSection from "@/modules/public/components/teachers/TeachersCatalogSection.vue";
import TeachersCtaSection from "@/modules/public/components/teachers/TeachersCtaSection.vue";
import TeachersHeroSection from "@/modules/public/components/teachers/TeachersHeroSection.vue";
import { useTeacherModal } from "@/modules/public/composables/useTeacherModal";
import { useTeachersPage } from "@/modules/public/composables/useTeachersPage";
import { teachersPageContent } from "@/modules/public/data/teachers-page.data";

const { localizePublicContent } = useI18n();

const content = computed(() => {
    return localizePublicContent(teachersPageContent);
});

const {
    pageData,
    filters,
    isLoading,
    errorMessage,
    resetFilters,
} = useTeachersPage();

const {
    selectedTeacher,
    isTeacherModalOpen,
    openTeacher,
    closeTeacher,
} = useTeacherModal();
</script>

<template>
    <PublicLayout>
        <TeachersHeroSection :content="content.hero" />

        <TeachersCatalogSection
            :content="content.catalog"
            :page-data="pageData"
            :search="filters.search"
            :subject="filters.subject"
            :is-loading="isLoading"
            :error-message="errorMessage"
            @update:search="filters.search = $event"
            @update:subject="filters.subject = $event"
            @reset-filters="resetFilters"
            @open-teacher="openTeacher"
        />

        <TeachersCtaSection :content="content.cta" />

        <TeacherModal
            :teacher="selectedTeacher"
            :is-open="isTeacherModalOpen"
            @close="closeTeacher"
        />
    </PublicLayout>
</template>
