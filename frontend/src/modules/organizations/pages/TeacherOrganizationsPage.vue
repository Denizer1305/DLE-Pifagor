<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import DashboardStateView from "@/components/dashboard/shared/DashboardStateView.vue";

import OrganizationDetailsModal from "../components/shared/OrganizationDetailsModal.vue";
import OrganizationWorkspace from "../components/shared/OrganizationWorkspace.vue";
import TeacherOrganizationDetailsPanel from "../components/teacher-organizations/TeacherOrganizationDetailsPanel.vue";
import TeacherOrganizationForm from "../components/teacher-organizations/TeacherOrganizationForm.vue";
import TeacherOrganizationListTable from "../components/teacher-organizations/TeacherOrganizationListTable.vue";
import { useOrganizationDictionaries, useTeacherOrganizations } from "../composables";
import { TEACHER_EMPLOYMENT_TYPE_OPTIONS } from "../data";
import type {
    OrganizationTableActionKey,
    TeacherOrganizationDto,
    TeacherOrganizationId,
    TeacherOrganizationListItemView,
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
} = useTeacherOrganizations();

const {
    organizationOptions,
    reloadDictionaries,
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

async function openEditForm(id?: TeacherOrganizationId): Promise<void> {
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

async function selectAndWaitDetails(id: TeacherOrganizationId): Promise<void> {
    await loadDetails(id);

    const localItem = items.value.find((item: TeacherOrganizationDto) => {
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
    item: TeacherOrganizationListItemView;
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
        search-placeholder="Поиск по преподавателю, email или организации"
        :is-loading="isLoading"
        :is-action-loading="isActionLoading"
        :has-active-filters="hasActiveFilters"
        :is-empty="!hasItems"
        :error-message="errorMessage"
        :empty-state="emptyState"
        filters-label="Найти"
        refresh-label="Обновить"
        create-label="Привязать преподавателя"
        @update:search-value="setSearch"
        @search="submitSearch"
        @refresh="loadItems"
        @create="openCreateForm"
    >
        <TeacherOrganizationListTable
            :items="viewItems"
            :columns="tableConfig.columns"
            :actions="tableConfig.actions"
            @select="selectItem($event.id)"
            @action="handleTableAction"
        />

        <template #details>
            <OrganizationDetailsModal
                :is-open="Boolean(selectedDetails) || isDetailsLoading"
                title="Карточка связи преподавателя"
                @close="clearSelection"
            >
                <DashboardStateView
                    v-if="isDetailsLoading"
                    variant="loading"
                    text="Загружаем данные связи преподавателя..."
                />

                <TeacherOrganizationDetailsPanel
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
        :title="formMode === 'create' ? 'Связь преподавателя с организацией' : 'Редактирование связи'"
        @close="closeFormModal"
    >
        <TeacherOrganizationForm
            :model-value="form"
            :teacher-options="teacherOptions"
            :organization-options="organizationOptions"
            :employment-type-options="TEACHER_EMPLOYMENT_TYPE_OPTIONS"
            :errors="fieldErrors"
            :title="formMode === 'create' ? 'Новая связь' : 'Данные связи'"
            text="Выберите преподавателя, организацию и параметры занятости."
            :submit-label="formMode === 'create' ? 'Создать' : 'Сохранить'"
            cancel-label="Отмена"
            :is-submitting="isSubmitting"
            @update:model-value="updateFormModel"
            @submit="submitForm"
            @cancel="closeFormModal"
        />
    </OrganizationDetailsModal>
</template>
