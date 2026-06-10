<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import TeacherSubjectDetailsPanel from "../components/teacher-subjects/TeacherSubjectDetailsPanel.vue";
import TeacherSubjectForm from "../components/teacher-subjects/TeacherSubjectForm.vue";
import TeacherSubjectListTable from "../components/teacher-subjects/TeacherSubjectListTable.vue";
import { useOrganizationDictionaries, useTeacherSubjects } from "../composables";
import type {
    OrganizationTableActionKey,
    TeacherSubjectDto,
    TeacherSubjectId,
    TeacherSubjectListItemView,
} from "../types";

type FormMode = "create" | "edit";

const {
    emptyState,
    errorMessage,
    fieldErrors,
    filters,
    form,
    hasItems,
    isActionLoading,
    isDetailsLoading,
    isLoading,
    isSubmitting,
    items,
    selectedDetails,
    selectedItem,
    tableConfig,
    viewItems,
    clearSelection,
    createItem,
    deactivateItem,
    fillForm,
    loadDetails,
    loadItems,
    resetForm,
    restoreItem,
    selectItem,
    setPrimaryItem,
    setSearch,
    submitSearch,
    updateItem,
} = useTeacherSubjects();

const {
    reloadDictionaries,
    subjectOptions,
    teacherOptions,
} = useOrganizationDictionaries();

const isFormModalOpen = ref(false);
const formMode = ref<FormMode>("create");

const hasActiveFilters = computed(() => {
    return Boolean(filters.search);
});

function updateFormModel(value: typeof form): void {
    Object.assign(form, value);
}

function openCreateForm(): void {
    formMode.value = "create";
    resetForm();
    isFormModalOpen.value = true;
}

async function openEditForm(id?: TeacherSubjectId): Promise<void> {
    formMode.value = "edit";

    if (id) {
        await selectAndWaitDetails(id);
    } else if (selectedItem.value) {
        fillForm(selectedItem.value);
    }

    isFormModalOpen.value = true;
}

function closeFormModal(): void {
    isFormModalOpen.value = false;
    resetForm();
}

async function submitForm(): Promise<void> {
    if (formMode.value === "create") {
        await createItem();
    } else if (selectedItem.value) {
        await updateItem(selectedItem.value.id);
    }

    if (!Object.keys(fieldErrors.value).length) {
        await reloadDictionaries();
        isFormModalOpen.value = false;
    }
}

async function selectAndWaitDetails(id: TeacherSubjectId): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item: TeacherSubjectDto) => {
        return item.id === id;
    });

    if (selectedItem.value) {
        fillForm(selectedItem.value);
        return;
    }

    if (localItem) {
        fillForm(localItem);
    }
}

function handleTableAction(payload: {
    actionKey: OrganizationTableActionKey;
    item: TeacherSubjectListItemView;
}): void {
    if (payload.actionKey === "details") {
        selectItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "setPrimary") {
        void setPrimaryItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "edit") {
        void openEditForm(payload.item.id);
        return;
    }

    if (payload.actionKey === "deactivate") {
        void deactivateItem(payload.item.id);
        return;
    }

    if (payload.actionKey === "restore") {
        void restoreItem(payload.item.id);
    }
}

onMounted(() => {
    void loadItems();
});
</script>

<template>
    <OrganizationWorkspace
        :search-value="filters.search"
        search-placeholder="Поиск по преподавателю, предмету или email"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Найти"
        refresh-label="Обновить"
        create-label="Назначить предмет"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <TeacherSubjectListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка предмета преподавателя"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем назначение предмета..."
                />

                <TeacherSubjectDetailsPanel
                    v-else
                    :details="selectedDetails"
                    @edit="openEditForm()"
                    @close="clearSelection"
                />
            </OrganizationDetailsModal>
        </template>
    </OrganizationWorkspace>

    <OrganizationDetailsModal
        :is-open="isFormModalOpen"
        :title="formMode === 'create' ? 'Назначение предмета' : 'Редактирование предмета'"
        @close="closeFormModal"
    >
        <TeacherSubjectForm
            :model-value="form"
            :teacher-options="teacherOptions"
            :subject-options="subjectOptions"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новое назначение' : 'Данные назначения'"
            text="Выберите преподавателя и учебный предмет."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отмена"
            :is-submitting="isSubmitting"
            @update:model-value="updateFormModel"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>
</template>
