import { computed, onMounted, ref } from "vue";

import {
    createDashboardItem,
    getDashboardItems,
    removeDashboardItem,
} from "@/components/dashboard/services/dashboard-items.service";
import type {
    DashboardItemCreatePayload,
    DashboardItemDto,
} from "@/components/dashboard/types/dashboard.types";
import { ROLE_LABELS } from "@/app/constants/roles.constants";
import { useAuthStore } from "@/stores/auth.store";
import { notesPageContent } from "@/modules/notes/data/notes-page.data";
import {
    createNotesPageModel,
    mapNotesPageItems,
    mapNotesPageStats,
    type NotesPageNote,
} from "@/modules/notes/mappers/notes-page.mapper";

export function useNotesPage() {
    const authStore = useAuthStore();
    const items = ref<DashboardItemDto[]>([]);
    const isLoading = ref(false);
    const isSaving = ref(false);
    const isCreateModalOpen = ref(false);
    const selectedNote = ref<NotesPageNote | null>(null);
    const errorMessage = ref("");
    const saveError = ref("");

    const model = computed(() => {
        return createNotesPageModel({
            fullName: authStore.userFullName || authStore.user?.email || "",
            roleCode: authStore.activeRole || "",
            roleLabel: authStore.activeRole
                ? ROLE_LABELS[authStore.activeRole]
                : "Пользователь",
            avatarUrl: authStore.avatarUrl || "",
        });
    });

    const notes = computed(() => mapNotesPageItems(items.value));
    const stats = computed(() => mapNotesPageStats(notes.value));
    const calendarRoute = computed(() => {
        return model.value.calendarContent.fullCalendarTo || { name: "student-calendar" };
    });

    async function loadNotes(): Promise<void> {
        isLoading.value = true;
        errorMessage.value = "";

        try {
            items.value = await getDashboardItems();
        } catch (error) {
            errorMessage.value = getErrorMessage(error, "Не удалось загрузить заметки.");
        } finally {
            isLoading.value = false;
        }
    }

    function openCreateModal(): void {
        saveError.value = "";
        isCreateModalOpen.value = true;
    }

    function closeCreateModal(): void {
        isCreateModalOpen.value = false;
    }

    function openNote(note: NotesPageNote): void {
        selectedNote.value = note;
    }

    function closeNote(): void {
        selectedNote.value = null;
    }

    async function submitCreateModal(payload: DashboardItemCreatePayload): Promise<void> {
        const title = payload.title.trim();

        if (!title) {
            return;
        }

        isSaving.value = true;
        saveError.value = "";

        try {
            const item = await createDashboardItem({
                ...payload,
                kind: "note",
                title,
                text: payload.text.trim(),
                eventType: "neutral",
            });

            items.value = [item, ...items.value];
            closeCreateModal();
            notifyDashboardItemsChanged();
        } catch (error) {
            saveError.value = getErrorMessage(error, "Не удалось сохранить заметку.");
        } finally {
            isSaving.value = false;
        }
    }

    async function deleteNote(itemId: number): Promise<void> {
        saveError.value = "";

        try {
            await removeDashboardItem(itemId);
            items.value = items.value.filter((item) => item.id !== itemId);
            if (selectedNote.value?.id === itemId) {
                closeNote();
            }
            notifyDashboardItemsChanged();
        } catch (error) {
            saveError.value = getErrorMessage(error, "Не удалось удалить заметку.");
        }
    }

    onMounted(() => {
        void loadNotes();
    });

    return {
        calendarRoute,
        content: notesPageContent,
        errorMessage,
        isCreateModalOpen,
        isLoading,
        isSaving,
        model,
        notes,
        saveError,
        selectedNote,
        stats,
        closeCreateModal,
        closeNote,
        deleteNote,
        loadNotes,
        openCreateModal,
        openNote,
        submitCreateModal,
    };
}

function notifyDashboardItemsChanged(): void {
    window.dispatchEvent(new Event("dashboard-items:changed"));
}

function getErrorMessage(error: unknown, fallback: string): string {
    return error instanceof Error && error.message ? error.message : fallback;
}
