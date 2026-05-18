<script setup lang="ts">
import PublicSectionHead from "@/modules/public/components/shared/PublicSectionHead.vue";
import TeacherCard from "@/modules/public/components/teachers/TeacherCard.vue";
import TeachersOrganizationFilter from "@/modules/public/components/teachers/TeachersOrganizationFilter.vue";
import type {
    PublicTeacher,
    PublicTeachersPageData,
    TeachersCatalogContent,
} from "@/modules/public/types/public-teachers.types";

interface Props {
    content: TeachersCatalogContent;
    pageData: PublicTeachersPageData;
    search: string;
    subject: string;
    isLoading: boolean;
    errorMessage: string;
}

interface Emits {
    (event: "update:search", value: string): void;
    (event: "update:subject", value: string): void;
    (event: "reset-filters"): void;
    (event: "open-teacher", teacher: PublicTeacher): void;
}

defineProps<Props>();
const emit = defineEmits<Emits>();
</script>

<template>
    <section
        id="teachers-catalog"
        class="section teachers-catalog"
    >
        <div class="container">
            <PublicSectionHead
                :label="content.label"
                :title="content.title"
                :description="content.description"
            />

            <div class="teachers-shell fade-in visible">
                <TeachersOrganizationFilter
                    :organization="pageData.organization"
                    :subjects="pageData.subjects"
                    :search="search"
                    :subject="subject"
                    :is-fallback="pageData.meta.isFallback"
                    :teachers-count="pageData.meta.teachersCount"
                    :search-placeholder="content.searchPlaceholder"
                    :subject-placeholder="content.subjectPlaceholder"
                    @update:search="emit('update:search', $event)"
                    @update:subject="emit('update:subject', $event)"
                    @reset="emit('reset-filters')"
                />

                <div
                    v-if="errorMessage"
                    class="teachers-api-status warning"
                >
                    <i class="fas fa-info-circle"></i>
                    <span>{{ errorMessage }}</span>
                </div>

                <div
                    v-if="isLoading"
                    class="teachers-empty-state"
                >
                    <div class="teachers-empty-icon">
                        <i class="fas fa-spinner teachers-loading-icon"></i>
                    </div>

                    <h3>
                        Загружаем преподавателей
                    </h3>

                    <p>
                        Получаем актуальный список преподавателей выбранной образовательной организации.
                    </p>
                </div>

                <div
                    v-else-if="pageData.teachers.length"
                    class="teachers-grid"
                >
                    <TeacherCard
                        v-for="teacher in pageData.teachers"
                        :key="teacher.id"
                        :teacher="teacher"
                        @open="emit('open-teacher', $event)"
                    />
                </div>

                <div
                    v-else-if="!pageData.organization"
                    class="teachers-empty-state"
                >
                    <div class="teachers-empty-icon">
                        <i class="fas fa-building-columns"></i>
                    </div>

                    <h3>
                        {{ content.emptyOrganizationsTitle }}
                    </h3>

                    <p>
                        {{ content.emptyOrganizationsText }}
                    </p>
                </div>

                <div
                    v-else
                    class="teachers-empty-state"
                >
                    <div class="teachers-empty-icon">
                        <i class="fas fa-chalkboard-user"></i>
                    </div>

                    <h3>
                        {{ content.emptyTitle }}
                    </h3>

                    <p>
                        {{ content.emptyText }}
                    </p>
                </div>
            </div>
        </div>
    </section>
</template>
