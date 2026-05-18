import { onMounted, reactive, ref, watch } from "vue";

import { fetchPublicTeachersPage } from "@/modules/public/api/public-teachers.api";
import { mapPublicTeachersPage } from "@/modules/public/mappers/publicTeachers.mapper";
import type {
    PublicTeachersPageData,
    PublicTeachersQuery,
} from "@/modules/public/types/public-teachers.types";

function createEmptyPageData(): PublicTeachersPageData {
    return {
        organization: null,
        subjects: [],
        teachers: [],
        meta: {
            teachersCount: 0,
            subjectsCount: 0,
            isFallback: true,
            search: "",
            subject: "",
            position: "",
        },
    };
}

export function useTeachersPage() {
    const pageData = ref<PublicTeachersPageData>(createEmptyPageData());
    const isLoading = ref(false);
    const errorMessage = ref("");

    const filters = reactive<Required<PublicTeachersQuery>>({
        search: "",
        subject: "",
        position: "",
    });

    let debounceTimer: number | null = null;

    async function loadTeachers(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            const response = await fetchPublicTeachersPage({
                search: filters.search,
                subject: filters.subject,
                position: filters.position,
            });

            pageData.value = mapPublicTeachersPage(response);

            if (pageData.value.meta.message) {
                errorMessage.value = pageData.value.meta.message;
            }
        } catch (error) {
            errorMessage.value = error instanceof Error
                ? error.message
                : "Не удалось загрузить преподавателей. Попробуйте обновить страницу.";
        } finally {
            isLoading.value = false;
        }
    }

    function scheduleLoadTeachers(): void {
        if (debounceTimer) {
            window.clearTimeout(debounceTimer);
        }

        debounceTimer = window.setTimeout(() => {
            void loadTeachers();
        }, 350);
    }

    function resetFilters(): void {
        filters.search = "";
        filters.subject = "";
        filters.position = "";
    }

    watch(
        () => [
            filters.search,
            filters.subject,
            filters.position,
        ],
        () => {
            scheduleLoadTeachers();
        },
    );

    onMounted(() => {
        void loadTeachers();
    });

    return {
        pageData,
        filters,
        isLoading,
        errorMessage,
        loadTeachers,
        resetFilters,
    };
}